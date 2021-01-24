import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth


# Create App
def create_app(test_config=None):
    
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers',
          'Content-Type, Authorization'
          )
        response.headers.add(
          'Access-Control-Allow-Methods',
          'GET, POST, PATCH, DELETE, OPTIONS'
          )
        return response

    @app.route("/", methods=["GET"])
    def start_page():
        movies = [movie.format() for movie in Movie.query.all()]
        return jsonify({
            "success": True,
            "message": "Its working!!! At least a bit...",
            "movies": movies
        })

    @app.route("/auth")
    def generate_auth_url():
        
        print("no auth. take preset")
        AUTH0_DOMAIN= "dev-t-4sg5-6.eu.auth0.com"
        API_AUDIENCE="agency"
        ALGORITHMS=['RS256']
        AUTH0_CLIENT_ID="DRQkvwQZrdvpBOs65wzGSz4pmxTps1tx"
        AUTH0_CALLBACK_URL="https://localhost:5000"
        
        url = f'https://{AUTH0_DOMAIN}/authorize' \
            f'?audience={API_AUDIENCE}' \
            f'&response_type=token&client_id=' \
            f'{AUTH0_CLIENT_ID}&redirect_uri=' \
            f'{AUTH0_CALLBACK_URL}'

        return jsonify({
            'auth_url': url
        })

    #Movie endpoints
  
    @app.route("/movies", methods=["GET"])
    @requires_auth("get:movies")
    def get_movies(payload):
        
        movies = [movie.format() for movie in Movie.query.all()]
        if movies is None:
            abort(404)

        return jsonify({
            "success": True,
            "movies": movies
        })

    @app.route("/movies", methods=["POST"])
    @requires_auth("post:movies")
    def post_movie(payload):
        body = request.get_json()
        check_keys={"title", "release_date","imdb_rating"}

        if body is None:
            abort(404)
        
        if not (body.keys()) >= check_keys:
            abort(422)

        title = body["title"]
        release_date = body["release_date"]
        imdb_rating = body["imdb_rating"]

        new_movie = Movie(title=title, release_date=release_date, imdb_rating=imdb_rating)
        new_movie.insert()

        return jsonify({
            "success": True,
            "message": "Whatever you add, Matrix is the best movie",
            "movies": [new_movie.format()]
        })

    @app.route("/movies/<int:movie_id>", methods=["PATCH"])
    @requires_auth("patch:movies")
    def update_movie(payload, movie_id):
        
        body = request.get_json()
        check_keys={"title", "release_date","imdb_rating"}
 
        if body is None:
            abort(404)
        
        if not (body.keys()) >= check_keys:
            abort(422)
    
        try:
            movie = Movie.query.get(movie_id)

            if movie is None:
                abort(404)

            movie.title = body["title"]
            movie.release_date = body["release_date"]
            movie.imdb_rating = body["imdb_rating"]
            movie.update()
            
            updated_movie = Movie.query.get(movie_id)
            
            return jsonify({
                "success": True,
                "movies": [updated_movie.format()]
            })

        except AuthError:
            abort(422)

    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    @requires_auth("delete:movies")
    def delete_movie(payload, movie_id):
        
        try:
            movie = Movie.query.get(movie_id)

            if movie is None:
                abort(404)
            
            deleted_movie = Movie.query.filter_by(id=movie_id).first()
            movie = Movie.query.get(movie_id).delete()

            return jsonify({
                "success": True,
                "delete": movie_id,
                "deleted_movie": [deleted_movie.format()]
            })
        
        except AuthError:
            abort(422)
            
    #Actors

    @app.route("/actors", methods=["GET"])
    @requires_auth("get:actors")
    def get_actors(payload):
        
        try:
            actors = [actor.format() for actor in Actor.query.all()]
            
            if actors is None:
                abort(404)

            return jsonify({
                "success": True,
                "actors": actors
            })

        except AuthError:
            abort(422)

    @app.route("/actors", methods=["POST"])
    @requires_auth("post:actors")
    def create_actor(payload):
        body = request.get_json()
        check_keys = {"name", "age", "gender"}
                
        if not (body.keys()) >= check_keys:
            abort(422)

        name = body["name"]
        age = body["age"]
        gender = body["gender"]

        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()

        return jsonify({
            "success": True,
            "actors": [actor.format()]
        })

    @app.route("/actors/<int:actor_id>", methods=["PATCH"])
    @requires_auth("patch:actors")
    def patch_actor(payload, actor_id):
        
        body = request.get_json()
        check_keys = {"name", "age", "gender"}

        if body is None:
            abort(404) 

        if not (body.keys()) >= check_keys:
            abort(422)

        try:
            actor = Actor.query.get(actor_id)

            if actor is None:
                abort(404)

            actor.name = body["name"]
            actor.age = body["age"]
            actor.gender = body["gender"]
            actor.update()
            
            updated_actor = Actor.query.get(actor_id)
            
            return jsonify({
                "success": True,
                "actor": [updated_actor.format()]
                })

        except AuthError:
            abort(422)


    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    @requires_auth("delete:actors")
    def delete_actor(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)
            if actor is None:
                abort(404)

            deleted_actor = Actor.query.filter_by(id=actor_id).first()
            Actor.query.get(actor_id).delete()
            
            return jsonify({
                "success": True,
                "deleted_actor": [deleted_actor.format()]
            })
        
        except AuthError:
            abort(422)
    
    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 422,
                        "message": "Unprocessable"
                    }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                        "success": False,
                        "error": 404,
                        "message": "Resource not found"
                    }), 404

    @app.errorhandler(403)
    def unauthorized(error):
        return jsonify({
                        "success": False,
                        "error": 403,
                        "message": "Forbidden"
                    }), 403

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
                        "success": False,
                        "error": 401,
                        "message": "Unauthorized Error"
                    }), 401

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                        "success": False,
                        "error": 400,
                        "message": "Bad Request"
                    }), 400

    @app.errorhandler(AuthError)
    def not_found(error):
        return jsonify({
                        "success": False,
                        "error": error.status_code,
                        "message": error.error["description"]
                    }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)