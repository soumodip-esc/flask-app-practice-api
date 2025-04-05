from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask App
app = Flask(__name__)

# Database Configuration (Update with your credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:soumo@127.0.0.1:3306/project_practice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# Define Database Model (Matches your table structure)
class Music(db.Model):
    __tablename__ = 'music_table'  # Fix: Match your actual MySQL table name
    
    id = db.Column(db.Integer, primary_key=True)
    sad_music = db.Column(db.String(50))
    romantic_music = db.Column(db.String(50))
    party_music = db.Column(db.String(50))
    happy_music = db.Column(db.String(50))
    personal_fav = db.Column(db.String(50))
    native_music = db.Column(db.String(50))
    classical_music = db.Column(db.String(50))
    workout_music = db.Column(db.String(50))
    rock_music = db.Column(db.String(50))
    rap_music = db.Column(db.String(50))
    pop_music = db.Column(db.String(50))
    jazz_music = db.Column(db.String(50))
    motivaton_music = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "sad_music": self.sad_music,
            "romantic_music": self.romantic_music,
            "party_music": self.party_music,
            "happy_music": self.happy_music,
            "personal_fav": self.personal_fav,  
            "native_music": self.native_music,
            "classical_music": self.classical_music,
            "workout_music": self.workout_music,
            "rock_music": self.rock_music,
            "rap_music": self.rap_music,
            "pop_music": self.pop_music,
            "jazz_music": self.jazz_music,
            "motivaton_music": self.motivaton_music,
        }

# Route to Fetch All Songs
@app.route('/songs', methods=['GET'])
def get_songs():
    songs = Music.query.all()
    return jsonify([song.to_dict() for song in songs])  #  Added jsonify()

# Route to Fetch Songs by Genre
@app.route('/songs/<genre>', methods=['GET'])
def get_songs_by_genre(genre):
    allowed_genres = [
        "sad_music", "romantic_music", "party_music", "happy_music", "personal_fav", 
        "native_music", "classical_music", "workout_music", "rock_music", "rap_music", 
        "pop_music", "jazz_music", "motivaton_music"
    ]
    
    if genre not in allowed_genres:
        return jsonify({"error": "Invalid genre"}), 400  #  Added jsonify()

    songs = Music.query.with_entities(getattr(Music, genre)).filter(getattr(Music, genre).isnot(None)).all()
    
    return jsonify({genre: [song[0] for song in songs]})  #  Added jsonify()

# Run Flask App
if __name__ == '__main__':
    print("Flask app is starting...")
    app.run(debug=True)
   