**🎬 IMDB Movie Recommender System**
A Flask-based machine learning web application that recommends similar movies based on user input using the IMDB Movie Dataset. It also fetches movie posters using the TMDB API.

**🚀 Live Demo**
If deployed on Render:(https://movie-recommender-4-71o3.onrender.com/)

**📌 Features**
🎯 Movie recommendation based on content similarity
🧠 Machine Learning (Cosine Similarity + CountVectorizer)
🎬 Movie poster fetching using TMDB API
🌐 Web interface using Flask
⚡ Fast and lightweight deployment (Render ready)

**🧠 How It Works**
Dataset is loaded (IMDB-Movie-Data.csv)
Movie description + genre are combined into "tags"
Text is converted into vectors using CountVectorizer
Similarity between movies is calculated using Cosine Similarity
Top 5 similar movies are 

**🏗️ Tech Stack**
Python 🐍
Flask 🌐
Pandas 📊
Scikit-learn 🤖
Requests 🌍
HTML/CSS 🎨

**📂 Project Structure**
movie recommender/
│
├── app.py
├── IMDB-Movie-Data.csv
├── requirements.txt
├── templates/
│     └── index.html
├── static/ (optional)
└── README.md

**⚙️ Installation & Setup**
1️⃣ Clone the repository
git clone
https://github.com/imsujit98/movie-recommender
cd movie-recommender
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Run the project locally
python app.py

Then open:

http://127.0.0.1:5000
🔑 API Setup (TMDB)

You need a TMDB API key:

👉 https://www.themoviedb.org/settings/api

Replace in app.py:

API_KEY = "00400f0ba8fc98a9861cb3ce21e0344d"

**🚀 Deployment (Render)**
Build Command:
pip install -r requirements.txt
Start Command:
gunicorn app:app

**📊 Dataset Used**
IMDB Movie Dataset (CSV)
Contains:
Title
Genre
Description
Ratings

**🧠 Machine Learning Model**
Feature Extraction: CountVectorizer
Similarity Metric: Cosine Similarity
Approach: Content-Based Filtering

**📸 Output Example**
User input: Avtar
Output:
Recommended Movies:
- Avengers
- Interstellar
- Titanic
- Inception
- The Martian
- 
⚠️ Notes
First run may take time due to model building
Keep dataset size limited for Render free tier
Ensure stable internet for poster fetching

**👨‍💻 Author**
Developed by: Sujit Mandal
Project Type: Machine Learning + Flask Web App

**📜 License**
This project is open-source and free to use for learning purposes.

