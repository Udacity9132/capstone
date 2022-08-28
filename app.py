import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db_drop_and_create_all, Movie, Actor, db
from auth import AuthError, requires_auth

DATABASE_URL = os.environ['DATABASE_URL']

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = "Secret"
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):

      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, PUT, OPTIONS')

      return response
  
    # db_drop_and_create_all()

    # Landing Page 

    @app.route('/')
    def index():
        return render_template('index.html')


    # GET - Movies

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
      try:
          movies = Movie.query.all()
          return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
          }), 200
      except Exception:
          abort(500)

    # GET - Movies by id

    @app.route('/movies/<int:id>')
    @requires_auth('get:movies')
    def get_movies_by_id(payload, id):

        try:
            movie = Movie.query.get(id)

            if movie is None:
                abort(404)
        
            return jsonify({
              'success': True,
              'movie': movie.format()
            }), 200
        
        except Exception:
            abort(500)

    # POST - Movies

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        data = request.get_json()
        movie = Movie(
          title=data['title'],
          release_date=data['release_date']
        )

        if movie.title is None or movie.release_date is None:
          abort(400)

        try:
            movie.insert()

            return jsonify({
              'success': True,
              'movie': movie.format()
            }),200
        except Exception:
            abort(500)

    # PATCH - Movies

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, id):
        data = request.get_json()
        title = data.get('title', None)
        release_date = data.get('release_date', None)

        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            abort(404)
        
        if title is None or release_date is None:
            abort(400)
          
        movie.title = title
        movie.release_date = release_date

        try:
            movie.update()
            return jsonify({
              'sucess': True,
              'movie': movie.format()
            }), 200
        
        except Exception:
            abort(500)


    # DELETE - Movies

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):

        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            abort(404)
        
        try: 
            movie.delete()
            return jsonify({
              'success': True,
              'message': 'Movie deleted'
            }), 200
        
        except Exception: 
            db.session.rollback()
            abort(500)



    # GET - Actors

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):

        try:
            actors = Actor.query.all()
            return jsonify({
              'success': True,
              'actors': [actor.format() for actor in actors]
            }), 200
        
        except Exception:
          abort(500)

    # GET - Actors by id

    @app.route('/actors/<int:id>')
    @requires_auth('get:actors')
    def get_actor_by_id(payload, id):

        try:
            actor = Actor.query.get(id)

            if actor is None:
                abort(404)
        
            return jsonify({
              'success': True,
              'actor': actor.format()
            }), 200
        
        except Exception:
          abort(500)


    # POST - Actors

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):

        data = request.get_json()
        actor = Actor(
          name=data['name'],
          age=data['age'],
          gender=data['gender'],
          movie_id=data['movie_id']
        )

        if name is None or age is None or gender is None:
            abort (400)
        
        try: 
            actor.insert()

            return jsonify({
              'success': True,
              'actor': actor.format()
            }), 200
        
        except Exception:
            abort(500)


    # Patch - Actors

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actor(payload, id):

        data = request.get_json()
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        
        if name is None or age is None or gender is None:
            abort(400)

        actor.name = name
        actor.age = age
        actor.gender = gender

        try:
            actor.update()
            return jsonify({
              'success': True,
              'actor': actor.format()
            }), 200
        
        except Exception:
            abort(500)


    # DELETE - Actors

    @app.route('/actors', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            abort(404)
        
        try: 
            actor.delete()
            return jsonify({
              'success': True,
              'message': 'Actor deleted'
            }), 200
        
        except Exception:
            db.session.rollback()
            abort(500)




    # Error Handlers

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad request"
        }), 400

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
          "success": False,
          "error": 403,
          "message": "You have no permission to make this request"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
          "success": False,
          "error": 500,
          "message": "Internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(exception):
        response = jsonify(exception.error)
        response.status_code = exception.status_code
        return response


    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)