from models import db, User, Movie

class DataManager():

    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_users(self):
        users = User.query.all()
        return users

    def get_movies(self, user_id):
        movies = Movie.query.filter_by(user_id=user_id).all()
        return movies

    def add_movie(self, movie):
        """assumes that the movie is already an movie object, created with the info from the app.py"""
        db.session.add(movie)
        db.session.commit()
        return f"{movie} Added Successfully"

    def update_movie(self, movie_id, new_title):
        movie = db.session.get(Movie, movie_id)
        if movie:
            movie.title = new_title
            db.session.commit()
            return movie
        return None

    def delete_movie(self, movie_id):
        movie = db.session.get(Movie, movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False