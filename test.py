import os
from datetime import datetime
import unittest
import requests
import time

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    my_url = "https://castpone.onrender.com"
    assistant_token = {'Content-Type': 'application/json', 'Authorization':"Bearer {}".format(os.environ['ASSISTANT'])}
    director_token = {'Content-Type': 'application/json', 'Authorization':"Bearer {}".format(os.environ['DIRECTOR'])}
    producer_token = {'Content-Type': 'application/json', 'Authorization':"Bearer {}".format(os.environ['PRODUCER'])}

    def setUp(self):
        pass
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # test for producer who has all permissions
    # post a actor
    def test_1_1_create_actor_ok_200(self):
        data = {'name': 'Jane','age': 26, 'gender':'female'}
        res = requests.post(self.my_url + "/actors", json=data, headers=self.producer_token)
        
        print("------------------")
        print(res)
        print("------------------")
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["created"])

        data = {'name': 'Tom','age': 25, 'gender':'male'}
        res = requests.post(self.my_url + "/actors", json=data, headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["created"])

        data = {'name': 'Ken','age': 27, 'gender':'male'}
        res = requests.post(self.my_url + "/actors", json=data, headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["created"])
    
    def test_1_2_create_actor_failed_422(self):
        data = {'age': 20, 'gender':'female'}
        res = requests.post(self.my_url + "/actors", json=data, headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 422)

    # get actors
    def test_1_3_get_actors_200(self):
        res = requests.get(self.my_url + "/actors")
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        
    # patch an actor
    def test_1_4_patch_actors_200(self):
        data = {'name': 'Jane','age': 22, 'gender':'female'}
        res = requests.patch(self.my_url + "/actors/1", json=data, headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["edited"])
    
    def test_1_5_patch_actors_404(self):
        data = {'name': 'Jane','age': 22, 'gender':'female'}
        res = requests.patch(self.my_url + "/actors/1000", json=data, headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 404)

    # delete an actor
    def test_1_6_delete_actors_200(self):
        res = requests.delete(self.my_url + "/actors/3", headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["deleted"])
    
    def test_1_7_delete_actors_404(self):
        res = requests.delete(self.my_url + "/actors/300", headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 404)

    # test for producer who has all permissions
    # post a movie
    def test_2_1_create_movie_ok_200(self):
        date_time = datetime(2021, 7, 1, 12, 15)
        unix_timestamp = time.mktime(date_time.timetuple())
        data = {'title': 'Gone with the Wind','release_date': unix_timestamp}
        res = requests.post(self.my_url + "/movies", json=data, headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["created"])

        date_time = datetime(2010, 12, 15, 8, 0)
        unix_timestamp = time.mktime(date_time.timetuple())
        data = {'title': 'Coco','release_date': unix_timestamp}
        res = requests.post(self.my_url + "/movies", json=data, headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["created"])
    
    def test_2_2_create_movie_failed_422(self):
        date_time = datetime(2001, 2, 3, 4, 5)
        unix_timestamp = time.mktime(date_time.timetuple())
        data = {'release_date': unix_timestamp}
        res = requests.post(self.my_url + "/movies", json=data, headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 422)

    # get movies
    def test_2_3_get_movies_200(self):
        res = requests.get(self.my_url + "/movies")
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        
    # patch a movie
    def test_2_4_patch_movies_200(self):
        date_time = datetime(2021, 7, 1, 12, 15)
        unix_timestamp = time.mktime(date_time.timetuple())
        data = {'title': 'Gone with the Wind-new name','release_date': unix_timestamp}
        res = requests.patch(self.my_url + "/movies/1", json=data, headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["edited"])
    
    def test_2_5_patch_movies_404(self):
        date_time = datetime(2021, 7, 1, 12, 15)
        unix_timestamp = time.mktime(date_time.timetuple())
        data = {'title': 'Gone with the Wind-new new name','release_date': unix_timestamp}
        res = requests.patch(self.my_url + "/movies/1000", json=data, headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 404)

    # delete a movie
    def test_2_6_delete_movies_200(self):
        res = requests.delete(self.my_url + "/movies/2", headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["deleted"])

    def test_2_7_delete_movies_404(self):
        res = requests.delete(self.my_url + "/movies/200", headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 404)

    # assign an actor to movie
    def test_3_1_assign_actor_movie_200(self):
        res = requests.post(self.my_url + "/movies/1/actors/1", headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["created"])
        res = requests.post(self.my_url + "/movies/1/actors/2", headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["created"])

    def test_3_2_assign_actor_404(self):
        res = requests.post(self.my_url + "/movies/1/actors/1000", headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 404)

    def test_3_3_assign_movie_404(self):
        res = requests.post(self.my_url + "/movies/1000/actors/1", headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 404)
    
    # get actors to movie
    def test_3_4_get_actors_of_movie_200(self):
        res = requests.get(self.my_url + "/movies/1/actors", headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_3_5_get_actors_of_movie_404(self):
        res = requests.get(self.my_url + "/movies/1000/actors", headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 404)
    
    # delete actors from movie
    def test_3_6_delete_actor_from_movie_200(self):
        res = requests.delete(self.my_url + "/movies/1/actors/2", headers=self.producer_token)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_3_7_delete_actor_from_movie_404_1(self):
        res = requests.delete(self.my_url + "/movies/1/actors/100", headers=self.producer_token)
        self.assertEqual(res.status_code, 404)

    def test_3_8_delete_actor_from_movie_404_2(self):
        res = requests.delete(self.my_url + "/movies/100/actors/1", headers=self.producer_token)
        self.assertEqual(res.status_code, 404)

    # no token
    def test_4_1_create_actor_no_token_401(self):
        data = {'name': 'Jane','age': 20, 'gender':'female'}
        res = requests.post(self.my_url + "/actors", json=data)
        data = res.json()
        self.assertEqual(res.status_code, 401)
    
    # assistant
    def test_4_2_get_assigns_assistant_ok_200(self):
        res = requests.get(self.my_url + "/movies/1/actors", headers=self.assistant_token)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_4_3_create_actor_assistant_fail_403(self):
        data = {'name': 'assistant','age': 20, 'gender':'male'}
        res = requests.post(self.my_url + "/actors", json=data, headers=self.assistant_token)
        data = res.json()
        self.assertEqual(res.status_code, 403)

    # director
    def test_4_4_create_actor_director_ok_200(self):
        data = {'name': 'director','age': 30, 'gender':'female'}
        res = requests.post(self.my_url + "/actors", json=data, headers=self.director_token)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["created"])
    
    def test_4_5_create_movie_director_fail_403(self):
        date_time = datetime(2010, 12, 15, 8, 0)
        unix_timestamp = time.mktime(date_time.timetuple())
        data = {'title': 'Movie for director','release_date': unix_timestamp}
        res = requests.post(self.my_url + "/movies", json=data, headers=self.director_token)
        data = res.json()
        self.assertEqual(res.status_code, 403)
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()