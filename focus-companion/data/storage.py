import json
import os

PROFILE_PATH = "data/user_profile.json"

def save_user_profile(data):
    os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)
    with open(PROFILE_PATH, "w") as f:
        json.dump(data, f, indent=2)

def load_user_profile():
    try:
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def reset_user_profile():
    try:
        os.remove(PROFILE_PATH)
    except FileNotFoundError:
        pass