import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movies, Actors, Relation
from api import create_app
from config import Authtoken, database


class TriviaTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.executive_director = Authtoken["executive_director"]

        # Uncomment this while connecting to heroku
        # self.database_path = os.environ['DATABASE_URL']

        # Uncomment this while connecting locally
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            database["username"], database["username_password"],
            database["port"], database["database_name"])
        setup_db(self.app, self.database_path)

    def test_a_get_actors(self):
        res = self.client().get(
            '/actors', headers={"Authorization": self.executive_director})
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_b_get_movies(self):
        res = self.client().get(
            '/movies', headers={"Authorization": self.executive_director})
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_c_add_actor(self):
        json_data = {
                    "name": "Bill",
                    "age": 27,
                    "gender": "female"}

        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]

        res = self.client().post('/actors', json=json_data, headers=head)

        data = res.json

        ans = Actors.query.filter(Actors.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['name'], ans.name)
        self.assertEqual(data['age'], ans.age)
        self.assertEqual(data['gender'], ans.gender)

    def test_d_add_movie(self):
        json_data = {
                    "title": "Yourmovie",
                    "release_date": "11/11/2011"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]

        res = self.client().post('/movies', json=json_data, headers=head)
        data = res.json

        ans = Movies.query.filter(Movies.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['title'], ans.title)

    def test_e_add_actor_to_movie(self):
        json_data = {
                    "movie_id": 1,
                    "actor_id": 1}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]
        res = self.client().post('/movies/cast', json=json_data, headers=head)
        data = res.json

        ans = Relation.query.filter(
            Relation.movie_id == 1 and Relation.actor_id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie_id'], ans.movie_id)
        self.assertEqual(data['actor_id'], ans.actor_id)

    def test_f_edit_actor(self):
        json_data = {
                "name": "will",
                "age": 53,
                "gender": "female"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]
        res = self.client().patch('/actors/1', json=json_data, headers=head)
        data = res.json

        ans = Actors.query.filter(Actors.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['name'], ans.name)
        self.assertEqual(data['age'], ans.age)
        self.assertEqual(data['gender'], ans.gender)

    def test_g_edit_movie(self):
        json_data = {
                    "title": "will",
                    "release_date": "2/2/2002"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]
        res = self.client().patch('/movies/1', json=json_data, headers=head)
        data = res.json

        ans = Movies.query.filter(Movies.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['title'], ans.title)

    def test_h_delete_actor_from_movie(self):
        head = {"Authorization": self.executive_director}
        res = self.client().delete(
            '/movies/cast?actorid=1&movieid=1', headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data["actor_id"], 1)
        self.assertEqual(data["movie_id"], 1)

    def test_i_delete_movie(self):
        head = {"Authorization": self.executive_director}
        res = self.client().delete(
            '/movies/1', headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data["movie_id"], '1')

    def test_j_delete_actor(self):
        head = {"Authorization": self.executive_director}
        res = self.client().delete(
            '/actors/1', headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data["actor_id"], '1')

    def test_k_error_add_actors(self):
        head = {"Authorization": self.executive_director}
        res = self.client().post(
            '/actors', headers=head)
        data = res.json

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_l_error_add_movies(self):
        head = {"Authorization": self.executive_director}
        res = self.client().post(
            '/movies', headers=head)
        data = res.json

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_m_error_422_add_actor_to_movie(self):
        head = {"Authorization": self.executive_director}
        res = self.client().post(
            '/movies/cast', headers=head)
        data = res.json

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_n_error_409_add_actor_to_movie(self):
        json_data = {
                "movie_id": 1,
                "actor_id": 1}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]
        res = self.client().post('/movies/cast', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['success'], False)

    def test_o_error_404_edit_actor(self):
        json_data = {
                    "name": "will",
                    "age": 53,
                    "gender": "male"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]
        res = self.client().patch('/actors/9', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_p_error_422_edit_actor(self):
        json_data = {
                    "name": "will",
                    "age": 53,
                    "gender": "female"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]
        self.client().post('/actors', json=json_data, headers=head)

        json_data = {
                "gender": "jfd"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]

        res = self.client().patch('/actors/2', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_q_error_404_edit_movie(self):
        json_data = {
                "title": "Matrix",
                "release_date": "11/11/2011"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]
        res = self.client().patch('/movies/9', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_r_error_422_edit_movie(self):
        json_data = {
                "title": "Yourmovie",
                "release_date": "11/11/2011"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]
        self.client().post('/movies', json=json_data, headers=head)

        head2 = [
            ('Content-Type', 'application/json'),
            ('Authorization', self.executive_director)]
        res = self.client().patch('/movies/2', headers=head2)
        data = res.json

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_s_error_delete_actor(self):
        head = {"Authorization": self.executive_director}
        res = self.client().delete(
            '/actors/9', headers=head)
        data = res.json

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_t_error_delete_movie(self):
        head = {"Authorization": self.executive_director}
        res = self.client().delete(
            '/movies/9', headers=head)
        data = res.json

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_u_error_delete_actor_from_movie(self):
        head = {"Authorization": self.executive_director}
        res = self.client().delete('/movies/cast', headers=head)
        data = res.json

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
