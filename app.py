from urllib import request

from flask import Flask, render_template, redirect, request, url_for
from data_manager import DataManager
from models import Movie, User, db
import requests
from sqlalchemy.exc import IntegrityError, NoResultFound

import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = "https://www.omdbapi.com/?"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

data_manager = DataManager()

@app.route('/', methods=['GET'])
def index():
    """The home page of your application. Show a list of all registered users and a form for adding new users."""
    users = data_manager.get_users()
    return render_template("index.html", users=users) # for now add a template for a home.html


@app.route('/users', methods=['POST'])
def create_user():
    """When the user submits the “add user” form, a POST request is made.
    The server receives the new user info, adds it to the database, then redirects back to '/'"""
    new_user = request.form.get('name')
    data_manager.create_user(new_user)
    return redirect(url_for('index'))#only temporarily returning a string fix later with a jinja template

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):
    """When you click on a user-name, the app retrieves that user’s list of favorite movies and displays it."""
    user = data_manager.get_user(user_id)
    user_movies = data_manager.get_movies(user_id)
    message = request.args.get('message')

    return render_template('user.html', user_id=user_id, movies=user_movies, user=user, message=message)

@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Add a new movie to a user’s list of favorite movies."""
    title = request.form.get('title')
    try:
        response = requests.get(f"{API_URL}apikey={API_KEY}&t={title}")
        response.raise_for_status()
        movie_data = response.json()
    except requests.exceptions.RequestException as req_err:
        return f"Error fetching products: {req_err}"

    if movie_data.get("Response") == "False":
        return f"{title} is not available"

    try:
        movie_title = movie_data["Title"]
    except KeyError as error:
        return f"{title} not found due to missing key: {error}"

    try:
        year = int(movie_data["Year"])
    except ValueError:
        return "Invalid format from API"

    try:
        director = movie_data["Director"]
        poster = movie_data["Poster"]
        user_id = user_id
    except KeyError:
        return f"Information unavailable from API"




    movie = Movie(
        title=movie_title,
        director=director,
        year=year,
        poster_url=poster,
        user_id=user_id
        )
    data_manager.add_movie(movie)
    return redirect(url_for('user_movies', user_id=user_id)) #for now returning to home

@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Modify the title of a specific movie in a user’s list, without depending on OMDb for corrections."""
    old_title = data_manager.get_movie(user_id, movie_id).title
    new_title = request.form.get('title')
    data_manager.update_movie(movie_id, new_title)
    message = f"{old_title} was updated to {new_title}"

    return redirect(url_for('user_movies', user_id=user_id, message=message))

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Remove a specific movie from a user’s favorite movie list."""
    movie = data_manager.get_movie(user_id, movie_id)
    data_manager.delete_movie(movie_id)

    message =f"{movie.title} sucessdully removed" # add this to the html template, just figuring out how to do it
    return redirect(url_for('user_movies', user_id=user_id, message=message))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def handle_unexpected_error(e):
    app.logger.error(f"Unhandled Exception: {e}")
    return render_template('500.html', error=str(e)), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)