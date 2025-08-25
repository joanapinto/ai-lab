"""
Unit tests for the data storage system
Tests user profile, mood data, and check-in data storage functionality
"""

import unittest
import json
import os
import tempfile
import shutil
from datetime import datetime
from unittest.mock import patch, mock_open

# Add the parent directory to the path to import the storage module
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.storage import (
    save_user_profile, load_user_profile, reset_user_profile,
    save_mood_data, load_mood_data, save_all_mood_data, delete_mood_entry,
    save_checkin_data, load_checkin_data, save_all_checkin_data
)


class TestStorageSystem(unittest.TestCase):
    """Test cases for the storage system"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.original_profile_path = "data/user_profile.json"
        self.original_mood_path = "data/mood_data.json"
        self.original_checkin_path = "data/checkin_data.json"
        
        # Store original paths
        import data.storage as storage_module
        self.original_profile_path_value = storage_module.PROFILE_PATH
        self.original_mood_path_value = storage_module.MOOD_DATA_PATH
        self.original_checkin_path_value = storage_module.CHECKIN_DATA_PATH
        
        # Set test paths
        storage_module.PROFILE_PATH = os.path.join(self.test_dir, "user_profile.json")
        storage_module.MOOD_DATA_PATH = os.path.join(self.test_dir, "mood_data.json")
        storage_module.CHECKIN_DATA_PATH = os.path.join(self.test_dir, "checkin_data.json")
    
    def tearDown(self):
        """Clean up test environment"""
        # Restore original paths
        import data.storage as storage_module
        storage_module.PROFILE_PATH = self.original_profile_path_value
        storage_module.MOOD_DATA_PATH = self.original_mood_path_value
        storage_module.CHECKIN_DATA_PATH = self.original_checkin_path_value
        
        # Remove test directory
        shutil.rmtree(self.test_dir)
    
    def test_save_and_load_user_profile(self):
        """Test saving and loading user profile"""
        test_profile = {
            "goal": "Improve focus and productivity",
            "availability": "2-4 hours",
            "energy": "Good",
            "check_ins": "Yes",
            "tone": "Gentle & supportive",
            "situation": "Freelancer"
        }
        
        # Test saving profile
        save_user_profile(test_profile)
        
        # Test loading profile
        loaded_profile = load_user_profile()
        
        self.assertEqual(loaded_profile, test_profile)
        self.assertEqual(loaded_profile["goal"], "Improve focus and productivity")
        self.assertEqual(loaded_profile["tone"], "Gentle & supportive")
    
    def test_load_user_profile_empty(self):
        """Test loading user profile when file doesn't exist"""
        # Ensure no profile file exists
        import data.storage as storage_module
        if os.path.exists(storage_module.PROFILE_PATH):
            os.remove(storage_module.PROFILE_PATH)
        
        loaded_profile = load_user_profile()
        self.assertEqual(loaded_profile, {})
    
    def test_reset_user_profile(self):
        """Test resetting user profile"""
        test_profile = {"goal": "Test goal"}
        save_user_profile(test_profile)
        
        # Verify profile exists
        loaded_profile = load_user_profile()
        self.assertEqual(loaded_profile, test_profile)
        
        # Reset profile
        reset_user_profile()
        
        # Verify profile is gone
        loaded_profile = load_user_profile()
        self.assertEqual(loaded_profile, {})
    
    def test_save_and_load_mood_data(self):
        """Test saving and loading mood data"""
        test_mood_entry = {
            "timestamp": "2024-01-15T10:30:00",
            "mood": "😊 Happy",
            "intensity": 8,
            "note": "Feeling productive today!",
            "date": "2024-01-15",
            "time": "10:30"
        }
        
        # Test saving mood entry
        save_mood_data(test_mood_entry)
        
        # Test loading mood data
        loaded_mood_data = load_mood_data()
        
        self.assertEqual(len(loaded_mood_data), 1)
        self.assertEqual(loaded_mood_data[0], test_mood_entry)
        self.assertEqual(loaded_mood_data[0]["mood"], "😊 Happy")
        self.assertEqual(loaded_mood_data[0]["intensity"], 8)
    
    def test_save_multiple_mood_entries(self):
        """Test saving multiple mood entries"""
        mood_entries = [
            {
                "timestamp": "2024-01-15T10:30:00",
                "mood": "😊 Happy",
                "intensity": 8,
                "note": "Morning mood",
                "date": "2024-01-15",
                "time": "10:30"
            },
            {
                "timestamp": "2024-01-15T15:30:00",
                "mood": "😌 Calm",
                "intensity": 6,
                "note": "Afternoon mood",
                "date": "2024-01-15",
                "time": "15:30"
            }
        ]
        
        # Save multiple entries
        for entry in mood_entries:
            save_mood_data(entry)
        
        # Load all entries
        loaded_mood_data = load_mood_data()
        
        self.assertEqual(len(loaded_mood_data), 2)
        self.assertEqual(loaded_mood_data[0]["mood"], "😊 Happy")
        self.assertEqual(loaded_mood_data[1]["mood"], "😌 Calm")
    
    def test_delete_mood_entry(self):
        """Test deleting a specific mood entry"""
        mood_entries = [
            {
                "timestamp": "2024-01-15T10:30:00",
                "mood": "😊 Happy",
                "intensity": 8,
                "note": "Keep this one",
                "date": "2024-01-15",
                "time": "10:30"
            },
            {
                "timestamp": "2024-01-15T15:30:00",
                "mood": "😌 Calm",
                "intensity": 6,
                "note": "Delete this one",
                "date": "2024-01-15",
                "time": "15:30"
            }
        ]
        
        # Save entries
        for entry in mood_entries:
            save_mood_data(entry)
        
        # Verify both entries exist
        loaded_mood_data = load_mood_data()
        self.assertEqual(len(loaded_mood_data), 2)
        
        # Delete second entry
        delete_mood_entry("2024-01-15T15:30:00")
        
        # Verify only first entry remains
        loaded_mood_data = load_mood_data()
        self.assertEqual(len(loaded_mood_data), 1)
        self.assertEqual(loaded_mood_data[0]["mood"], "😊 Happy")
    
    def test_save_all_mood_data(self):
        """Test saving entire mood data array"""
        mood_entries = [
            {
                "timestamp": "2024-01-15T10:30:00",
                "mood": "😊 Happy",
                "intensity": 8,
                "date": "2024-01-15",
                "time": "10:30"
            },
            {
                "timestamp": "2024-01-15T15:30:00",
                "mood": "😌 Calm",
                "intensity": 6,
                "date": "2024-01-15",
                "time": "15:30"
            }
        ]
        
        # Save all data at once
        save_all_mood_data(mood_entries)
        
        # Load and verify
        loaded_mood_data = load_mood_data()
        self.assertEqual(loaded_mood_data, mood_entries)
    
    def test_save_and_load_checkin_data(self):
        """Test saving and loading check-in data"""
        test_checkin_entry = {
            "timestamp": "2024-01-15T08:00:00",
            "time_period": "morning",
            "sleep_quality": "Good",
            "focus_today": "Complete project proposal",
            "energy_level": "High"
        }
        
        # Test saving check-in entry
        save_checkin_data(test_checkin_entry)
        
        # Test loading check-in data
        loaded_checkin_data = load_checkin_data()
        
        self.assertEqual(len(loaded_checkin_data), 1)
        self.assertEqual(loaded_checkin_data[0], test_checkin_entry)
        self.assertEqual(loaded_checkin_data[0]["time_period"], "morning")
        self.assertEqual(loaded_checkin_data[0]["sleep_quality"], "Good")
    
    def test_save_multiple_checkin_entries(self):
        """Test saving multiple check-in entries"""
        checkin_entries = [
            {
                "timestamp": "2024-01-15T08:00:00",
                "time_period": "morning",
                "sleep_quality": "Good",
                "focus_today": "Morning tasks",
                "energy_level": "High"
            },
            {
                "timestamp": "2024-01-15T14:00:00",
                "time_period": "afternoon",
                "day_progress": "Good",
                "adjust_plan": "No changes needed",
                "take_break": "No, I'm in the zone"
            }
        ]
        
        # Save multiple entries
        for entry in checkin_entries:
            save_checkin_data(entry)
        
        # Load all entries
        loaded_checkin_data = load_checkin_data()
        
        self.assertEqual(len(loaded_checkin_data), 2)
        self.assertEqual(loaded_checkin_data[0]["time_period"], "morning")
        self.assertEqual(loaded_checkin_data[1]["time_period"], "afternoon")
    
    def test_save_all_checkin_data(self):
        """Test saving entire check-in data array"""
        checkin_entries = [
            {
                "timestamp": "2024-01-15T08:00:00",
                "time_period": "morning",
                "sleep_quality": "Good",
                "focus_today": "Morning tasks",
                "energy_level": "High"
            },
            {
                "timestamp": "2024-01-15T14:00:00",
                "time_period": "afternoon",
                "day_progress": "Good",
                "adjust_plan": "No changes needed",
                "take_break": "No, I'm in the zone"
            }
        ]
        
        # Save all data at once
        save_all_checkin_data(checkin_entries)
        
        # Load and verify
        loaded_checkin_data = load_checkin_data()
        self.assertEqual(loaded_checkin_data, checkin_entries)
    
    def test_load_empty_data_files(self):
        """Test loading data when files don't exist"""
        # Ensure no data files exist
        import data.storage as storage_module
        for path in [storage_module.MOOD_DATA_PATH, storage_module.CHECKIN_DATA_PATH]:
            if os.path.exists(path):
                os.remove(path)
        
        # Test loading empty data
        mood_data = load_mood_data()
        checkin_data = load_checkin_data()
        
        self.assertEqual(mood_data, [])
        self.assertEqual(checkin_data, [])
    
    def test_corrupted_json_handling(self):
        """Test handling of corrupted JSON files"""
        import data.storage as storage_module
        
        # Create corrupted JSON file
        with open(storage_module.PROFILE_PATH, 'w') as f:
            f.write('{"invalid": json}')
        
        # Should return empty dict for corrupted profile
        profile = load_user_profile()
        self.assertEqual(profile, {})
    
    def test_directory_creation(self):
        """Test that directories are created when they don't exist"""
        # Remove test directory
        shutil.rmtree(self.test_dir)
        
        # Save data (should create directory)
        test_profile = {"goal": "Test goal"}
        save_user_profile(test_profile)
        
        # Verify directory was created
        self.assertTrue(os.path.exists(self.test_dir))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "user_profile.json")))


if __name__ == '__main__':
    unittest.main() 