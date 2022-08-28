import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor


# JWTs for each role

Casting_Assistant = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBvdzNPUjAxNmd6Q0VxYXJrcnAteiJ9.eyJpc3MiOiJodHRwczovL2NoZXpwaXRvdS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjMwYTVlNmE5ZWViMzhkZmEyMTg3NTJmIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2NjE3MDg0MTIsImV4cCI6MTY2MTc5NDgxMiwiYXpwIjoidE1WTXlRbVBKRFBSZGsyZFZ3dTVuVVloaE9ISTd4ZW8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.itWMqPDcJdiiRoglNbr8O6h8BSmNEwJXCbM1ube5IkJ5UNi3CIsvs9CkIjgvOJaIEGi5AYhmeg4PbfYZfXUJDvDsXK38H2DB1K0pD4uNkxCmRFBcmvr68puIV3gea5sFSNGefbahQRWGSopl-66QRJXl-00B73uQwqh1mqX8DKfcmYgk4s69lHZ_tt21KTTlgy7g3XauQoBQ-nQBjWOgE2A4mvhFrOlv7Dmc3B1C6p9J6J3DNIqbkEfT6ISdOc26_Jkaokz9wADQNlwbnovBvagpG2rLfZstr0_02Ijn3U0BUc2hUvLiIr044Af1k8HhwQlBH35sMjqmQ_fF3ETuaw')
Casting_Director = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBvdzNPUjAxNmd6Q0VxYXJrcnAteiJ9.eyJpc3MiOiJodHRwczovL2NoZXpwaXRvdS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjMwYTVlZTgzMTM0MGMyNjUwMTMzNzNiIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2NjE3MDg0NjQsImV4cCI6MTY2MTc5NDg2NCwiYXpwIjoidE1WTXlRbVBKRFBSZGsyZFZ3dTVuVVloaE9ISTd4ZW8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.mLr2Y37y6-K1zX4iqhc3FyHgLq1uo1Csquv5B0-mTG6n_tZ7jOYa6kk_WYPPFCGcpa_go5u9csiK423h492BdFtOupQRWMlQRKrtGY3la7k37veq7nkIlroWJgq6R5ZhcvvlSJd3L-pAz8f53t_JiDn-2JqVFcw-bw9gXCSTKUhhSGza5xW02C74216Zxj6SQeH74BOQa_2HILwxJ-wx_uE7JFogoGTRmAXWDQpygHnXnUZW0S1xh3IURN6yjV2eukHlyUyMf5tV36oSE5wLOTNF4CXOcUKtQYs3PeWND-Zf8ADkfFEKJYEAnlU9LSzam-V_7Aky3pu-0QHzeoxUzw')

class CastingTest(unittest.TestCase):

# SetUp Application for Tests

    def setUp(self):
        
        self.app = create_app()
        self.client = self.app.test_client
        self.test_movie = {
            'title': 'Example movie',
            'release_date': '2022-01-01',
        }

        self.database_path = os.environ['DATABASE_URL']

        setup_db(self.app, self.database_path)


# Teardown activated after each test 

    def tearDown(self):
        pass

