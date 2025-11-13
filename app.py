from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "3d266294"  # your OMDb API key


@app.route("/", methods=["GET", "POST"])
def home():
    genre = request.args.get("genre")
    movie_name = request.args.get("movie")

    movies = []
    message = None

    # Case 1: User selects a genre only
    if genre and not movie_name:
        url = f"http://www.omdbapi.com/?s={genre}&type=movie&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data.get("Response") == "True":
            movies = data.get("Search", [])
            message = f"🎬 Popular {genre} Movies"
        else:
            message = "No movies found for this genre."

    # Case 2: User enters a movie name (search similar)
    elif movie_name:
        url = f"http://www.omdbapi.com/?s={movie_name}&type=movie&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data.get("Response") == "True":
            movies = data.get("Search", [])
            message = f"🎥 Movies similar to '{movie_name}'"
        else:
            message = f"❌ No similar movies found for '{movie_name}'. Try another!"

    # Case 3: No input yet
    else:
        message = "🔎 Select a genre to get started!"

    return render_template("index.html", movies=movies, message=message, genre=genre)


if __name__ == "__main__":
    app.run(debug=True)
