from models import db, User, Movie

class DataManager():
    """The class that manages the database information"""
    def create_user(self, name):
        """Creates a new user"""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_users(self):
        """Returns a list of all registered users"""
        users = User.query.all()
        return users

    def get_movies(self, user_id):
        """Returns a list of all movies for a user with the given id"""
        movies = Movie.query.filter_by(user_id=user_id).all()
        return movies

    def add_movie(self, movie: Movie):
        """Adds a movie to the database expects that is already a Movie object, created with the info from the app.py"""
        if not isinstance(movie, Movie):
            raise TypeError('Movie must be of type Movie')
        db.session.add(movie)
        db.session.commit()
        return f"{movie} Added Successfully"

    def update_movie(self, movie_id, new_title):
        """Updates a movie with the given id, if it doesn't exist in the database returns None"""
        movie = db.session.get(Movie, movie_id)
        if movie:
            movie.title = new_title
            db.session.commit()
            return movie
        return None

    def delete_movie(self, movie_id):
        """Deletes a movie from the database, Returns TRue if movie is there and it deletes successfully,
        otherwise returns False"""
        movie = db.session.get(Movie, movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False