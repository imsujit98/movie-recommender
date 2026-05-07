from flask import Flask, render_template, request
import pickle
import requests
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load movie data
movies = pickle.load(open("movies.pkl", "rb"))

# Reduce dataset size for Render memory optimization
movies = movies.head(1000)

# Fill missing tags
movies['tags'] = movies['tags'].fillna('')

# Create vectors
cv = CountVectorizer(
    max_features=2000,
    stop_words='english'
)

vectors = cv.fit_transform(movies['tags']).toarray()

# Generate similarity matrix
similarity = cosine_similarity(vectors)

# TMDB API KEY
API_KEY = "00400f0ba8fc98a9861cb3ce21e0344d"


# Fetch poster function
def fetch_poster(movie_name):

    try:

        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"

        data = requests.get(url).json()

        poster_path = data['results'][0]['poster_path']

        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

        return full_path

    except:

        return "https://via.placeholder.com/300x450?text=No+Image"


# Recommendation function
def recommend(movie):

    movie = movie.lower()

    # Movie not found
    if movie not in movies['title'].str.lower().values:

        return [], []

    # Get movie index
    index = movies[movies['title'].str.lower() == movie].index[0]

    distances = similarity[index]

    # Get top 5 similar movies
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:

        movie_title = movies.iloc[i[0]].title

        recommended_movies.append(movie_title)

        poster = fetch_poster(movie_title)

        recommended_posters.append(poster)

    return recommended_movies, recommended_posters


# Home route
@app.route("/")
def home():

    return render_template(
        "index.html",
        movies=[],
        posters=[]
    )


# Recommend route
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


# Run app
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )