import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, db_drop_and_create, insert_basic_data

from datetime import date

CASTING_ASSISTANT_JWT = os.getenv('CASTING_ASSISTANT_JWT', "Not set")
CASTING_DIRECTOR_JWT = os.getenv('CASTING_DIRECTOR_JWT', "Not set")
EXECUTIVE_PRODUCER_JWT = os.getenv('EXECUTIVE_PRODUCER_JWT', "Not set")

if (CASTING_ASSISTANT_JWT == "Not set") or (CASTING_DIRECTOR_JWT == "Not set") or (EXECUTIVE_PRODUCER_JWT == "Not set"):
    print("No JWT set")
    EXECUTIVE_PRODUCER_JWT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjQ2ZDZtYXBxTDh4VFJNdmFRNnRaQyJ9.eyJpc3MiOiJodHRwczovL2Rldi10LTRzZzUtNi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZmNzc0ZDQ5YWY0YmYwMDc2MmJmOWQ5IiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNjExMzk2NTI2LCJleHAiOjE2MTE0ODI5MjYsImF6cCI6IkRSUWt2d1FacmR2cEJPczY1d3pHU3o0cG14VHBzMXR4Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.Sc1bRP5exP8lUe8LozfCZx6uRPCcqhA-Jd62qugXRsbIrQmwuNA1mFu8BL4p1Wzm9LfZARKK-SC8_fmKkss8uz-1K76bakz_XfuIyTRmZ-_lQr2R52flBLC-Wz-QpmmDBGK-q3ksHs-VWKrOu9zvudNnisiKLJhkxq6XkCa3BZq9irq0AD7q74Mn8uq-On6Fmze0ZL02HBVE1VJHrpE9whVVbP1lGNrOqB4RA_zS-gt-tfjM18YbNMJ_nClsf7_CpVpsk97aEx99wYp2Qmvmda5-1PqpcQym0Xj5Sj4w7HkHF9zmKRk-ySBvd8BPRMQY0HwL97KfZonhzySu06Npkw"
    CASTING_ASSISTANT_JWT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjQ2ZDZtYXBxTDh4VFJNdmFRNnRaQyJ9.eyJpc3MiOiJodHRwczovL2Rldi10LTRzZzUtNi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwOWZmZDk3MDM4ZTIwMDcxYzcyZDY5IiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNjExNDA0ODIxLCJleHAiOjE2MTE0OTEyMjEsImF6cCI6IkRSUWt2d1FacmR2cEJPczY1d3pHU3o0cG14VHBzMXR4Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.HUaWBN8jvvTa4gwmBJuh8WxCNOiEjU2p0AMDLc_MUdP0-qwLGKsjUF3oHpWjdMPuMvx7mTihgdelgCe6orFqH-5XmoUlCjf0jU1-vZaB_5lbIgXTulB-PPhsr9e3VGSbSCGLC37-qZXFiBRTFxKT1v4NwuQP1c2Mlc9nfPx-YZo6rCTwYy6wuEhe9__at_6eJCJT5TYcF_wEjb5CCi5mLCvhUoPsLOMnVeV_pesBw9JV_Vx6cy-RJQR3AEX6f4JJB3-knMNQ5UZ7EIQqrIuwrCYg1JfXneJfEcsLPNyVH4ZSzcihAovt4eB3rsjyCRoqoc6ltWDXDRwtFTN3h6elfg"
    CASTING_DIRECTOR_JWT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjQ2ZDZtYXBxTDh4VFJNdmFRNnRaQyJ9.eyJpc3MiOiJodHRwczovL2Rldi10LTRzZzUtNi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwYzE1NjM1MjM4ZmIwMDY5NWYzMTAyIiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNjExNDA0OTczLCJleHAiOjE2MTE0OTEzNzMsImF6cCI6IkRSUWt2d1FacmR2cEJPczY1d3pHU3o0cG14VHBzMXR4Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.ty7IXi4hwkooLL6c2mUqRRd7UzQFsCAMdJxnw1J566c4TmBpxlllMkeF_JLBQXRCanuFcCmR18wp5ys8qkqIlVpmsPoQV2oaSPox_GDGY5HB6ORK_99K3Q58UjjNqh59HsuG-x9OddFMUJvYM5y4pGQtukYtpQd35Czh6-YdIpRhKa_6bANPYNt1ewhK832fe-Hty6wOZPTelX6AIAUlBJGTrNbup1yFMZN5qPO-wfAO1MEUPjqnmSACpN9E6cFpeTcbBHMrHbOJsOSS5c3xuXn0mDyQqdh5QlJKzzVQxq0_uLolddYdpJioqm6ts81r1SF077AeFdwmRfopacbguQ"

