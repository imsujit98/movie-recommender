from flask import Flask, render_template, request
import pandas as pd
import pickle
import requests
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# -----------------------------
# LOAD DATASET (IMDB CSV)
# -----------------------------
movies = pd.read_csv("IMDB-Movie-Data.csv")

# Keep only required columns
movies = movies[['Title', 'Genre', 'Description']]

# Rename for convenience
movies.rename(columns={
    'Title': 'title',
    'Genre': 'genre',
    'Description': 'overview'
}, inplace=True)

# Fill missing values
movies['overview'] = movies['overview'].fillna('')

# -----------------------------
# CREATE TAGS (VERY IMPORTANT)
# -----------------------------
movies['tags'] = movies['overview'] + " " + movies['genre']

# Reduce size (Render safe)
movies = movies.head(1000)

# -----------------------------
# ML MODEL
# -----------------------------
cv = CountVectorizer(max_features=2000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

similarity = cosine_similarity(vectors)

# -----------------------------
# TMDB API
# -----------------------------
API_KEY = "00400f0ba8fc98a9861cb3ce21e0344d"


def fetch_poster(movie_name):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
        data = requests.get(url).json()

        if not data.get("results"):
            return "https://via.placeholder.com/300x450?text=No+Image"

        poster_path = data["results"][0]["poster_path"]

        if not poster_path:
            return "https://via.placeholder.com/300x450?text=No+Image"

        return "https://image.tmdb.org/t/p/w500/" + poster_path

    except:
        return "https://via.placeholder.com/300x450?text=No+Image"


# -----------------------------
# RECOMMENDER
# -----------------------------
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


# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html", movies=[], posters=[])


@app.route("/recommend", methods=["POST"])
def recommend_movies():

    movie = request.form.get("movie")

    if movie:
        names, posters = recommend(movie)
        return render_template("index.html", movies=names, posters=posters)

    return render_template("index.html", movies=[], posters=[])


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)