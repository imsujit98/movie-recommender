from flask import Flask, render_template, request
import pickle
import requests
import os

app = Flask(__name__)

# Load data
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# TMDB API KEY
API_KEY = "00400f0ba8fc98a9861cb3ce21e0344d"

# Fetch Poster
def fetch_poster(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
    data = requests.get(url).json()

    try:
        poster_path = data['results'][0]['poster_path']
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        return ""

# Recommend Function
def recommend(movie):
    movie = movie.lower()

    if movie not in movies['title'].str.lower().values:
        return [], []

    index = movies[movies['title'].str.lower() == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names = []
    posters = []

    for i in movie_list:
        title = movies.iloc[i[0]].title
        names.append(title)
        posters.append(fetch_poster(title))

    return names, posters

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Recommendation Route
@app.route("/recommend", methods=["POST"])
def recommend_movies():
    movie = request.form.get("movie")

    if movie:
        names, posters = recommend(movie)
        return render_template(
            "index.html",
            movies=names,
            posters=posters
        )

    return render_template(
        "index.html",
        movies=[],
        posters=[]
    )

# Run App
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)