casting_assistant_header = {
    "Authorization": "Bearer " + CASTING_ASSISTANT_JWT
}

casting_director_header = {
    "Authorization": "Bearer " + CASTING_DIRECTOR_JWT 
}

executive_producer_header = {
    "Authorization": "Bearer " + EXECUTIVE_PRODUCER_JWT
}

class AgencyTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
           
        self.database_name = "capstone_test"
        self.database_type = 'postgres'
        self.database_code = 'Coding2!su'
        self.database_host = 'localhost:5432'
        self.database_path = "postgres://{}:{}@{}/{}".format(self.database_type, self.database_code , self.database_host , self.database_name)
        setup_db(self.app, self.database_path)

        db_drop_and_create()

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
    Moivie Tests 
    '''
    # Test Get Movies

    def test_get_movies(self):
        res = self.client().get("/movies", headers=casting_assistant_header)
        data = json.loads(res.data.decode('utf-8'))
        # data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["movies"])

    def test_get_movies_no_header_401(self):
        res = self.client().get("/movies")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)


    # Create movie

    def test_post_movie(self):
        new_movie = {
            "title": "Matrix 3",
            "release_date": date.today(),
            "imdb_rating": 10,
        }

        res = self.client().post("/movies", json=new_movie, headers=executive_producer_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["message"],"Whatever you add, Matrix is the best movie")

    def test_post_movie_no_auth_403(self):
        new_movie = {
            "title": "Matrix 3",
            "release_date": date.today(),
            "imdb_rating": 10,
        }

        res = self.client().post("/movies", json=new_movie, headers=casting_assistant_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 403)


    # Update movie

    def test_update_movie(self):
        update_movie = {
            "title": "Bananas in Pyjamas",
            "release_date": date.today(),
            "imdb_rating": 1,
        }
        res = self.client().patch("/movies/1", json=update_movie, headers=casting_director_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_update_movie_no_auth_403(self):
        update_movie = {
            "title": "Bananas in Pyjamas",
            "release_date": date.today(),
            "imdb_rating": 1,
        }
        res = self.client().patch("/movies/1", json=update_movie, headers=casting_assistant_header)
        data = json.loads(res.data.decode('utf-8'))
        
        self.assertEqual(res.status_code, 403)

    # Delete Movie

    def test_delete_movie(self):
        res = self.client().delete("/movies/1", headers=executive_producer_header)

        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_delete_movie_no_auth_403(self):
        res = self.client().delete("/movies/1", headers=casting_assistant_header)
        data = json.loads(res.data.decode('utf-8'))
        
        self.assertEqual(res.status_code, 403)

    # Get Actor

    def test_get_actors(self):
        res = self.client().get("/actors", headers=casting_assistant_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["actors"])

    def test_get_actors_no_header_401(self):
        res = self.client().get("/actors")
        data = json.loads(res.data.decode('utf-8'))
        
        self.assertEqual(res.status_code, 401)

    # Create Actor

    def test_create_actor(self):
        new_actor = {
            "name": "Laurence Fishburne",
            "age": 59,
            "gender": "Male"
        }
        res = self.client().post("/actors", json=new_actor, headers=casting_director_header)
        data = json.loads(res.data.decode('utf-8'))
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_create_actor_no_header_403(self):
         new_actor = {
            "name": "Laurence Fishburne",
            "age": 59,
            "gender": "Male"
        }
        res = self.client().get("/actors", json=new_actor, headers=casting_assistant_header)
        data = json.loads(res.data.decode('utf-8'))
        
        self.assertEqual(res.status_code, 403)

    # Update Actor

    def test_patch_actor(self):
        patch_actor = {
            "name": "Hugo Weaving",
            "age": 59,
            "gender": "Male"
        }
        res = self.client().patch("/actors/1", json=patch_actor, headers=casting_director_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["actor"]),1)

    def test_patch_actor_no_auth_403(self):
        patch_actor = {
            "name": "Hugo Weaving",
            "age": 59,
            "gender": "Male"
        }
        res = self.client().patch("/actors/1", json=patch_actor, headers=casting_assistant_header)
        data = json.loads(res.data.decode('utf-8'))
        
        self.assertEqual(res.status_code, 403)

    # delete Actor

    def test_delete_actor(self):
        res = self.client().delete("/actors/1", headers=casting_director_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["deleted_actor"]), 1)

    def test_delete_actor_no_auth_403(self):
        res = self.client().delete("/actors/1", headers=casting_assistant_header)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 403)

if __name__ == "__main__":
    unittest.main()
