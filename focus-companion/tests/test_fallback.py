"""
Unit tests for the fallback assistant system
Tests FallbackAssistant class and all response methods
"""

import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the assistant module
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from assistant.fallback import FallbackAssistant


class TestFallbackAssistant(unittest.TestCase):
    """Test cases for the FallbackAssistant class"""
    
    def setUp(self):
        """Set up test environment"""
        self.user_profile = {
            "goal": "Improve focus and productivity",
            "availability": "2-4 hours",
            "energy": "Good",
            "check_ins": "Yes",
            "tone": "Gentle & supportive",
            "situation": "Freelancer"
        }
        
        self.assistant = FallbackAssistant(self.user_profile)
    
    def test_initialization(self):
        """Test FallbackAssistant initialization"""
        self.assertEqual(self.assistant.user_profile, self.user_profile)
        self.assertEqual(self.assistant.user_goal, "Improve focus and productivity")
        self.assertEqual(self.assistant.user_tone, "Gentle & supportive")
    
    def test_get_daily_encouragement(self):
        """Test daily encouragement generation"""
        encouragement = self.assistant.get_daily_encouragement()
        
        # Check that encouragement is a string
        self.assertIsInstance(encouragement, str)
        self.assertGreater(len(encouragement), 0)
        
        # Check that it contains encouraging content
        encouraging_words = ["great", "amazing", "wonderful", "excellent", "fantastic", "incredible"]
        has_encouraging_word = any(word in encouragement.lower() for word in encouraging_words)
        self.assertTrue(has_encouraging_word or "!" in encouragement)
    
    def test_get_mood_insight(self):
        """Test mood insight generation"""
        # Test with different moods
        happy_mood = "😊 Happy"
        calm_mood = "😌 Calm"
        stressed_mood = "😤 Stressed"
        
        happy_insight = self.assistant.get_mood_insight(happy_mood)
        calm_insight = self.assistant.get_mood_insight(calm_mood)
        stressed_insight = self.assistant.get_mood_insight(stressed_mood)
        
        # Check that insights are strings
        self.assertIsInstance(happy_insight, str)
        self.assertIsInstance(calm_insight, str)
        self.assertIsInstance(stressed_insight, str)
        
        # Check that insights are not empty
        self.assertGreater(len(happy_insight), 0)
        self.assertGreater(len(calm_insight), 0)
        self.assertGreater(len(stressed_insight), 0)
        
        # Check that insights are different for different moods
        self.assertNotEqual(happy_insight, calm_insight)
        self.assertNotEqual(calm_insight, stressed_insight)
    
    def test_get_productivity_tip(self):
        """Test productivity tip generation"""
        tip = self.assistant.get_productivity_tip()
        
        # Check that tip is a string
        self.assertIsInstance(tip, str)
        self.assertGreater(len(tip), 0)
        
        # Check that it contains productivity-related content
        productivity_words = ["focus", "productivity", "efficiency", "work", "task", "goal"]
        has_productivity_word = any(word in tip.lower() for word in productivity_words)
        self.assertTrue(has_productivity_word)
    
    def test_get_wellness_reminder(self):
        """Test wellness reminder generation"""
        reminder = self.assistant.get_wellness_reminder()
        
        # Check that reminder is a string
        self.assertIsInstance(reminder, str)
        self.assertGreater(len(reminder), 0)
        
        # Check that it contains wellness-related content
        wellness_words = ["health", "wellness", "care", "rest", "break", "balance", "mindful"]
        has_wellness_word = any(word in reminder.lower() for word in wellness_words)
        self.assertTrue(has_wellness_word)
    
    def test_get_goal_reminder(self):
        """Test goal reminder generation"""
        reminder = self.assistant.get_goal_reminder()
        
        # Check that reminder is a string
        self.assertIsInstance(reminder, str)
        self.assertGreater(len(reminder), 0)
        
        # Check that it contains the user's goal
        self.assertIn("Improve focus and productivity", reminder)
    
    def test_get_weekly_motivation(self):
        """Test weekly motivation generation"""
        motivation = self.assistant.get_weekly_motivation()
        
        # Check that motivation is a string
        self.assertIsInstance(motivation, str)
        self.assertGreater(len(motivation), 0)
        
        # Check that it contains motivational content
        motivational_words = ["motivation", "inspire", "achieve", "success", "progress", "growth"]
        has_motivational_word = any(word in motivation.lower() for word in motivational_words)
        self.assertTrue(has_motivational_word or "!" in motivation)
    
    def test_get_personalized_greeting(self):
        """Test personalized greeting generation"""
        greeting = self.assistant.get_personalized_greeting()
        
        # Check that greeting is a string
        self.assertIsInstance(greeting, str)
        self.assertGreater(len(greeting), 0)
        
        # Check that it contains the user's goal
        self.assertIn("Improve focus and productivity", greeting)
        
        # Check that it contains appropriate greeting based on time
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            self.assertIn("Good morning", greeting)
        elif 12 <= current_hour < 18:
            self.assertIn("Good afternoon", greeting)
        else:
            self.assertIn("Good evening", greeting)
    
    def test_get_activity_suggestion(self):
        """Test activity suggestion generation"""
        suggestion = self.assistant.get_activity_suggestion()
        
        # Check that suggestion is a string
        self.assertIsInstance(suggestion, str)
        self.assertGreater(len(suggestion), 0)
        
        # Check that it contains activity-related content
        activity_words = ["activity", "exercise", "walk", "stretch", "meditation", "break"]
        has_activity_word = any(word in suggestion.lower() for word in activity_words)
        self.assertTrue(has_activity_word)
    
    def test_get_encouragement_for_situation(self):
        """Test situation-specific encouragement generation"""
        # Test with different situations
        situations = [
            "feeling overwhelmed",
            "lack of motivation",
            "procrastination",
            "stress",
            "tiredness"
        ]
        
        for situation in situations:
            encouragement = self.assistant.get_encouragement_for_situation(situation)
            
            # Check that encouragement is a string
            self.assertIsInstance(encouragement, str)
            self.assertGreater(len(encouragement), 0)
            
            # Check that it contains encouraging content
            encouraging_words = ["remember", "try", "consider", "think", "focus", "take"]
            has_encouraging_word = any(word in encouragement.lower() for word in encouraging_words)
            self.assertTrue(has_encouraging_word)
    
    def test_time_based_responses(self):
        """Test that responses vary based on time of day"""
        with patch('assistant.fallback.datetime') as mock_datetime:
            # Test morning time
            mock_datetime.now.return_value.hour = 9
            morning_greeting = self.assistant.get_personalized_greeting()
            self.assertIn("Good morning", morning_greeting)
            
            # Test afternoon time
            mock_datetime.now.return_value.hour = 14
            afternoon_greeting = self.assistant.get_personalized_greeting()
            self.assertIn("Good afternoon", afternoon_greeting)
            
            # Test evening time
            mock_datetime.now.return_value.hour = 20
            evening_greeting = self.assistant.get_personalized_greeting()
            self.assertIn("Good evening", evening_greeting)
    
    def test_tone_based_responses(self):
        """Test that responses adapt to user tone preference"""
        # Test with gentle tone
        gentle_profile = self.user_profile.copy()
        gentle_profile["tone"] = "Gentle & supportive"
        gentle_assistant = FallbackAssistant(gentle_profile)
        gentle_greeting = gentle_assistant.get_personalized_greeting()
        
        # Test with direct tone
        direct_profile = self.user_profile.copy()
        direct_profile["tone"] = "Direct & motivating"
        direct_assistant = FallbackAssistant(direct_profile)
        direct_greeting = direct_assistant.get_personalized_greeting()
        
        # Check that greetings are different
        self.assertNotEqual(gentle_greeting, direct_greeting)
    
    def test_goal_integration(self):
        """Test that user goal is integrated into responses"""
        # Test goal reminder
        goal_reminder = self.assistant.get_goal_reminder()
        self.assertIn("Improve focus and productivity", goal_reminder)
        
        # Test personalized greeting
        greeting = self.assistant.get_personalized_greeting()
        self.assertIn("Improve focus and productivity", greeting)
    
    def test_response_variety(self):
        """Test that responses have variety and don't repeat"""
        responses = []
        
        # Generate multiple responses of the same type
        for _ in range(5):
            responses.append(self.assistant.get_daily_encouragement())
            responses.append(self.assistant.get_productivity_tip())
            responses.append(self.assistant.get_wellness_reminder())
        
        # Check that responses are not all identical
        self.assertGreater(len(set(responses)), 1)
    
    def test_empty_profile_handling(self):
        """Test handling of empty user profile"""
        empty_profile = {}
        empty_assistant = FallbackAssistant(empty_profile)
        
        # Test that it doesn't crash with empty profile
        greeting = empty_assistant.get_personalized_greeting()
        self.assertIsInstance(greeting, str)
        self.assertGreater(len(greeting), 0)
        
        # Test that default values are used
        self.assertEqual(empty_assistant.user_goal, "Improve focus and productivity")
        self.assertEqual(empty_assistant.user_tone, "Gentle & supportive")
    
    def test_missing_profile_fields(self):
        """Test handling of missing profile fields"""
        partial_profile = {"goal": "Test goal"}
        partial_assistant = FallbackAssistant(partial_profile)
        
        # Test that missing fields use defaults
        self.assertEqual(partial_assistant.user_goal, "Test goal")
        self.assertEqual(partial_assistant.user_tone, "Gentle & supportive")
        
        # Test that responses still work
        greeting = partial_assistant.get_personalized_greeting()
        self.assertIsInstance(greeting, str)
        self.assertGreater(len(greeting), 0)


if __name__ == '__main__':
    unittest.main() 