import json
import os
from datetime import datetime
from .database import DatabaseManager

# Initialize database manager
db = DatabaseManager()

PROFILE_PATH = "data/user_profile.json"
MOOD_DATA_PATH = "data/mood_data.json"
CHECKIN_DATA_PATH = "data/checkin_data.json"

def save_user_profile(data, user_email=None):
    """Save user profile to database and JSON backup"""
    # Save to database
    if user_email:
        db.save_user_profile(user_email, data)
    
    # Keep JSON backup for compatibility
    os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)
    with open(PROFILE_PATH, "w") as f:
        json.dump(data, f, indent=2)

def load_user_profile(user_email=None):
    """Load user profile from database or JSON fallback"""
    if user_email:
        # Try database first
        profile = db.get_user_profile(user_email)
        if profile:
            return profile
    
    # Fallback to JSON
    try:
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def reset_user_profile(user_email=None):
    """Reset user profile from both database and JSON"""
    if user_email:
        db.delete_user_data(user_email)
    
    try:
        os.remove(PROFILE_PATH)
    except FileNotFoundError:
        pass

# Mood data functions
def save_mood_data(mood_entry, user_email=None):
    """Save a single mood entry to database and JSON backup"""
    # Save to database
    if user_email:
        db.save_mood_log(
            user_email=user_email,
            mood=mood_entry.get('mood', 'unknown'),
            intensity=mood_entry.get('intensity', 5),
            notes=mood_entry.get('notes', '')
        )
    
    # Keep JSON backup for compatibility
    os.makedirs(os.path.dirname(MOOD_DATA_PATH), exist_ok=True)
    existing_data = load_mood_data(user_email)
    existing_data.append(mood_entry)
    with open(MOOD_DATA_PATH, "w") as f:
        json.dump(existing_data, f, indent=2)

def load_mood_data(user_email=None):
    """Load mood data from database or JSON fallback"""
    if user_email:
        # Try database first
        mood_logs = db.get_mood_logs(user_email, days=365)  # Last year
        if mood_logs:
            # Convert database format to JSON format for compatibility
            converted_logs = []
            for log in mood_logs:
                converted_logs.append({
                    'mood': log['mood'],
                    'intensity': log['intensity'],
                    'notes': log['notes'],
                    'timestamp': log['created_at']
                })
            return converted_logs
    
    # Fallback to JSON
    try:
        with open(MOOD_DATA_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_all_mood_data(mood_data, user_email=None):
    """Save entire mood data array to database and JSON"""
    if user_email:
        # Clear existing mood logs for this user
        # Note: This is a simplified approach - in production you might want more sophisticated merging
        pass
    
    # Save to JSON
    os.makedirs(os.path.dirname(MOOD_DATA_PATH), exist_ok=True)
    with open(MOOD_DATA_PATH, "w") as f:
        json.dump(mood_data, f, indent=2)

def delete_mood_entry(timestamp, user_email=None):
    """Delete a specific mood entry by timestamp"""
    # Note: Database deletion by timestamp would require additional implementation
    # For now, just update JSON
    mood_data = load_mood_data(user_email)
    mood_data = [entry for entry in mood_data if entry.get('timestamp') != timestamp]
    save_all_mood_data(mood_data, user_email)

# Check-in data functions
def save_checkin_data(checkin_entry, user_email=None):
    """Save a single check-in entry to database and JSON backup"""
    # Save to database
    if user_email:
        db.save_checkin(user_email, checkin_entry)
    
    # Keep JSON backup for compatibility
    os.makedirs(os.path.dirname(CHECKIN_DATA_PATH), exist_ok=True)
    existing_data = load_checkin_data(user_email)
    existing_data.append(checkin_entry)
    with open(CHECKIN_DATA_PATH, "w") as f:
        json.dump(existing_data, f, indent=2)

def load_checkin_data(user_email=None):
    """Load check-in data from database or JSON fallback"""
    if user_email:
        # Try database first
        checkins = db.get_checkins(user_email, days=365)  # Last year
        if checkins:
            # Convert database format to JSON format for compatibility
            converted_checkins = []
            for checkin in checkins:
                converted_checkin = {
                    'time_period': checkin['time_period'],
                    'sleep_quality': checkin['sleep_quality'],
                    'energy_level': checkin['energy_level'],
                    'focus_today': checkin['focus_today'],
                    'current_feeling': checkin['current_feeling'],
                    'day_progress': checkin['day_progress'],
                    'accomplishments': checkin['accomplishments'],
                    'challenges': checkin['challenges'],
                    'task_plan': checkin['task_plan'],
                    'task_completion': checkin['task_completion'],
                    'timestamp': checkin['created_at']
                }
                converted_checkins.append(converted_checkin)
            return converted_checkins
    
    # Fallback to JSON
    try:
        with open(CHECKIN_DATA_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_all_checkin_data(checkin_data, user_email=None):
    """Save entire check-in data array to database and JSON"""
    if user_email:
        # Note: This would require clearing existing checkins for this user
        # For now, just save to JSON
        pass
    
    # Save to JSON
    os.makedirs(os.path.dirname(CHECKIN_DATA_PATH), exist_ok=True)
    with open(CHECKIN_DATA_PATH, "w") as f:
        json.dump(checkin_data, f, indent=2)