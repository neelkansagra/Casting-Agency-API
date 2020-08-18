import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import exc
from models import db, Movies, Actors, Relation, setup_db
from auth import requires_auth, AuthError
from config import auth_config


def conv_actor_list_to_dict(actors_list):
    dict_of_actors = {}
    for actor in actors_list:
        if actor[0] not in dict_of_actors:
            if actor[1]:
                dict_of_actors[actor[0]] = [actor[1].title]
            else:
                dict_of_actors[actor[0]] = []
        else:
            dict_of_actors[actor[0]].append(actor[1].title)
    return dict_of_actors


def conv_movie_list_to_dict(movies_list):
    dict_of_movies = {}
    for movie in movies_list:
        if movie[0] not in dict_of_movies:
            if movie[1]:
                dict_of_movies[movie[0]] = [movie[1].name]
            else:
                dict_of_movies[movie[0]] = []
        else:
            dict_of_movies[movie[0]].append(movie[1].name)
    return dict_of_movies


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    # Uncomment this for authorization

    AUTH0_DOMAIN = auth_config["AUTH0_DOMAIN"]
    API_AUDIENCE = auth_config["API_AUDIENCE"]
    AUTH0_CLIENT_ID = auth_config["AUTH0_CLIENT_ID"]
    AUTH0_CALLBACK_URL = auth_config["AUTH0_CALLBACK_URL"]

    @app.route("/authorization", methods=["GET"])
    def generate_auth_url():
        url = f'https://{AUTH0_DOMAIN}/authorize' \
            f'?audience={API_AUDIENCE}' \
            f'&response_type=token&client_id=' \
            f'{AUTH0_CLIENT_ID}&redirect_uri=' \
            f'{AUTH0_CALLBACK_URL}'

        return jsonify({
            'url': url
        })

    @app.route("/")
    def home():
        message = "Welcome to my Casting Agency API"
        endpoint = ("GET /actors,GET /movies, POST /actors, "
                    "POST /movies, POST /movies/cast, DELETE /actors/id, "
                    "DELETE /movies/id, DELETE /movies/cast,"
                    "PATCH /movies/id, PATCH /actors/id")
        note = "Make sure you have permission to access these endpoints"
        return jsonify({
            "message": message,
            "available_endpoints": endpoint,
            "note": note,
            "success": True
        })

    @app.route("/actors")
    @requires_auth('get:actors')
    def get_actors(payload):
        list_of_actors = db.session.query(Actors, Movies).outerjoin(
            Relation, Relation.actor_id == Actors.id).outerjoin(
            Movies, Relation.movie_id == Movies.id).order_by(Actors.id).all()
        dict_of_actors = conv_actor_list_to_dict(list_of_actors)
        list_of_actors = [actor.format(dict_of_actors[actor])
                          for actor in dict_of_actors]
        return jsonify({
            "actors": list_of_actors,
            "success": True
        })

    @app.route("/movies")
    @requires_auth('get:movies')
    def get_movies(payload):
        list_of_movies = db.session.query(Movies, Actors).outerjoin(
            Relation, Relation.movie_id == Movies.id).outerjoin(
            Actors, Relation.actor_id == Actors.id).order_by(Movies.id).all()
        # print(list_of_movies)
        dict_of_movies = conv_movie_list_to_dict(list_of_movies)
        list_of_movies = [movie.format(dict_of_movies[movie])
                          for movie in dict_of_movies]
        return jsonify({
            "movies": list_of_movies,
            "success": True
        })

    @app.route("/actors", methods=["POST"])
    @requires_auth('post:actors')
    def add_actor(payload):
        try:
            name = request.get_json()['name']
            age = request.get_json()['age']
            gender = request.get_json()['gender']
            actor = Actors(name=name, age=age, gender=gender)
            actor.insert()
        except:
            Actors.rollback()
            abort(422)
        return jsonify({
            "name": name,
            "age": age,
            "gender": gender,
            "success": True
        })

    @app.route("/movies", methods=["POST"])
    @requires_auth('post:movies')
    def add_movie(payload):
        try:
            title = request.get_json()['title']
            release_date = request.get_json()['release_date']
            movie = Movies(title=title, release_date=release_date)
            movie.insert()
        except:
            Movies.rollback()
            abort(422)

        return jsonify({
            "title": title,
            "release_date": release_date,
            "success": True
        })

    @app.route("/movies/cast", methods=["POST"])
    @requires_auth('post:actor_to_movie')
    def add_actor_to_movie(payload):
        try:
            movie_id = request.get_json()["movie_id"]
            actor_id = request.get_json()["actor_id"]
            # print("movie" ,movie_id)
            # print("actor",actor_id)
            relation = Relation(movie_id=movie_id, actor_id=actor_id)
            relation.insert()

        except exc.IntegrityError:
            Relation.rollback()
            # print(sys.exc_info())
            abort(409)
        except:
            Relation.rollback()
            # print(sys.exc_info())
            abort(422)
        return jsonify({
            "movie_id": movie_id,
            "actor_id": actor_id,
            "success": True
        })

    @app.route("/actors/<id>", methods=["DELETE"])
    @requires_auth('delete:actor')
    def remove_actor(payload, id):

        relation = Relation.query.filter(Relation.actor_id == id).delete()
        actor = Actors.query.filter(Actors.id == id).one_or_none()
        if actor:
            actor.delete()
        else:
            Actors.rollback()
            # print(sys.exc_info())
            abort(404)

        return jsonify({
            "success": True,
            "actor_id": id
        })

    @app.route("/movies/<id>", methods=["DELETE"])
    @requires_auth('delete:movie')
    def remove_movie(payload, id):
        relation = Relation.query.filter(Relation.movie_id == id).delete()
        movie = Movies.query.filter(Movies.id == id).one_or_none()
        if movie:
            movie.delete()
        else:
            Movies.rollback()
            # print(sys.exc_info())
            abort(404)

        return jsonify({
            "success": True,
            "movie_id": id
        })

    @app.route("/movies/cast", methods=["DELETE"])
    @requires_auth('delete:actor_from_movie')
    def remove_actor_from_movie(payload):
        aid = request.args.get('actorid', None, int)
        mid = request.args.get('movieid', None, int)
        if aid is None or mid is None:
            abort(404)
        relation = Relation.query.filter(
            Relation.actor_id == aid and
            Relation.movie_id == mid).one_or_none()
        if relation:
            relation.delete()
        else:
            Relation.rollback()
            # print(sys.exc_info())

            abort(404)

        return jsonify({
            "success": True,
            "actor_id": aid,
            "movie_id": mid
        })

    @app.route("/actors/<id>", methods=["PATCH"])
    @requires_auth('patch:actor')
    def edit_actor(payload, id):
        ans = Actors.query.filter(Actors.id == id).one_or_none()
        # print(ans)
        if ans is None:
            abort(404)
        try:
            name = ""
            age = ""
            gender = ""
            if 'name' in request.get_json():
                name = request.get_json()['name']
                ans.name = name
            if 'age' in request.get_json():
                age = request.get_json()['age']
                ans.age = age
            if 'gender' in request.get_json():
                gender = request.get_json()['gender']
                ans.gender = gender
            name = ans.name
            age = ans.age
            gender = ans.gender
            Actors.commit()
        except:
            Actors.rollback()
            abort(422)
        return jsonify({
            "success": True,
            "name": name,
            "age": age,
            "gender": gender
        })

    @app.route("/movies/<id>", methods=["PATCH"])
    @requires_auth('patch:movie')
    def edit_movie(payload, id):
        ans = Movies.query.filter(Movies.id == id).one_or_none()
        if ans is None:
            abort(404)
        try:
            title = ""
            release_date = ""
            if 'title' in request.get_json():
                title = request.get_json()['title']
                ans.title = title
            if 'release_date' in request.get_json():
                release_date = request.get_json()['release_date']
                ans.release_date = release_date
            title = ans.title
            release_date = ans.release_date
            Movies.commit()
        except:
            Movies.rollback()
            abort(422)
        return jsonify({
            "success": True,
            "title": title,
            "release_date": release_date
        })

    @app.errorhandler(404)
    def error_handler_404(error):
        return jsonify({
            "success": False,
            "message": "Resource not found",
            "error_code": 404
        }), 404

    @app.errorhandler(422)
    def error_handler_422(error):
        return jsonify({
            "success": False,
            "message": "Request unprocessable",
            "error_code": 422
        }), 422

    @app.errorhandler(409)
    def error_handler_409(error):
        return jsonify({
            "success": False,
            "message": "Resource conflict ",
            "error_code": 409
        }), 409

    @app.errorhandler(AuthError)
    def auth_error_handler(error):
        return jsonify({
            "success": False,
            "message": error.error['description'],
            "error_code": error.status_code
        }), error.status_code

    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
