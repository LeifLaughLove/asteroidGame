import requests
import os
from datetime import date
from dotenv import load_dotenv

    # This file handles the leaderboard functionality, when using a it connects to the server URL to either get top scores or post a score
    # for it to connect to a server, the SERVER_URL needs to be set in a .env file.
    # If SERVER_URL is not defined, it defaults to http://localhost:5000 for local use.

load_dotenv()
SERVER_URL = os.environ.get("SERVER_URL", "http://localhost:5000")

def post_score(name, score):
    payload = {
        "name": name,
        "score": score,
        "date": date.today().isoformat()
    }
    try:
        response = requests.post(f"{SERVER_URL}/submit-score", json=payload)
        if response.status_code == 201:
            print("Score submitted successfully!")
        else:
            print(f"Failed to submit score: {response.status_code}")
    except Exception as e:
        print(f"Error posting score: {e}")
        

def get_leaderboard():
    try:
        response = requests.get(f"{SERVER_URL}/get-leaderboard")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve leaderboard: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error retrieving leaderboard: {e}")
        return []