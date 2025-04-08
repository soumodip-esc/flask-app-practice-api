from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
import time
import requests
#from spotify_token import get_token  

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Database
db = SQLAlchemy(app)

# Define Music Table Model
class Music(db.Model):
    __tablename__ = "music_table"

    id = db.Column(db.Integer, primary_key=True)
    sad_music = db.Column(db.String(100))
    romantic_music = db.Column(db.String(100))
    party_music = db.Column(db.String(100))
    happy_music = db.Column(db.String(100))
    melancholy_music = db.Column(db.String(100))
    focus_music = db.Column(db.String(100))
    instrumental_music = db.Column(db.String(100))
    k_pop_music = db.Column(db.String(100))
    electronic_music = db.Column(db.String(100))
    rnb_music = db.Column(db.String(100))
    blues_music = db.Column(db.String(100))
    personal_fav = db.Column(db.String(100))
    native_music = db.Column(db.String(100))
    classical_music = db.Column(db.String(100))
    workout_music = db.Column(db.String(100))
    rock_music = db.Column(db.String(100))
    rap_music = db.Column(db.String(100))
    pop_music = db.Column(db.String(100))
    jazz_music = db.Column(db.String(100))
    motivaton_music = db.Column(db.String(100))
    trending_music = db.Column(db.String(100))
    latest_music = db.Column(db.String(100))
    top10_music = db.Column(db.String(100))
    hidden_gems_music = db.Column(db.String(100))
    developers_choice_music = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "sad_music": self.sad_music,
            "romantic_music": self.romantic_music,
            "party_music": self.party_music,
            "happy_music": self.happy_music,
            "melancholy_music": self.melancholy_music,
            "focus_music": self.focus_music,
            "instrumental_music": self.instrumental_music,
            "k_pop_music": self.k_pop_music,
            "electronic_music": self.electronic_music,
            "rnb_music": self.rnb_music,
            "blues_music": self.blues_music,
            "personal_fav": self.personal_fav,
            "native_music": self.native_music,
            "classical_music": self.classical_music,
            "workout_music": self.workout_music,
            "rock_music": self.rock_music,
            "rap_music": self.rap_music,
            "pop_music": self.pop_music,
            "jazz_music": self.jazz_music,
            "motivaton_music": self.motivaton_music,
            "trending_music": self.trending_music,
            "latest_music": self.latest_music,
            "top10_music": self.top10_music,
            "hidden_gems_music": self.hidden_gems_music,
            "developers_choice_music": self.developers_choice_music,
        }

# Route to fetch all songs
@app.route("/songs", methods=["GET"])
def get_songs():
    songs = Music.query.all()
    return jsonify([song.to_dict() for song in songs])

# Route to fetch songs by genre
@app.route("/songs/<genre>", methods=["GET"])
def get_songs_by_genre(genre):
    allowed_genres = [
        "sad_music", "romantic_music", "party_music", "happy_music",
        "melancholy_music", "focus_music", "instrumental_music", "k_pop_music",
        "electronic_music", "rnb_music", "blues_music", "personal_fav",
        "native_music", "classical_music", "workout_music", "rock_music",
        "rap_music", "pop_music", "jazz_music", "motivaton_music",
        "trending_music", "latest_music", "top10_music",
        "hidden_gems_music", "developers_choice_music"
    ]

    if genre not in allowed_genres:
        return jsonify({"error": "Invalid genre"}), 400

    songs = (
        Music.query.with_entities(getattr(Music, genre))
        .filter(getattr(Music, genre).isnot(None))
        .all()
    )
    return jsonify({genre: [song[0] for song in songs]})


# Spotify Token Gen SEC
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Globals for caching token
access_token = None
expires_at = 0


def refresh_token():
    global access_token, expires_at
    print("Refreshing token...")

    auth_response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        headers={
            "Authorization": "Basic "
            + (f"{CLIENT_ID}:{CLIENT_SECRET}").encode("ascii").decode("latin1")
        },
        auth=(CLIENT_ID, CLIENT_SECRET),
    )

    if auth_response.status_code != 200:
        raise Exception("Failed to get token: " + auth_response.text)

    token_data = auth_response.json()
    access_token = token_data["access_token"]
    expires_in = token_data["expires_in"]  # Usually 3600 seconds
    expires_at = time.time() + expires_in - 60  # Refresh 1 minute before expiry

    print(f"New token: {access_token[:20]}...")


@app.route("/token")
def get_token():
    global access_token, expires_at
    if not access_token or time.time() > expires_at:
        refresh_token()
    return jsonify({"access_token": access_token})



# Run the Flask app
if __name__ == "__main__":
    print("Flask app is starting...")
    app.run(debug=True)


