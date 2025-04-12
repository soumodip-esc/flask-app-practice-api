from flask import Flask, jsonify, redirect ,request ,session, url_for  # ← Add redirect here
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from urllib.parse import urlencode
from spotify import spotify  # This imports the blueprint
import os
import time
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config.update(
    SESSION_COOKIE_SAMESITE="None",  # Allow cross-site cookies
    SESSION_COOKIE_SECURE=True       # Required for HTTPS (Render + Vercel)
)

# CORS(app)
CORS(app, origins=["https://music-recommender-app.vercel.app"], supports_credentials=True)

#Blueprint For Spotify
app.register_blueprint(spotify)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Soptify Configuration
# Spotify Token Gen SEC
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

#API KEY
app.secret_key = os.getenv("FLASK_SECRET_KEY") 

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
from flask import request, url_for

@app.route("/songs/<genre>", methods=["GET"])
def get_songs_by_genre(genre):
    allowed_genres = [
        "sad_music",
        "romantic_music",
        "party_music",
        "happy_music",
        "melancholy_music",
        "focus_music",
        "instrumental_music",
        "k_pop_music",
        "electronic_music",
        "rnb_music",
        "blues_music",
        "personal_fav",
        "native_music",
        "classical_music",
        "workout_music",
        "rock_music",
        "rap_music",
        "pop_music",
        "jazz_music",
        "motivaton_music",
        "trending_music",
        "latest_music",
        "top10_music",
        "hidden_gems_music",
        "developers_choice_music",
    ]

    if genre not in allowed_genres:
        return jsonify({"error": "Invalid genre"}), 400

    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))

    genre_column = getattr(Music, genre)
    total_items = Music.query.filter(genre_column.isnot(None)).count()

    songs = (
        Music.query.with_entities(genre_column)
        .filter(genre_column.isnot(None))
        .offset(offset)
        .limit(limit)
        .all()
    )

    results = [song[0] for song in songs]

    next_offset = offset + limit
    prev_offset = max(0, offset - limit)

    # Create full URLs for next and previous
    base_url = request.base_url
    next_url = f"{base_url}?offset={next_offset}&limit={limit}" if next_offset < total_items else None
    prev_url = f"{base_url}?offset={prev_offset}&limit={limit}" if offset > 0 else None

    return jsonify({
        "results": results,
        "next_offset": next_offset,
        "total_items": total_items,
        "has_more": next_offset < total_items,
        "length": len(results),
        "next": next_url,
        "prev": prev_url
    })


# Run the Flask app
if __name__ == "__main__":
    print("Flask app is starting...")
    app.run(debug=True)  
