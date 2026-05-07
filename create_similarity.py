import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pickle.load(open("movies.pkl", "rb"))

# Reduce size (important for performance)
movies = movies.head(1000)

# Fix missing values
movies['tags'] = movies['tags'].fillna('')

# Convert text to numbers
cv = CountVectorizer(max_features=2000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# Create similarity matrix
similarity = cosine_similarity(vectors)

# Save file
pickle.dump(similarity, open("similarity.pkl", "wb"))

print("similarity.pkl created successfully!")