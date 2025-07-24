from urllib import request

from flask import Flask, render_template, redirect, request
from data_manager import DataManager
from models import Movie, User, db
import requests

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

@app.route('/')
def home():
    """The home page of your application. Show a list of all registered users and a form for adding new users."""
    return "Welcome to MoviWeb App!" # for now add a template for a home.html

@app.route('/users', methods=['POST'])
def users():
    """When the user submits the “add user” form, a POST request is made.
    The server receives the new user info, adds it to the database, then redirects back to '/'"""
    all_users = data_manager.get_users()
    return str(all_users) #only temporarily returning a string fix later with a jinja template

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):
    """When you click on a user-name, the app retrieves that user’s list of favorite movies and displays it."""
    user_movies = data_manager.get_movies(user_id)
    return str(user_movies) #add template here for user page

@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Add a new movie to a user’s list of favorite movies."""
    title = request.form.get['title']
    try:
        response = requests.get(f"{API_URL}apikey={API_KEY}&t={title}")
        response.raise_for_status()
        movie_data = response.json()

        if movie_data.get("Response") == "False":
            return f"{title} is not available"

        movie_title = movie_data["Title"]
        year = movie_data["Year"]
        director = movie_data["Director"]
        poster = movie_data["Poster"]

    except requests.exceptions.RequestException as req_err:
        return f"Error fetching products: {req_err}"

    except KeyError as error:
        return f"{title} not found due to missing key: {error}"

    movie = Movie(movie_title, director, year, poster)
    data_manager.add_movie(movie)
    return redirect("/") #for now returning to home

@app.route('/users/<int:user_id>/movies/<int:movie_id>', methods=['POST'])
def update_movie(user_id, movie_id):
    """Modify the title of a specific movie in a user’s list, without depending on OMDb for corrections."""
    data_manager.update_movie(user_id, movie_id)
    movie = data_manager.get_movie(user_id, movie_id)
    print(f"{movie} sucessdully added") #add this to the html template somehow
    return redirect("/")

@app.route('/users/<int:user_id>/movies/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Remove a specific movie from a user’s favorite movie list."""
    data_manager.delete_movie(movie_id)
    movie = data_manager.get_movie(user_id, movie_id)
    print(f"{movie} sucessdully removed") # add this to the html template, just figuring out how to do it
    return redirect("/")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run()