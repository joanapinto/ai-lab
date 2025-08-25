"""
Unit tests for the prompt templates system
Tests PromptTemplates and ResponseFormats classes
"""

import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the assistant module
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from assistant.prompts import PromptTemplates, ResponseFormats


class TestPromptTemplates(unittest.TestCase):
    """Test cases for the PromptTemplates class"""
    
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
        
        self.sample_mood_data = [
            {
                "timestamp": "2024-01-15T10:30:00",
                "mood": "😊 Happy",
                "intensity": 8,
                "note": "Feeling productive today!",
                "date": "2024-01-15",
                "time": "10:30"
            }
        ]
        
        self.sample_checkin_data = [
            {
                "timestamp": "2024-01-15T08:00:00",
                "time_period": "morning",
                "sleep_quality": "Good",
                "focus_today": "Complete project proposal",
                "energy_level": "High"
            }
        ]
    
    def test_mood_analysis_prompt(self):
        """Test mood analysis prompt generation"""
        prompt = PromptTemplates.mood_analysis_prompt(
            self.user_profile,
            self.sample_mood_data,
            "😊 Happy"
        )
        
        # Check that prompt is a string
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        
        # Check that it contains expected elements
        self.assertIn("mood analysis", prompt.lower())
        self.assertIn("Improve focus and productivity", prompt)
        self.assertIn("😊 Happy", prompt)
        self.assertIn("user profile", prompt.lower())
        self.assertIn("mood history", prompt.lower())
    
    def test_daily_recommendation_prompt(self):
        """Test daily recommendation prompt generation"""
        prompt = PromptTemplates.daily_recommendation_prompt(
            self.user_profile,
            self.sample_mood_data,
            self.sample_checkin_data
        )
        
        # Check that prompt is a string
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        
        # Check that it contains expected elements
        self.assertIn("daily recommendation", prompt.lower())
        self.assertIn("Improve focus and productivity", prompt)
        self.assertIn("user profile", prompt.lower())
        self.assertIn("mood data", prompt.lower())
        self.assertIn("check-in data", prompt.lower())
    
    def test_weekly_reflection_prompt(self):
        """Test weekly reflection prompt generation"""
        prompt = PromptTemplates.weekly_reflection_prompt(
            self.user_profile,
            self.sample_mood_data,
            self.sample_checkin_data
        )
        
        # Check that prompt is a string
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        
        # Check that it contains expected elements
        self.assertIn("weekly reflection", prompt.lower())
        self.assertIn("Improve focus and productivity", prompt)
        self.assertIn("user profile", prompt.lower())
        self.assertIn("mood data", prompt.lower())
        self.assertIn("check-in data", prompt.lower())
    
    def test_focus_optimization_prompt(self):
        """Test focus optimization prompt generation"""
        prompt = PromptTemplates.focus_optimization_prompt(
            self.user_profile,
            self.sample_checkin_data
        )
        
        # Check that prompt is a string
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        
        # Check that it contains expected elements
        self.assertIn("focus optimization", prompt.lower())
        self.assertIn("Improve focus and productivity", prompt)
        self.assertIn("user profile", prompt.lower())
        self.assertIn("check-in data", prompt.lower())
    
    def test_sleep_optimization_prompt(self):
        """Test sleep optimization prompt generation"""
        prompt = PromptTemplates.sleep_optimization_prompt(
            self.user_profile,
            self.sample_checkin_data
        )
        
        # Check that prompt is a string
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        
        # Check that it contains expected elements
        self.assertIn("sleep optimization", prompt.lower())
        self.assertIn("Improve focus and productivity", prompt)
        self.assertIn("user profile", prompt.lower())
        self.assertIn("check-in data", prompt.lower())
    
    def test_goal_progress_prompt(self):
        """Test goal progress prompt generation"""
        prompt = PromptTemplates.goal_progress_prompt(
            self.user_profile,
            self.sample_checkin_data
        )
        
        # Check that prompt is a string
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        
        # Check that it contains expected elements
        self.assertIn("goal progress", prompt.lower())
        self.assertIn("Improve focus and productivity", prompt)
        self.assertIn("user profile", prompt.lower())
        self.assertIn("check-in data", prompt.lower())
    
    def test_stress_management_prompt(self):
        """Test stress management prompt generation"""
        prompt = PromptTemplates.stress_management_prompt(
            self.user_profile,
            self.sample_mood_data,
            self.sample_checkin_data
        )
        
        # Check that prompt is a string
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        
        # Check that it contains expected elements
        self.assertIn("stress management", prompt.lower())
        self.assertIn("Improve focus and productivity", prompt)
        self.assertIn("user profile", prompt.lower())
        self.assertIn("mood data", prompt.lower())
        self.assertIn("check-in data", prompt.lower())
    
    def test_productivity_insights_prompt(self):
        """Test productivity insights prompt generation"""
        prompt = PromptTemplates.productivity_insights_prompt(
            self.user_profile,
            self.sample_checkin_data
        )
        
        # Check that prompt is a string
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        
        # Check that it contains expected elements
        self.assertIn("productivity insights", prompt.lower())
        self.assertIn("Improve focus and productivity", prompt)
        self.assertIn("user profile", prompt.lower())
        self.assertIn("check-in data", prompt.lower())
    
    def test_morning_checkin_prompt(self):
        """Test morning check-in prompt generation"""
        analysis_data = {
            "previous_evening": {"time_period": "evening", "current_feeling": "Good"},
            "current_checkin": {"sleep_quality": "Good", "energy_level": "High"},
            "sleep_analysis": {"average_quality": 4.0, "trend": "improving"},
            "energy_analysis": {"average_energy": 4.0, "trend": "stable"},
            "focus_suggestions": ["Tackle challenging tasks first"],
            "wellness_tips": ["Start with water", "Take deep breaths"]
        }
        
        prompt = PromptTemplates.morning_checkin_prompt(
            self.user_profile,
            analysis_data
        )
        
        # Check that prompt is a string
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        
        # Check that it contains expected elements
        self.assertIn("morning check-in", prompt.lower())
        self.assertIn("Improve focus and productivity", prompt)
        self.assertIn("user profile", prompt.lower())
        self.assertIn("sleep quality", prompt.lower())
        self.assertIn("energy level", prompt.lower())
    
    def test_afternoon_checkin_prompt(self):
        """Test afternoon check-in prompt generation"""
        analysis_data = {
            "morning_checkin": {"focus_today": "Complete project", "energy_level": "High"},
            "current_checkin": {"day_progress": "Good", "take_break": "Maybe later"},
            "progress_analysis": {"progress_level": "Good", "insights": ["Making progress"]},
            "energy_changes": {"energy_trend": "maintaining", "maintenance_tips": ["Stay hydrated"]},
            "plan_adjustments": ["Continue current approach"],
            "break_recommendations": ["Consider short break"]
        }
        
        prompt = PromptTemplates.afternoon_checkin_prompt(
            self.user_profile,
            analysis_data
        )
        
        # Check that prompt is a string
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        
        # Check that it contains expected elements
        self.assertIn("afternoon check-in", prompt.lower())
        self.assertIn("Improve focus and productivity", prompt)
        self.assertIn("user profile", prompt.lower())
        self.assertIn("day progress", prompt.lower())
        self.assertIn("morning check-in", prompt.lower())
    
    def test_evening_checkin_prompt(self):
        """Test evening check-in prompt generation"""
        analysis_data = {
            "daily_journey": {
                "morning": {"focus_today": "Complete project"},
                "afternoon": {"day_progress": "Good"},
                "evening": {"current_feeling": "Accomplished"},
                "complete": True
            },
            "current_checkin": {
                "accomplishments": "Completed project",
                "challenges": "Technical difficulties",
                "current_feeling": "Accomplished"
            },
            "daily_patterns": {"energy_flow": "optimal", "successes": ["High productivity"]},
            "emotional_analysis": {"emotional_state": "Accomplished", "processing_needs": ["Celebrate"]},
            "tomorrow_preparation": ["Build on momentum"],
            "sleep_preparation": ["Create relaxing routine"]
        }
        
        prompt = PromptTemplates.evening_checkin_prompt(
            self.user_profile,
            analysis_data
        )
        
        # Check that prompt is a string
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        
        # Check that it contains expected elements
        self.assertIn("evening check-in", prompt.lower())
        self.assertIn("Improve focus and productivity", prompt)
        self.assertIn("user profile", prompt.lower())
        self.assertIn("daily journey", prompt.lower())
        self.assertIn("accomplishments", prompt.lower())
    
    def test_daily_summary_prompt(self):
        """Test daily summary prompt generation"""
        summary_data = {
            "complete_daily_data": {
                "morning": {"focus_today": "Complete project"},
                "afternoon": {"day_progress": "Good"},
                "evening": {"current_feeling": "Accomplished"},
                "complete": True
            },
            "mood_analysis": {"insights": ["Positive trend"], "patterns": ["Good energy"]},
            "checkin_analysis": {"insights": ["Consistent check-ins"], "recommendations": ["Keep routine"]},
            "goal_progress": {"progress_indicators": ["Set focus goals"], "overall_progress": "good"},
            "wellness_assessment": {"wellness_indicators": ["Good sleep"], "overall_wellness": "good"},
            "growth_insights": ["Demonstrated goal-setting", "Faced challenges"]
        }
        
        prompt = PromptTemplates.daily_summary_prompt(
            self.user_profile,
            summary_data
        )
        
        # Check that prompt is a string
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
        
        # Check that it contains expected elements
        self.assertIn("daily summary", prompt.lower())
        self.assertIn("Improve focus and productivity", prompt)
        self.assertIn("user profile", prompt.lower())
        self.assertIn("complete daily data", prompt.lower())
        self.assertIn("mood analysis", prompt.lower())
    
    def test_empty_data_handling(self):
        """Test prompt generation with empty data"""
        empty_mood_data = []
        empty_checkin_data = []
        
        # Test mood analysis with empty data
        mood_prompt = PromptTemplates.mood_analysis_prompt(
            self.user_profile,
            empty_mood_data,
            "😊 Happy"
        )
        self.assertIsInstance(mood_prompt, str)
        self.assertGreater(len(mood_prompt), 0)
        
        # Test daily recommendation with empty data
        rec_prompt = PromptTemplates.daily_recommendation_prompt(
            self.user_profile,
            empty_mood_data,
            empty_checkin_data
        )
        self.assertIsInstance(rec_prompt, str)
        self.assertGreater(len(rec_prompt), 0)
    
    def test_empty_profile_handling(self):
        """Test prompt generation with empty profile"""
        empty_profile = {}
        
        prompt = PromptTemplates.mood_analysis_prompt(
            empty_profile,
            self.sample_mood_data,
            "😊 Happy"
        )
        
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)


