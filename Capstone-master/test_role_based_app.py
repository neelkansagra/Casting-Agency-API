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
        self.casting_assistant = Authtoken["casting_assistant"]
        self.casting_director = Authtoken["casting_director"]
        self.executive_director = Authtoken["executive_director"]

        # Uncomment this while connecting to heroku
        # self.database_path = os.environ['DATABASE_URL']
        # Uncomment this while connecting locally
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            database["username"], database["username_password"],
            database["port"], database["database_name"])
        setup_db(self.app, self.database_path)

    def test_a_get_actors_by_casting_assistant(self):
        head = {"Authorization": self.casting_assistant}
        res = self.client().get(
            '/actors', headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_b_get_actors_by_casting_director(self):
        head = {"Authorization": self.casting_assistant}
        res = self.client().get(
            '/actors', headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_c_get_actors_by_executive_director(self):
        head = {"Authorization": self.executive_director}
        res = self.client().get(
            '/actors', headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_d_get_movies_by_casting_assistant(self):
        head = {"Authorization": self.casting_assistant}
        res = self.client().get(
            '/movies', headers=head)
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_e_get_movies_by_casting_director(self):
        head = {"Authorization": self.casting_director}
        res = self.client().get(
            '/movies', headers=head)
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_f_get_movies_by_executive_director(self):
        head = {"Authorization": self.executive_director}
        res = self.client().get(
            '/movies', headers=head)
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_g_add_actor_by_casting_assistant(self):
        json_data = {
                "name": "Bill", "age": 27,
                "gender": "female"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.casting_assistant)]
        res = self.client().post('/actors', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_h_add_actor_by_casting_director(self):
        json_data = {
                "name": "Bill", "age": 27,
                "gender": "female"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.casting_director)]
        res = self.client().post('/actors', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_i_add_actor_by_executive_director(self):
        json_data = {
                "name": "Bill", "age": 27,
                "gender": "female"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]
        res = self.client().post('/actors', json=json_data, headers=head)
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_j_add_movie_by_casting_assistant(self):
        json_data = {
                    "title": "Yourmovie",
                    "release_date": "11/11/2011"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.casting_assistant)]
        res = self.client().post('/movies', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_k_add_movie_by_casting_director(self):
        json_data = {
                    "title": "Yourmovie",
                    "release_date": "11/11/2011"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.casting_director)]
        res = self.client().post('/movies', json=json_data, headers=head)
        data = res.json
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_l_add_movie_by_executive_director(self):
        json_data = {
                    "title": "Yourmovie",
                    "release_date": "11/11/2011"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]
        res = self.client().post('/movies', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_m_add_actor_to_movie_by_casting_assistant(self):
        json_data = {"movie_id": 3, "actor_id": 3}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.casting_assistant)]
        res = self.client().post('/movies/cast', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_n_add_actor_to_movie_by_casting_director(self):
        json_data = {"movie_id": 3, "actor_id": 3}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.casting_director)]
        res = self.client().post('/movies/cast', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_o_add_actor_to_movie_by_executive_director(self):
        json_data = {"movie_id": 3, "actor_id": 4}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]
        res = self.client().post('/movies/cast', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_p_edit_actor_by_casting_assistant(self):
        json_data = {
                    "name": "will",
                    "age": 53,
                    "gender": "female"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.casting_assistant)]
        res = self.client().patch('/actors/3', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_q_edit_actor_by_casting_director(self):
        json_data = {
                    "name": "will",
                    "age": 53,
                    "gender": "female"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.casting_director)]
        res = self.client().patch('/actors/3', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_r_edit_actor_by_executive_director(self):
        json_data = {
                    "name": "will",
                    "age": 53,
                    "gender": "female"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]
        res = self.client().patch('/actors/4', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_s_edit_movie_by_casting_assistant(self):
        json_data = {
                    "title": "will",
                    "release_date": "2/2/2002"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.casting_assistant)]
        res = self.client().patch('/movies/3', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_t_edit_movie_by_casting_director(self):
        json_data = {
                    "title": "will",
                    "release_date": "2/2/2002"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.casting_director)]
        res = self.client().patch('/movies/3', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_u_edit_movie_by_executive_director(self):
        json_data = {
                    "title": "will",
                    "release_date": "2/2/2002"}
        head = [
                ('Content-Type', 'application/json'),
                ('Authorization', self.executive_director)]
        res = self.client().patch('/movies/3', json=json_data, headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_v_delete_actor_from_movie_by_casting_assistant(self):
        head = {"Authorization": self.casting_assistant}
        res = self.client().delete('/movies/cast?actorid=3&movieid=3',
                                   headers=head)
        data = res.json

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_w_delete_actor_from_movie_by_casting_director(self):
        head = {"Authorization": self.casting_director}
        res = self.client().delete('/movies/cast?actorid=3&movieid=3',
                                   headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_x_delete_actor_from_movie_by_executive_director(self):
        head = {"Authorization": self.executive_director}
        res = self.client().delete('/movies/cast?actorid=4&movieid=3',
                                   headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_y_delete_actor_by_casting_assistant(self):
        head = {"Authorization": self.casting_assistant}
        res = self.client().delete(
            '/actors/3', headers=head)
        data = res.json
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_z_delete_actor_by_casting_director(self):
        head = {"Authorization": self.casting_director}
        res = self.client().delete(
            '/actors/3', headers=head)
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_za_delete_actor_by_executive_director(self):
        head = {"Authorization": self.executive_director}
        res = self.client().delete(
            '/actors/4', headers=head)
        data = res.json
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_zb_delete_movie_by_casting_assistant(self):
        head = {"Authorization": self.casting_assistant}
        res = self.client().delete(
            '/movies/3', headers=head)
        data = res.json

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_zc_delete_movie_by_casting_director(self):
        head = {"Authorization": self.casting_director}
        res = self.client().delete(
            '/movies/3', headers=head)
        data = res.json

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_zd_delete_movie_by_executive_director(self):
        head = {"Authorization": self.executive_director}
        res = self.client().delete(
            '/movies/3', headers=head)
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


if __name__ == "__main__":
    unittest.main()