# Overview - Lists of tests
# Get movies
# Get movies - Error behaviour
# Get movie by id 
# Get movie by id - Error behaviour
# Add new movie
# Add new movie - Error behaviour
# Update a movie
# Update a movie - Error behaviour
# Delete a movie
# Delete a movie - Error behaviour
# Get actors
# Get actors - Error behaviour
# Get actor by id 
# Get actor by id - Error behaviour
# Add new actor
# Add new actor - Error behaviour
# Update an actor
# Update an actor - Error behaviour
# Delete an actor 
# Delete an actor - Error behaviour
# RBAC - Add new movie
# RBAC - Delete actor

    # Test: Get movies 

    def test_get_movies(self):
        response = self.client().get('/movies', headers={'Authorization': f'Bearer {Casting_Assistant}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Test: Get movies - Error behaviour - invalid header

    def test_get_actors_error(self):
        response = self.client().get('/movies', headers={"Authorization": f'Pizza {Casting_Assistant}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 401)

    # Test: Get movie by id 

    def test_get_movie_by_id(self):
        response = self.client().get('/movies/1', headers={"Authorization": f'Bearer {Casting_Assistant}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    # Test: Get movie by id - Error behaviour 404 - wrong ID for non-existing movie

    def test_get_movie_by_id_error(self):
        response = self.client().get('/movies/99', headers={"Authorization": f'Bearer {Casting_Assistant}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)

    # Test: Add new movie - RBAC Error

    def test_add_movie_error_rbac(self):
        response = self.client().post('/movies', json=self.test_movie, headers={"Authorization": f'Bearer {Casting_Assistant}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 403)

    # Test: Add new movie

    def test_add_movie(self):
        response = self.client().post('/movies', json=self.test_movie, headers={"Authorization": f'Bearer {Casting_Director}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], 'Example movie1')

    # Test: Add new movie - Error behaviour 400 - JSON includes no Data which should trigger a Bad request 400
    
    def test_add_movie_error(self):
        response = self.client().post('/movies', json={}, headers={"Authorization": f'Bearer {Casting_Director}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)

    # Test: Update a movie

    def test_update_movie(self):
        response = self.client().patch('/movies/1', json={'title': 'Patched movie', 'release_date': '2022-02-01'}, headers={"Authorization": f'Bearer {Casting_Director}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], 'Patched movie')

    # Test: Update a movie - Error behaviour - JSON includes no Data which should trigger a Bad request 400

    def test_update_movie_error(self):
        response = self.client().patch('/movies/1', json={}, headers={"Authorization": f'Bearer {Casting_Director}'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)

    # Test: Delete a movie - Error behaviour 404 - wrong ID for non-existing movie

    def test_delete_movie_error(self):
        response = self.client().delete('/movies/99', headers={'Authorization': f'Bearer {Casting_Director}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)

    # Test: Delete a movie

    def test_delete_movie(self): 
        response = self.client().delete('/movies/1', headers={'Authorization': f'Bearer {Casting_Director}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])


    # Test: Get actors

    def test_get_actors(self):
        response = self.client().get('/actors', headers={'Authorization': f'Bearer {Casting_Assistant}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Test: Get actors - Error behaviour - invalid header

    def test_get_actors_error(self):
        response = self.client().get('/actors', headers={"Authorization": f'Pizza {Casting_Assistant}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 401)

    # Test: Get actor by id 

    def test_get_actor_by_id(self):
        response = self.client().get('/actors/1', headers={"Authorization": f'Bearer {Casting_Assistant}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])


    # Test: Get actor by id - Error behaviour

    def test_get_actor_by_id_error(self):
        response = self.client().get('/actors/99', headers={"Authorization": f'Bearer {Casting_Assistant}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)

    # Test: Add new actor

    def test_add_actor(self):
        response = self.client().post('/actors', json={'name': 'Michael', 'age': 25, 'gender': 'male'}, headers={"Authorization": f'Bearer {Casting_Director}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test: Add new actor - Error behaviour 400 - JSON includes no data

    def test_add_actor_error(self):
        response = self.client().post('/actors', json={}, headers={"Authorization": f'Bearer {Casting_Director}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)

    # Test: Update an actor

    def test_update_actor(self):
        response = self.client().patch('/actors/1', json={'name': 'Markus', 'age': '29', 'gender': 'male'}, headers={"Authorization": f'Bearer {Casting_Director}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test: Update an actor - Error behaviour

    def test_update_actor_error(self):
        response = self.client().patch('/actors/1', json={}, headers={"Authorization": f'Bearer {Casting_Director}'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)

    # Test: Delete an actor - Error behaviour 404 - wrong ID for non-existing actor

    def test_delete_actor_error(self):
        response = self.client().delete('/actors/99', headers={'Authorization': f'Bearer {Casting_Director}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)

    # Test: RBAC for delete actor

    def test_delete_actor_error_rbac(self): 
        response = self.client().delete('/actors/1', headers={'Authorization': f'Bearer {Casting_Assistant}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)

    # Test: Delete an actor 

    def test_delete_actor(self): 
        response = self.client().delete('/actors/1', headers={'Authorization': f'Bearer {Casting_Director}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])