class TestResponseFormats(unittest.TestCase):
    """Test cases for the ResponseFormats class"""
    
    def test_mood_analysis_format(self):
        """Test mood analysis response format"""
        format_spec = ResponseFormats.mood_analysis_format()
        
        # Check that format is a string
        self.assertIsInstance(format_spec, str)
        self.assertGreater(len(format_spec), 0)
        
        # Check that it contains expected elements
        self.assertIn("json", format_spec.lower())
        self.assertIn("insights", format_spec.lower())
        self.assertIn("patterns", format_spec.lower())
        self.assertIn("recommendations", format_spec.lower())
    
    def test_daily_recommendation_format(self):
        """Test daily recommendation response format"""
        format_spec = ResponseFormats.daily_recommendation_format()
        
        # Check that format is a string
        self.assertIsInstance(format_spec, str)
        self.assertGreater(len(format_spec), 0)
        
        # Check that it contains expected elements
        self.assertIn("json", format_spec.lower())
        self.assertIn("recommendation", format_spec.lower())
        self.assertIn("reasoning", format_spec.lower())
        self.assertIn("priority", format_spec.lower())
    
    def test_weekly_reflection_format(self):
        """Test weekly reflection response format"""
        format_spec = ResponseFormats.weekly_reflection_format()
        
        # Check that format is a string
        self.assertIsInstance(format_spec, str)
        self.assertGreater(len(format_spec), 0)
        
        # Check that it contains expected elements
        self.assertIn("json", format_spec.lower())
        self.assertIn("summary", format_spec.lower())
        self.assertIn("insights", format_spec.lower())
        self.assertIn("growth_areas", format_spec.lower())
        self.assertIn("next_week_goals", format_spec.lower())
    
    def test_focus_optimization_format(self):
        """Test focus optimization response format"""
        format_spec = ResponseFormats.focus_optimization_format()
        
        # Check that format is a string
        self.assertIsInstance(format_spec, str)
        self.assertGreater(len(format_spec), 0)
        
        # Check that it contains expected elements
        self.assertIn("json", format_spec.lower())
        self.assertIn("optimization_strategies", format_spec.lower())
        self.assertIn("environment_tips", format_spec.lower())
        self.assertIn("time_management", format_spec.lower())
    
    def test_sleep_optimization_format(self):
        """Test sleep optimization response format"""
        format_spec = ResponseFormats.sleep_optimization_format()
        
        # Check that format is a string
        self.assertIsInstance(format_spec, str)
        self.assertGreater(len(format_spec), 0)
        
        # Check that it contains expected elements
        self.assertIn("json", format_spec.lower())
        self.assertIn("sleep_hygiene", format_spec.lower())
        self.assertIn("routine_suggestions", format_spec.lower())
        self.assertIn("environment_optimization", format_spec.lower())
    
    def test_goal_progress_format(self):
        """Test goal progress response format"""
        format_spec = ResponseFormats.goal_progress_format()
        
        # Check that format is a string
        self.assertIsInstance(format_spec, str)
        self.assertGreater(len(format_spec), 0)
        
        # Check that it contains expected elements
        self.assertIn("json", format_spec.lower())
        self.assertIn("progress_assessment", format_spec.lower())
        self.assertIn("milestones", format_spec.lower())
        self.assertIn("adjustments", format_spec.lower())
    
    def test_stress_management_format(self):
        """Test stress management response format"""
        format_spec = ResponseFormats.stress_management_format()
        
        # Check that format is a string
        self.assertIsInstance(format_spec, str)
        self.assertGreater(len(format_spec), 0)
        
        # Check that it contains expected elements
        self.assertIn("json", format_spec.lower())
        self.assertIn("stress_indicators", format_spec.lower())
        self.assertIn("coping_strategies", format_spec.lower())
        self.assertIn("prevention_tips", format_spec.lower())
    
    def test_productivity_insights_format(self):
        """Test productivity insights response format"""
        format_spec = ResponseFormats.productivity_insights_format()
        
        # Check that format is a string
        self.assertIsInstance(format_spec, str)
        self.assertGreater(len(format_spec), 0)
        
        # Check that it contains expected elements
        self.assertIn("json", format_spec.lower())
        self.assertIn("productivity_patterns", format_spec.lower())
        self.assertIn("peak_performance_times", format_spec.lower())
        self.assertIn("optimization_suggestions", format_spec.lower())
    
    def test_morning_checkin_format(self):
        """Test morning check-in response format"""
        format_spec = ResponseFormats.morning_checkin_format()
        
        # Check that format is a string
        self.assertIsInstance(format_spec, str)
        self.assertGreater(len(format_spec), 0)
        
        # Check that it contains expected elements
        self.assertIn("json", format_spec.lower())
        self.assertIn("morning_insights", format_spec.lower())
        self.assertIn("focus_recommendations", format_spec.lower())
        self.assertIn("wellness_tips", format_spec.lower())
    
    def test_afternoon_checkin_format(self):
        """Test afternoon check-in response format"""
        format_spec = ResponseFormats.afternoon_checkin_format()
        
        # Check that format is a string
        self.assertIsInstance(format_spec, str)
        self.assertGreater(len(format_spec), 0)
        
        # Check that it contains expected elements
        self.assertIn("json", format_spec.lower())
        self.assertIn("progress_insights", format_spec.lower())
        self.assertIn("plan_adjustments", format_spec.lower())
        self.assertIn("break_recommendations", format_spec.lower())
    
    def test_evening_checkin_format(self):
        """Test evening check-in response format"""
        format_spec = ResponseFormats.evening_checkin_format()
        
        # Check that format is a string
        self.assertIsInstance(format_spec, str)
        self.assertGreater(len(format_spec), 0)
        
        # Check that it contains expected elements
        self.assertIn("json", format_spec.lower())
        self.assertIn("daily_reflection", format_spec.lower())
        self.assertIn("emotional_processing", format_spec.lower())
        self.assertIn("tomorrow_preparation", format_spec.lower())
    
    def test_daily_summary_format(self):
        """Test daily summary response format"""
        format_spec = ResponseFormats.daily_summary_format()
        
        # Check that format is a string
        self.assertIsInstance(format_spec, str)
        self.assertGreater(len(format_spec), 0)
        
        # Check that it contains expected elements
        self.assertIn("json", format_spec.lower())
        self.assertIn("daily_overview", format_spec.lower())
        self.assertIn("key_achievements", format_spec.lower())
        self.assertIn("challenges_faced", format_spec.lower())
        self.assertIn("growth_insights", format_spec.lower())
        self.assertIn("tomorrow_focus", format_spec.lower())


if __name__ == '__main__':
    unittest.main() 