import os
import time
import requests
from flask import Flask, jsonify


app = Flask(__name__)

CLIENT_ID = os.getenv("b122c002e81948f1934fcdc254dfdbe1")
CLIENT_SECRET = os.getenv("7ab31e87bb824bdfb319c51c5e33d672")

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


if __name__ == "__main__":
    app.run(debug=True)
