# spotify.py

from flask import Blueprint, redirect, request, session, jsonify
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Globals for caching token
access_token = None
expires_at = 0


spotify = Blueprint("spotify", __name__)

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/callback"

access_token_cache = {"access_token": None, "expires_at": 0}


def refresh_token():
    auth_response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET),
    )

    if auth_response.status_code != 200:
        raise Exception("Failed to get token: " + auth_response.text)

    token_data = auth_response.json()
    access_token_cache["access_token"] = token_data["access_token"]
    access_token_cache["expires_at"] = time.time() + token_data["expires_in"] - 60


@spotify.route("/token")
def get_token():
    if (
        not access_token_cache["access_token"]
        or time.time() > access_token_cache["expires_at"]
    ):
        refresh_token()
    return jsonify({"access_token": access_token_cache["access_token"]})


@spotify.route("/callback")
def callback():
    code = request.args.get("code") 

    if not code:
        return jsonify({
            "error": "Missing authorization code",
            "details": "Don't refresh this page. Start again from /login."
        }), 400

    print("Authorization code:", code)

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    response = requests.post("https://accounts.spotify.com/api/token", data=payload)
    if response.status_code != 200:
        return jsonify({
            "error": "Failed to obtain access token",
            "details": response.text
        }), 400

    token_data = response.json()
    session["access_token"] = token_data["access_token"]
    session["refresh_token"] = token_data.get("refresh_token")

    return redirect("/me")


@spotify.route("/me")
def get_profile():
    token = session.get("access_token")
    if not token:
        return jsonify({"error": "No access token in session"}), 401

    headers = {"Authorization": f"Bearer {token}"}

    profile_response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    if profile_response.status_code != 200:
        return (
            jsonify(
                {"error": "Failed to fetch profile", "details": profile_response.text}
            ),
            400,
        )

    playlists_response = requests.get(
        "https://api.spotify.com/v1/me/playlists", headers=headers
    )
    if playlists_response.status_code != 200:
        return (
            jsonify(
                {
                    "error": "Failed to fetch playlists",
                    "details": playlists_response.text,
                }
            ),
            400,
        )

    profile = profile_response.json()
    playlists = playlists_response.json()

    return jsonify(
        {
            "profile": {
                "display_name": profile.get("display_name"),
                "email": profile.get("email"),
                "image": profile["images"][0]["url"] if profile.get("images") else None,
            },
            "playlists": playlists,
        }
    )


@spotify.route("/create_playlist", methods=["POST"])
def create_playlist():
    token = session.get("access_token")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    profile = requests.get("https://api.spotify.com/v1/me", headers=headers).json()
    user_id = profile["id"]

    data = {
        "name": "OopsVincent’s Fire Playlist 🔥",
        "description": "Curated with chaotic love by Vincent",
        "public": False,
    }

    response = requests.post(
        f"https://api.spotify.com/v1/users/{user_id}/playlists",
        headers=headers,
        json=data,
    )

    return jsonify(response.json())

@spotify.route("/login")
def login():
    scopes = "user-read-private user-read-email playlist-read-private playlist-modify-private"
    auth_url = "https://accounts.spotify.com/authorize"
    query_params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "scope": scopes,
        "redirect_uri": REDIRECT_URI,
    }

    query_string = "&".join(f"{k}={requests.utils.quote(v)}" for k, v in query_params.items())
    return redirect(f"{auth_url}?{query_string}")
     


