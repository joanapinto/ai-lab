"""
Tests for AI Cache functionality
"""

import unittest
import tempfile
import os
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add the parent directory to Python path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from assistant.ai_cache import AICache, PromptOptimizer

class TestAICache(unittest.TestCase):
    """Test AI Cache functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary cache file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.cache_file = os.path.join(self.temp_dir, "test_cache.json")
        self.cache = AICache(self.cache_file, max_cache_age_hours=1)
    
    def tearDown(self):
        """Clean up test environment"""
        # Remove temporary files
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_cache_initialization(self):
        """Test cache initialization"""
        self.assertEqual(len(self.cache.cache), 0)
        self.assertEqual(self.cache.max_cache_age_hours, 1)
    
    def test_cache_response(self):
        """Test caching a response"""
        feature = "greeting"
        user_email = "test@example.com"
        input_data = {"mood": "happy", "time": "morning"}
        response = "Hello! Great to see you in a happy mood this morning!"
        
        # Cache the response
        self.cache.cache_response(feature, user_email, input_data, response)
        
        # Check that response was cached
        cached_response = self.cache.get_cached_response(feature, user_email, input_data)
        self.assertEqual(cached_response, response)
    
    def test_cache_key_generation(self):
        """Test cache key generation is consistent"""
        feature = "greeting"
        user_email = "test@example.com"
        input_data = {"mood": "happy", "time": "morning"}
        
        # Generate cache key twice
        key1 = self.cache._generate_cache_key(feature, user_email, input_data)
        key2 = self.cache._generate_cache_key(feature, user_email, input_data)
        
        # Keys should be identical
        self.assertEqual(key1, key2)
    
    def test_cache_key_uniqueness(self):
        """Test cache keys are unique for different inputs"""
        feature = "greeting"
        user_email = "test@example.com"
        
        input_data1 = {"mood": "happy", "time": "morning"}
        input_data2 = {"mood": "sad", "time": "morning"}
        
        key1 = self.cache._generate_cache_key(feature, user_email, input_data1)
        key2 = self.cache._generate_cache_key(feature, user_email, input_data2)
        
        # Keys should be different
        self.assertNotEqual(key1, key2)
    
    def test_cache_expiration(self):
        """Test cache entries expire correctly"""
        feature = "greeting"
        user_email = "test@example.com"
        input_data = {"mood": "happy"}
        response = "Hello!"
        
        # Cache a response
        self.cache.cache_response(feature, user_email, input_data, response)
        
        # Manually set the timestamp to be old
        cache_key = self.cache._generate_cache_key(feature, user_email, input_data)
        old_time = datetime.now() - timedelta(hours=2)  # 2 hours ago
        self.cache.cache[cache_key]['timestamp'] = old_time.isoformat()
        
        # Should not return expired cache
        cached_response = self.cache.get_cached_response(feature, user_email, input_data)
        self.assertIsNone(cached_response)
    
    def test_cache_ignores_timestamps(self):
        """Test that cache ignores timestamp fields"""
        feature = "greeting"
        user_email = "test@example.com"
        
        input_data1 = {"mood": "happy", "timestamp": "2023-01-01T10:00:00"}
        input_data2 = {"mood": "happy", "timestamp": "2023-01-01T11:00:00"}
        
        key1 = self.cache._generate_cache_key(feature, user_email, input_data1)
        key2 = self.cache._generate_cache_key(feature, user_email, input_data2)
        
        # Keys should be identical despite different timestamps
        self.assertEqual(key1, key2)
    
    def test_cache_stats(self):
        """Test cache statistics"""
        # Add some test data
        self.cache.cache_response("greeting", "user1@test.com", {"mood": "happy"}, "Hello!")
        self.cache.cache_response("greeting", "user2@test.com", {"mood": "sad"}, "Hi there!")
        self.cache.cache_response("weekly_summary", "user1@test.com", {"week": 1}, "Summary!")
        
        stats = self.cache.get_cache_stats()
        
        self.assertEqual(stats['total_entries'], 3)
        self.assertEqual(stats['features']['greeting'], 2)
        self.assertEqual(stats['features']['weekly_summary'], 1)
        self.assertGreaterEqual(stats['cache_size_mb'], 0)
    
    def test_clear_cache(self):
        """Test clearing cache"""
        # Add test data
        self.cache.cache_response("greeting", "user1@test.com", {"mood": "happy"}, "Hello!")
        self.cache.cache_response("greeting", "user2@test.com", {"mood": "sad"}, "Hi there!")
        
        # Clear cache for specific user
        self.cache.clear_cache("user1@test.com")
        
        # Check that only user1's cache was cleared
        stats = self.cache.get_cache_stats()
        self.assertEqual(stats['total_entries'], 1)
        
        # Clear all cache
        self.cache.clear_cache()
        stats = self.cache.get_cache_stats()
        self.assertEqual(stats['total_entries'], 0)

class TestPromptOptimizer(unittest.TestCase):
    """Test Prompt Optimizer functionality"""
    
    def test_optimize_weekly_summary_prompt(self):
        """Test weekly summary prompt optimization"""
        user_profile = {
            "goal": "Improve focus and productivity",
            "tone": "Friendly"
        }
        
        week_analysis = {
            "total_checkins": 5,
            "total_mood_entries": 3,
            "checkin_days": ["Monday", "Tuesday", "Wednesday"],
            "energy_patterns": {"Monday": ["High"], "Tuesday": ["Good"]},
            "mood_patterns": {"Monday": {"moods": ["Happy"], "intensities": [8]}},
            "time_periods": {"morning": 3, "afternoon": 2},
            "accomplishments": ["Completed project"],
            "challenges": ["Focus issues"]
        }
        
        prompt = PromptOptimizer.optimize_weekly_summary_prompt(user_profile, week_analysis)
        
        # Check that prompt is optimized (shorter and more focused)
        self.assertIn("Improve focus and productivity", prompt)
        self.assertIn("5 check-ins", prompt)
        self.assertIn("3 moods", prompt)
        self.assertLess(len(prompt), 500)  # Should be much shorter than original
    
    def test_optimize_greeting_prompt(self):
        """Test greeting prompt optimization"""
        user_profile = {
            "goal": "Improve focus and productivity",
            "tone": "Friendly"
        }
        
        recent_data = {
            "time_context": "morning",
            "mood_summary": "You've been in a positive mood recently",
            "checkin_summary": "Your energy has been good"
        }
        
        prompt = PromptOptimizer.optimize_greeting_prompt(user_profile, recent_data)
        
        # Check that prompt is optimized
        self.assertIn("morning", prompt)
        self.assertIn("positive mood", prompt)
        self.assertLess(len(prompt), 250)  # Should be concise
    
    def test_optimize_encouragement_prompt(self):
        """Test encouragement prompt optimization"""
        user_profile = {
            "goal": "Improve focus and productivity",
            "tone": "Friendly"
        }
        
        recent_data = {
            "checkin_summary": "Good energy"
        }
        
        prompt = PromptOptimizer.optimize_encouragement_prompt(user_profile, recent_data)
        
        # Check that prompt is optimized
        self.assertIn("Good energy", prompt)
        self.assertIn("Improve focus and productivity", prompt)
        self.assertLess(len(prompt), 150)  # Should be very concise

if __name__ == "__main__":
    unittest.main() 