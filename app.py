import os
from flask import Flask, abort, jsonify, request, redirect, render_template, session, url_for
from models import setup_db, Actor, Movie, Assign
from flask_cors import CORS
from datetime import datetime
from auth.auth import AuthError, requires_auth

from dotenv import find_dotenv, load_dotenv
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode

def create_app(test_config=None):

    app = Flask(__name__)
    app.secret_key = os.env.get("APP_SECRET_KEY")
    setup_db(app)
    CORS(app)
    oauth = OAuth(app)

    oauth.register(
        "auth0",
        client_id = os.env.get("AUTH0_CLIENT_ID"),
        client_secret = os.env.get("AUTH0_CLIENT_SECRET"),
        client_kwargs = {
            "scope": "openid profile email",
        },
        server_metadata_url=f'https://{os.env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
    )
    
    @app.route("/login")
    def login():
        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for("callback", _external=True)
        )
    
    @app.route("/callback", methods=["GET", "POST"])
    def callback():
        token = oauth.auth0.authorize_access_token()
        session["user"] = token
        return redirect("/")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(
            "https://" + os.env.get("AUTH0_DOMAIN")
            + "/v2/logout?"
            + urlencode(
                {
                    "returnTo": url_for("home", _external=True),
                    "client_id": os.env.get("AUTH0_CLIENT_ID"),
                },
                quote_via=quote_plus,
            )
        )
    
    @app.route("/")
    def home():
        return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
    
    @app.route('/actors', methods=['GET'])
    def get_actors():
        res = [actor.format() for actor in Actor.query.all()]
        return jsonify({
            'success': True,
            'actors': res,
            'total_actors': len(res)
        })
    
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actors(payload, actor_id):
        actor = Actor.query.filter(Actor.id==actor_id).one_or_none()
        if actor is None:
            abort(404)
        actor.delete()
        return jsonify({
                "success": True,
                "deleted": actor_id
            })
    
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def post_actors(payload):
        body = request.get_json()
        new_name = body.get("name", None)
        new_age = body.get("age", None)
        new_gender = body.get("gender", None)

        actor = Actor(name=new_name, age=new_age, gender=new_gender)
        actor.insert()

        return jsonify(
            {
                "success": True,
                "created": actor.id
            }
        )
    
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def patch_actors(payload, actor_id):
        actor = Actor.query.filter(Actor.id==actor_id).one_or_none()
        if actor is None:
            abort(404)
        body = request.get_json()
        actor.name = body.get("name", None)
        actor.age = body.get("age", None)
        actor.gender = body.get("gender", None)
        actor.update()
        return jsonify(
            {
                "success": True,
                "edited": actor.id
            }
        )


    @app.route('/movies', methods=['GET'])
    def get_movies():
        res = [movie.format() for movie in Movie.query.all()]
        return jsonify({
            'success': True,
            'movies': res,
            'total_movies': len(res)
        })
    
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movies(payload, movie_id):
        movie = Movie.query.filter(Movie.id==movie_id).one_or_none()
        if movie is None:
            abort(404)
        movie.delete()
        return jsonify({
                "success": True,
                "deleted": movie_id
            })
    
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def post_movies(payload):
        body = request.get_json()
        new_title = body.get("title", None)
        new_relase_date = datetime.utcfromtimestamp(body.get("release_date", None)).strftime('%Y-%m-%dT%H:%M:%SZ')

        movie = Movie(title=new_title, release_date=new_relase_date)
        movie.insert()

        return jsonify(
            {
                "success": True,
                "created": movie.id
            }
        )
    
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def patch_movies(payload, movie_id):
        movie = Movie.query.filter(Movie.id==movie_id).one_or_none()
        if movie is None:
            abort(404)
        body = request.get_json()
        movie.title = body.get("title", None)
        movie.release_date = datetime.utcfromtimestamp(body.get("release_date", None)).strftime('%Y-%m-%dT%H:%M:%SZ')
        movie.update()
        return jsonify(
            {
                "success": True,
                "edited": movie.id
            }
        )

    @app.route('/movies/<int:movie_id>/actors', methods=['GET'])
    def get_actors_by_movie(movie_id):
        movie = Movie.query.filter(Movie.id==movie_id).one_or_none()
        if movie is None:
            abort(404)
        res = [actor.format() for actor in movie.actors]
        return jsonify(
            {
                "success": True,
                "actors": res,
                "total_actors": len(res)
            }
        )
    
    @app.route("/movies/<int:movie_id>/actors/<int:actor_id>", methods=['POST'])
    @requires_auth('post:assign')
    def assign_actor_to_movie(payload, movie_id, actor_id):
        print("moive_id = ", movie_id)
        print("actor_id = ", actor_id)
        movie = Movie.query.filter(Movie.id==movie_id).one_or_none()
        if movie is None:
            abort(404)
        print("get movie")
        actor = Actor.query.filter(Actor.id==actor_id).one_or_none()
        if actor is None:
            abort(404)
        print("get actor")
        assign = Assign(movie_id=movie_id, actor_id=actor_id)
        assign.insert()
        return jsonify(
            {
                "success": True,
                "created": assign.id
            }
        )

    @app.route("/movies/<int:movie_id>/actors/<int:actor_id>", methods=['DELETE'])
    @requires_auth('delete:assign')
    def remove_actor_from_movie(payload, movie_id, actor_id):
        assign = Assign.query.filter(Assign.movie_id==movie_id).filter(Assign.actor_id==actor_id).one_or_none()
        if assign is None:
            abort(404)
        assign_id = assign.id
        assign.delete()
        return jsonify(
            {
                "success": True,
                "deleted": assign_id
            }
        )
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "resource not found"}), 404
        

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400
    

    return app

app = create_app()

if __name__ == '__main__':
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)
    app.run()
