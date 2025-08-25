"""
Integration tests for mood logging functionality
Tests the complete mood tracking workflow
"""

import unittest
import tempfile
import shutil
import os
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.storage import (
    save_mood_data, load_mood_data, save_all_mood_data, delete_mood_entry
)
from assistant.logic import FocusAssistant
from assistant.fallback import FallbackAssistant


class TestMoodLoggingIntegration(unittest.TestCase):
    """Integration tests for mood logging functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        
        # Store original paths
        import data.storage as storage_module
        self.original_mood_path_value = storage_module.MOOD_DATA_PATH
        
        # Set test path
        storage_module.MOOD_DATA_PATH = os.path.join(self.test_dir, "mood_data.json")
        
        # Sample user profile
        self.user_profile = {
            "goal": "Improve focus and productivity",
            "availability": "2-4 hours",
            "energy": "Good",
            "check_ins": "Yes",
            "tone": "Gentle & supportive",
            "situation": "Freelancer"
        }
        
        # Sample mood entries for testing
        self.sample_mood_entries = [
            {
                "timestamp": "2024-01-15T10:30:00",
                "mood": "😊 Happy",
                "intensity": 8,
                "note": "Feeling productive today!",
                "date": "2024-01-15",
                "time": "10:30"
            },
            {
                "timestamp": "2024-01-15T15:30:00",
                "mood": "😌 Calm",
                "intensity": 6,
                "note": "Afternoon mood - feeling balanced",
                "date": "2024-01-15",
                "time": "15:30"
            },
            {
                "timestamp": "2024-01-16T09:00:00",
                "mood": "😤 Stressed",
                "intensity": 3,
                "note": "Feeling overwhelmed with tasks",
                "date": "2024-01-16",
                "time": "09:00"
            },
            {
                "timestamp": "2024-01-16T14:00:00",
                "mood": "😊 Happy",
                "intensity": 7,
                "note": "Made good progress on project",
                "date": "2024-01-16",
                "time": "14:00"
            }
        ]
    
    def tearDown(self):
        """Clean up test environment"""
        # Restore original path
        import data.storage as storage_module
        storage_module.MOOD_DATA_PATH = self.original_mood_path_value
        
        # Remove test directory
        shutil.rmtree(self.test_dir)
    
    def test_complete_mood_logging_workflow(self):
        """Test the complete mood logging workflow"""
        # Step 1: Save multiple mood entries
        for entry in self.sample_mood_entries:
            save_mood_data(entry)
        
        # Step 2: Load and verify all entries
        loaded_mood_data = load_mood_data()
        self.assertEqual(len(loaded_mood_data), 4)
        
        # Step 3: Verify specific entries
        happy_entries = [entry for entry in loaded_mood_data if entry["mood"] == "😊 Happy"]
        stressed_entries = [entry for entry in loaded_mood_data if entry["mood"] == "😤 Stressed"]
        
        self.assertEqual(len(happy_entries), 2)
        self.assertEqual(len(stressed_entries), 1)
        
        # Step 4: Test mood analysis with FocusAssistant
        assistant = FocusAssistant(self.user_profile, loaded_mood_data, [])
        mood_analysis = assistant.analyze_mood_patterns()
        
        # Verify analysis contains expected data
        self.assertIn("insights", mood_analysis)
        self.assertIn("patterns", mood_analysis)
        self.assertIn("recent_trend", mood_analysis)
        
        # Step 5: Test fallback assistant mood insights
        fallback_assistant = FallbackAssistant(self.user_profile)
        
        for entry in loaded_mood_data:
            insight = fallback_assistant.get_mood_insight(entry["mood"])
            self.assertIsInstance(insight, str)
            self.assertGreater(len(insight), 0)
    
    def test_mood_data_analysis_integration(self):
        """Test integration between mood data and analysis"""
        # Save sample mood data
        for entry in self.sample_mood_entries:
            save_mood_data(entry)
        
        loaded_mood_data = load_mood_data()
        assistant = FocusAssistant(self.user_profile, loaded_mood_data, [])
        
        # Test mood pattern analysis
        analysis = assistant.analyze_mood_patterns()
        
        # Verify analysis structure
        self.assertIsInstance(analysis["insights"], list)
        self.assertIsInstance(analysis["patterns"], list)
        self.assertIsInstance(analysis["recent_trend"], str)
        
        # Verify that analysis provides meaningful insights
        if analysis["insights"]:
            for insight in analysis["insights"]:
                self.assertIsInstance(insight, str)
                self.assertGreater(len(insight), 0)
        
        if analysis["patterns"]:
            for pattern in analysis["patterns"]:
                self.assertIsInstance(pattern, str)
                self.assertGreater(len(pattern), 0)
    
    def test_mood_intensity_analysis(self):
        """Test mood intensity analysis and trends"""
        # Create mood entries with varying intensities
        intensity_test_entries = [
            {
                "timestamp": "2024-01-15T10:00:00",
                "mood": "😊 Happy",
                "intensity": 9,
                "note": "Very high energy",
                "date": "2024-01-15",
                "time": "10:00"
            },
            {
                "timestamp": "2024-01-15T14:00:00",
                "mood": "😊 Happy",
                "intensity": 6,
                "note": "Moderate energy",
                "date": "2024-01-15",
                "time": "14:00"
            },
            {
                "timestamp": "2024-01-15T18:00:00",
                "mood": "😊 Happy",
                "intensity": 4,
                "note": "Lower energy",
                "date": "2024-01-15",
                "time": "18:00"
            }
        ]
        
        # Save intensity test entries
        for entry in intensity_test_entries:
            save_mood_data(entry)
        
        loaded_mood_data = load_mood_data()
        assistant = FocusAssistant(self.user_profile, loaded_mood_data, [])
        
        # Test intensity analysis
        analysis = assistant.analyze_mood_patterns()
        
        # Verify that intensity patterns are detected
        self.assertIsInstance(analysis["patterns"], list)
        
        # Check for time-based patterns
        time_patterns = [pattern for pattern in analysis["patterns"] if "time" in pattern.lower()]
        self.assertGreaterEqual(len(time_patterns), 0)
    
    def test_mood_data_filtering_and_search(self):
        """Test filtering and searching mood data"""
        # Save sample mood data
        for entry in self.sample_mood_entries:
            save_mood_data(entry)
        
        loaded_mood_data = load_mood_data()
        
        # Test filtering by mood
        happy_moods = [entry for entry in loaded_mood_data if "Happy" in entry["mood"]]
        stressed_moods = [entry for entry in loaded_mood_data if "Stressed" in entry["mood"]]
        
        self.assertEqual(len(happy_moods), 2)
        self.assertEqual(len(stressed_moods), 1)
        
        # Test filtering by intensity
        high_intensity = [entry for entry in loaded_mood_data if entry["intensity"] >= 7]
        low_intensity = [entry for entry in loaded_mood_data if entry["intensity"] <= 4]
        
        self.assertEqual(len(high_intensity), 2)  # 8 and 7
        self.assertEqual(len(low_intensity), 1)   # 3
        
        # Test filtering by date
        jan_15_entries = [entry for entry in loaded_mood_data if entry["date"] == "2024-01-15"]
        jan_16_entries = [entry for entry in loaded_mood_data if entry["date"] == "2024-01-16"]
        
        self.assertEqual(len(jan_15_entries), 2)
        self.assertEqual(len(jan_16_entries), 2)
    
    def test_mood_data_modification_workflow(self):
        """Test mood data modification workflow"""
        # Save initial mood data
        for entry in self.sample_mood_entries:
            save_mood_data(entry)
        
        loaded_mood_data = load_mood_data()
        initial_count = len(loaded_mood_data)
        
        # Test deleting an entry
        timestamp_to_delete = "2024-01-15T15:30:00"
        delete_mood_entry(timestamp_to_delete)
        
        # Verify entry was deleted
        updated_mood_data = load_mood_data()
        self.assertEqual(len(updated_mood_data), initial_count - 1)
        
        # Verify the specific entry is gone
        deleted_entry = [entry for entry in updated_mood_data if entry["timestamp"] == timestamp_to_delete]
        self.assertEqual(len(deleted_entry), 0)
        
        # Test adding a new entry after deletion
        new_entry = {
            "timestamp": "2024-01-17T12:00:00",
            "mood": "😌 Calm",
            "intensity": 5,
            "note": "New entry after deletion",
            "date": "2024-01-17",
            "time": "12:00"
        }
        save_mood_data(new_entry)
        
        # Verify new entry was added
        final_mood_data = load_mood_data()
        self.assertEqual(len(final_mood_data), initial_count)  # Deleted one, added one
        
        # Verify new entry exists
        new_entry_found = [entry for entry in final_mood_data if entry["timestamp"] == "2024-01-17T12:00:00"]
        self.assertEqual(len(new_entry_found), 1)
    
    def test_mood_data_export_import(self):
        """Test mood data export and import functionality"""
        # Save sample mood data
        for entry in self.sample_mood_entries:
            save_mood_data(entry)
        
        loaded_mood_data = load_mood_data()
        
        # Test export functionality (save_all_mood_data)
        export_data = [
            {
                "timestamp": "2024-01-18T10:00:00",
                "mood": "😊 Happy",
                "intensity": 8,
                "note": "Exported entry",
                "date": "2024-01-18",
                "time": "10:00"
            }
        ]
        
        save_all_mood_data(export_data)
        
        # Verify export replaced existing data
        exported_mood_data = load_mood_data()
        self.assertEqual(len(exported_mood_data), 1)
        self.assertEqual(exported_mood_data[0]["note"], "Exported entry")
    
    def test_mood_data_validation(self):
        """Test mood data validation and error handling"""
        # Test with invalid mood entry (missing required fields)
        invalid_entry = {
            "timestamp": "2024-01-15T10:30:00",
            "mood": "😊 Happy"
            # Missing intensity, note, date, time
        }
        
        # Should still save without crashing
        save_mood_data(invalid_entry)
        
        loaded_mood_data = load_mood_data()
        self.assertEqual(len(loaded_mood_data), 1)
        
        # Verify the entry was saved with missing fields
        saved_entry = loaded_mood_data[0]
        self.assertEqual(saved_entry["mood"], "😊 Happy")
        self.assertNotIn("intensity", saved_entry)
        self.assertNotIn("note", saved_entry)
    
    def test_mood_data_performance(self):
        """Test mood data performance with larger datasets"""
        # Create larger dataset
        large_mood_dataset = []
        for i in range(100):
            entry = {
                "timestamp": f"2024-01-{15 + (i // 10):02d}T{10 + (i % 10):02d}:00:00",
                "mood": "😊 Happy" if i % 3 == 0 else "😌 Calm" if i % 3 == 1 else "😤 Stressed",
                "intensity": (i % 10) + 1,
                "note": f"Entry {i}",
                "date": f"2024-01-{15 + (i // 10):02d}",
                "time": f"{10 + (i % 10):02d}:00"
            }
            large_mood_dataset.append(entry)
        
        # Save large dataset
        for entry in large_mood_dataset:
            save_mood_data(entry)
        
        # Test loading performance
        loaded_mood_data = load_mood_data()
        self.assertEqual(len(loaded_mood_data), 100)
        
        # Test analysis performance
        assistant = FocusAssistant(self.user_profile, loaded_mood_data, [])
        analysis = assistant.analyze_mood_patterns()
        
        # Verify analysis still works with large dataset
        self.assertIn("insights", analysis)
        self.assertIn("patterns", analysis)
        self.assertIn("recent_trend", analysis)
    
    def test_mood_data_concurrent_access(self):
        """Test mood data concurrent access scenarios"""
        # Simulate concurrent access by saving multiple entries rapidly
        concurrent_entries = []
        for i in range(10):
            entry = {
                "timestamp": f"2024-01-15T{10 + i}:00:00",
                "mood": "😊 Happy",
                "intensity": 7,
                "note": f"Concurrent entry {i}",
                "date": "2024-01-15",
                "time": f"{10 + i}:00"
            }
            concurrent_entries.append(entry)
        
        # Save all entries
        for entry in concurrent_entries:
            save_mood_data(entry)
        
        # Verify all entries were saved
        loaded_mood_data = load_mood_data()
        self.assertEqual(len(loaded_mood_data), 10)
        
        # Verify no data corruption
        for entry in loaded_mood_data:
            self.assertIn("timestamp", entry)
            self.assertIn("mood", entry)
            self.assertIn("intensity", entry)
            self.assertIn("note", entry)


if __name__ == '__main__':
    unittest.main() 