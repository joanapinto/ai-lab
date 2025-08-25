import json
import os
from datetime import datetime

PROFILE_PATH = "data/user_profile.json"
MOOD_DATA_PATH = "data/mood_data.json"
CHECKIN_DATA_PATH = "data/checkin_data.json"

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

# Mood data functions
def save_mood_data(mood_entry):
    """Save a single mood entry to the mood data file"""
    os.makedirs(os.path.dirname(MOOD_DATA_PATH), exist_ok=True)
    
    # Load existing data
    existing_data = load_mood_data()
    
    # Add new entry
    existing_data.append(mood_entry)
    
    # Save back to file
    with open(MOOD_DATA_PATH, "w") as f:
        json.dump(existing_data, f, indent=2)

def load_mood_data():
    """Load all mood data from file"""
    try:
        with open(MOOD_DATA_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_all_mood_data(mood_data):
    """Save entire mood data array to file"""
    os.makedirs(os.path.dirname(MOOD_DATA_PATH), exist_ok=True)
    with open(MOOD_DATA_PATH, "w") as f:
        json.dump(mood_data, f, indent=2)

def delete_mood_entry(timestamp):
    """Delete a specific mood entry by timestamp"""
    mood_data = load_mood_data()
    mood_data = [entry for entry in mood_data if entry.get('timestamp') != timestamp]
    save_all_mood_data(mood_data)

# Check-in data functions
def save_checkin_data(checkin_entry):
    """Save a single check-in entry to the check-in data file"""
    os.makedirs(os.path.dirname(CHECKIN_DATA_PATH), exist_ok=True)
    
    # Load existing data
    existing_data = load_checkin_data()
    
    # Add new entry
    existing_data.append(checkin_entry)
    
    # Save back to file
    with open(CHECKIN_DATA_PATH, "w") as f:
        json.dump(existing_data, f, indent=2)

def load_checkin_data():
    """Load all check-in data from file"""
    try:
        with open(CHECKIN_DATA_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_all_checkin_data(checkin_data):
    """Save entire check-in data array to file"""
    os.makedirs(os.path.dirname(CHECKIN_DATA_PATH), exist_ok=True)
    with open(CHECKIN_DATA_PATH, "w") as f:
        json.dump(checkin_data, f, indent=2)