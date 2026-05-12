import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv("movies.csv")

# Fill missing
movies.fillna("", inplace=True)

# Create tags (only overview used)
movies["tags"] = movies["overview"]

# Convert to vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies["tags"]).toarray()

# Similarity
similarity = cosine_similarity(vectors)

# Save files
pickle.dump(movies, open("movies.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))

print("Model created successfully")

#this is first project of ml project