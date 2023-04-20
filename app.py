import os
from flask import Flask, abort, jsonify, request
from models import setup_db, Actor, Movie
from flask_cors import CORS
from datetime import datetime

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"
    
    @app.route('/actors', methods=['GET'])
    def get_actors():
        res = [actor.format() for actor in Actor.query.all()]
        return jsonify({
            'success': True,
            'actors': res,
            'total_actors': len(res)
        })
    
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actors(actor_id):
        actor = Actor.query.filter(Actor.id==actor_id).one_or_none()
        if actor is None:
            abort(404)
        actor.delete()
        return jsonify({
                "success": True,
                "deleted": actor_id
            })
    
    @app.route('/actors', methods=['POST'])
    def post_actors():
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
    def patch_actors(actor_id):
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
    def delete_movies(movie_id):
        movie = Movie.query.filter(Movie.id==movie_id).one_or_none()
        if movie is None:
            abort(404)
        movie.delete()
        return jsonify({
                "success": True,
                "deleted": movie_id
            })
    
    @app.route('/movies', methods=['POST'])
    def post_movies():
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
    def patch_movies(movie_id):
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
    app.run()
