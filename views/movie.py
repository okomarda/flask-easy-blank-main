# здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки). сюда импортируются сервисы из пакета service
from flask_restx import Resource, Namespace
from flask import request
from setup_db import db
from models import Movie, MovieSchema

movie_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@movie_ns.route('/')
class MovieView(Resource):
    def get_all(self):
        movies = Movie.query.all()
        return movies_schema.dump(movies), 200

    def get_by_director(self):
        did = request.args.get('director_id')
        movies = db.session.query(Movie).filter(Movie.director_id == int(did))
        return movies_schema.dump(movies), 200

    def get_by_genre(self):
        gid = request.args.get('genre_id')
        movies = db.session.query(Movie).filter(Movie.genre_id == int(gid))
        return movies_schema.dump(movies), 200

    def get_by_year(self):
        year = request.args.get('year')
        movies = db.session.query(Movie).filter(Movie.year == year)
        return movies_schema.dump(movies), 200

    def post(self) :
        data = request.json
        new_movie = Movie(**data)
        db.session.add(new_movie)
        db.session.commit()
        return '', 201

@movie_ns.route ('/<int:mid>')
class MovieView (Resource):
    def get_mid(self, mid):
        movie = db.session.query(Movie).filter (Movie.id == mid)
        return movie_schema.dump(movie), 200

    def put(self, mid):
        movie = Movie.query.get (mid)
        if not movie:
            return "", 404
        req_json = request.json
        movie.name = req_json.get ('name')
        movie.title = req_json.get ('title')
        movie.description = req_json.get ('description')
        movie.trailer = req_json.get ('trailer')
        movie.year = req_json.get ('year')
        movie.rating = req_json.get ('rating')
        db.session.add (movie)
        db.session.commit()
        return "", 204

    def delete(self, mid):
        movie = Movie.query.get (mid)
        if not movie:
            return "", 404
        db.session.delete(movie)
        db.session.commit()
        return "", 204


