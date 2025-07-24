from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Class that defines a User for the database"""
    def __init__(self, id, name):
        self.id = id
        self.name = name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    movies = db.relationship('Movie', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name


class Movie(db.Model):
    """Class that defines a Movie for the database,
    information is gathered by an API and added to the object upon initialization"""
    def __init__(self, title, director, year, poster_url):
        self.title = title
        self.director = director
        self.year = year
        self.poster_url = poster_url


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return (f"<Movie {self.title}>"
                f"<Director {self.director}>"
                f"<Year {self.year}>")

