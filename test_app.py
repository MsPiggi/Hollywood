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
    EXECUTIVE_PRODUCER_JWT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjQ2ZDZtYXBxTDh4VFJNdmFRNnRaQyJ9.eyJpc3MiOiJodHRwczovL2Rldi10LTRzZzUtNi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZmNzc0ZDQ5YWY0YmYwMDc2MmJmOWQ5IiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNjExNTA0MTU4LCJleHAiOjE2MTE1OTA1NTgsImF6cCI6IkRSUWt2d1FacmR2cEJPczY1d3pHU3o0cG14VHBzMXR4Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.BmM81qL9OgMe3YnkMXa0H8_ZNUxHywSft8oC8M9nIk1pPH3RcJT2FVzBzzgdH1zG8NFNq7MORemNLzmHzzP5H0CyblVa6Cfd5pzGSIoiyHJd4nYS79Zz7vGdnVJ27UYHu1SXNEPbnFWm4ISFFfqF7eat5lXKOYiiemvAImBC4vgfsp5BSisOg_0onCZy-EYgHgSHU2N47KY0wtQl65t7d3Glno6cD1XI6LJ7KEbWUo3oYmY7jxDn-z8tg2d64bewSMi0-5cP2YJRlPYJPzTqjgBAcEH5bW9OlKVNVWOQfNGS-EcfiJv_W9peG8MEplTr5H4nhUHst9A5Fi7GDD9urg"
    CASTING_ASSISTANT_JWT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjQ2ZDZtYXBxTDh4VFJNdmFRNnRaQyJ9.eyJpc3MiOiJodHRwczovL2Rldi10LTRzZzUtNi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwOWZmZDk3MDM4ZTIwMDcxYzcyZDY5IiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNjExNTA0MjcyLCJleHAiOjE2MTE1OTA2NzIsImF6cCI6IkRSUWt2d1FacmR2cEJPczY1d3pHU3o0cG14VHBzMXR4Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.hKS-4CodHMjcQ0KX3FkV7OveppaD0vbE6To-kLR3nSDPL09ZDY9U3RH-ZEQllxciftYqSry8o84Dd6JcLYrkQ-l9YCRfm6XBy59DAuC4JrEJ-ffT-ewGIqOZd-j1-7J-oUEsENimkN35Uf0JdDNgDtjURJrYfTszkrZY_CRHqgLrrnBrgc0EPY_IGZp0tC_BsLEl8CSjwPUOpln-9fPs1-NrGzMZXZtEbbmIpQaSYbkI86qgn12YbM2Hceh8H-jvx9GxJWXS9mLb05WPO5bNWC2kQGZk8E5vQjBFFIKskgHYjGe4QKgJqSUhVIBSuFYD4PQOQI_tCG8NkcX5MnFB0g"
    CASTING_DIRECTOR_JWT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjQ2ZDZtYXBxTDh4VFJNdmFRNnRaQyJ9.eyJpc3MiOiJodHRwczovL2Rldi10LTRzZzUtNi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwYzE1NjM1MjM4ZmIwMDY5NWYzMTAyIiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNjExNTA0MzUwLCJleHAiOjE2MTE1OTA3NTAsImF6cCI6IkRSUWt2d1FacmR2cEJPczY1d3pHU3o0cG14VHBzMXR4Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.ClkPBAru3erUyR7sainf4QDPhphdMndehOfE_BwGpotroWSolUhhwdVVe_J8LYdUSoX789pJzutpFCfe5yXZyHJj5VQac4Fh1YOMWP1QvqPHgNQTMDm1UP6ic4sRgYmI_8ljes4xgy7GsBapxCWl8svgPVdCF7GFTjKugRq-0vzxp3kbcNVtBjfJLR_GYaX9rjRtuA2k0errx3LDhmNGcrnQb4umfpsA6s9U0pregOcLB66Ils3ChDTF-Q5IWCD8ipq4Fls81KwWv0rv6yUcdx-xtRmvizN9ldwMfEUuVGJ05yvvenF-df5E_whLHsQxA9h06REWWIA8zPGgx8mLJw"

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

    def test_create_actor_no_header_401(self):
        new_actor = {
            "name": "Laurence Fishburne",
            "age": 59,
            "gender": "Male"
        }
        res = self.client().get("/actors", json=new_actor)
        data = json.loads(res.data.decode('utf-8'))
        
        self.assertEqual(res.status_code, 401)

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
