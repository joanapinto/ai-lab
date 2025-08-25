"""
Unit tests for the assistant logic system
Tests FocusAssistant class and all analysis methods
"""

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the assistant module
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from assistant.logic import FocusAssistant


class TestFocusAssistant(unittest.TestCase):
    """Test cases for the FocusAssistant class"""
    
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
            },
            {
                "timestamp": "2024-01-16T14:30:00",
                "mood": "😌 Calm",
                "intensity": 6,
                "note": "Afternoon mood",
                "date": "2024-01-16",
                "time": "14:30"
            },
            {
                "timestamp": "2024-01-17T09:30:00",
                "mood": "😤 Stressed",
                "intensity": 3,
                "note": "Feeling overwhelmed",
                "date": "2024-01-17",
                "time": "09:30"
            }
        ]
        
        self.sample_checkin_data = [
            {
                "timestamp": "2024-01-15T08:00:00",
                "time_period": "morning",
                "sleep_quality": "Good",
                "focus_today": "Complete project proposal",
                "energy_level": "High",
                "day_of_week": "Monday",
                "checkin_hour": 8
            },
            {
                "timestamp": "2024-01-15T14:00:00",
                "time_period": "afternoon",
                "day_progress": "Good",
                "adjust_plan": "No changes needed",
                "take_break": "No, I'm in the zone",
                "day_of_week": "Monday",
                "checkin_hour": 14
            },
            {
                "timestamp": "2024-01-15T20:00:00",
                "time_period": "evening",
                "accomplishments": "Completed project proposal",
                "challenges": "Had some technical difficulties",
                "current_feeling": "Accomplished",
                "day_of_week": "Monday",
                "checkin_hour": 20
            }
        ]
        
        self.assistant = FocusAssistant(
            self.user_profile,
            self.sample_mood_data,
            self.sample_checkin_data
        )
    
    def test_initialization(self):
        """Test FocusAssistant initialization"""
        self.assertEqual(self.assistant.user_goal, "Improve focus and productivity")
        self.assertEqual(self.assistant.user_tone, "Gentle & supportive")
        self.assertEqual(len(self.assistant.mood_data), 3)
        self.assertEqual(len(self.assistant.checkin_data), 3)
    
    def test_analyze_mood_patterns_with_data(self):
        """Test mood pattern analysis with sample data"""
        analysis = self.assistant.analyze_mood_patterns()
        
        # Check that analysis contains expected keys
        self.assertIn("insights", analysis)
        self.assertIn("patterns", analysis)
        self.assertIn("best_day", analysis)
        self.assertIn("recent_trend", analysis)
        
        # Check that patterns are generated
        self.assertIsInstance(analysis["patterns"], list)
        self.assertIsInstance(analysis["insights"], list)
    
    def test_analyze_mood_patterns_empty_data(self):
        """Test mood pattern analysis with empty data"""
        empty_assistant = FocusAssistant(self.user_profile, [], [])
        analysis = empty_assistant.analyze_mood_patterns()
        
        self.assertEqual(analysis["insights"], [])
        self.assertEqual(analysis["patterns"], [])
        self.assertIsNone(analysis["best_day"])
        self.assertIsNone(analysis["best_hour"])
    
    def test_analyze_checkin_patterns_with_data(self):
        """Test check-in pattern analysis with sample data"""
        analysis = self.assistant.analyze_checkin_patterns()
        
        # Check that analysis contains expected keys
        self.assertIn("insights", analysis)
        self.assertIn("recommendations", analysis)
        self.assertIn("sleep_quality", analysis)
        self.assertIn("energy_level", analysis)
        
        # Check that insights are generated
        self.assertIsInstance(analysis["insights"], list)
        self.assertIsInstance(analysis["recommendations"], list)
    
    def test_analyze_checkin_patterns_empty_data(self):
        """Test check-in pattern analysis with empty data"""
        empty_assistant = FocusAssistant(self.user_profile, [], [])
        analysis = empty_assistant.analyze_checkin_patterns()
        
        self.assertEqual(analysis["insights"], [])
        self.assertEqual(analysis["recommendations"], [])
    
    def test_generate_daily_recommendation(self):
        """Test daily recommendation generation"""
        recommendation = self.assistant.generate_daily_recommendation()
        
        # Check that recommendation is a string
        self.assertIsInstance(recommendation, str)
        self.assertGreater(len(recommendation), 0)
        
        # Check that it contains goal reference
        self.assertIn("Improve focus and productivity", recommendation)
    
    def test_get_weekly_summary(self):
        """Test weekly summary generation"""
        summary = self.assistant.get_weekly_summary()
        
        # Check that summary contains expected keys
        self.assertIn("mood_entries", summary)
        self.assertIn("checkin_entries", summary)
        self.assertIn("mood_trend", summary)
        self.assertIn("insights", summary)
        self.assertIn("recommendations", summary)
        
        # Check that counts are correct
        self.assertEqual(summary["mood_entries"], 3)
        self.assertEqual(summary["checkin_entries"], 3)
    
    def test_get_personalized_greeting(self):
        """Test personalized greeting generation"""
        greeting = self.assistant.get_personalized_greeting()
        
        # Check that greeting is a string
        self.assertIsInstance(greeting, str)
        self.assertGreater(len(greeting), 0)
        
        # Check that it contains goal reference
        self.assertIn("Improve focus and productivity", greeting)
        
        # Check that it contains appropriate greeting based on time
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            self.assertIn("Good morning", greeting)
        elif 12 <= current_hour < 18:
            self.assertIn("Good afternoon", greeting)
        else:
            self.assertIn("Good evening", greeting)
    
    def test_get_morning_analysis_data(self):
        """Test morning analysis data preparation"""
        current_checkin = {
            "timestamp": "2024-01-16T08:00:00",
            "time_period": "morning",
            "sleep_quality": "Good",
            "focus_today": "Test focus",
            "energy_level": "High"
        }
        
        analysis_data = self.assistant.get_morning_analysis_data(current_checkin)
        
        # Check that analysis data contains expected keys
        self.assertIn("previous_evening", analysis_data)
        self.assertIn("current_checkin", analysis_data)
        self.assertIn("sleep_analysis", analysis_data)
        self.assertIn("energy_analysis", analysis_data)
        self.assertIn("focus_suggestions", analysis_data)
        self.assertIn("wellness_tips", analysis_data)
        
        # Check that current check-in is included
        self.assertEqual(analysis_data["current_checkin"], current_checkin)
        
        # Check that previous evening is found
        self.assertIsNotNone(analysis_data["previous_evening"])
        self.assertEqual(analysis_data["previous_evening"]["time_period"], "evening")
    
    def test_get_afternoon_analysis_data(self):
        """Test afternoon analysis data preparation"""
        current_checkin = {
            "timestamp": "2024-01-16T14:00:00",
            "time_period": "afternoon",
            "day_progress": "Good",
            "adjust_plan": "No changes",
            "take_break": "Maybe later"
        }
        
        analysis_data = self.assistant.get_afternoon_analysis_data(current_checkin)
        
        # Check that analysis data contains expected keys
        self.assertIn("morning_checkin", analysis_data)
        self.assertIn("current_checkin", analysis_data)
        self.assertIn("progress_analysis", analysis_data)
        self.assertIn("energy_changes", analysis_data)
        self.assertIn("plan_adjustments", analysis_data)
        self.assertIn("break_recommendations", analysis_data)
        
        # Check that current check-in is included
        self.assertEqual(analysis_data["current_checkin"], current_checkin)
    
    def test_get_evening_analysis_data(self):
        """Test evening analysis data preparation"""
        current_checkin = {
            "timestamp": "2024-01-16T20:00:00",
            "time_period": "evening",
            "accomplishments": "Test accomplishments",
            "challenges": "Test challenges",
            "current_feeling": "Good"
        }
        
        analysis_data = self.assistant.get_evening_analysis_data(current_checkin)
        
        # Check that analysis data contains expected keys
        self.assertIn("daily_journey", analysis_data)
        self.assertIn("current_checkin", analysis_data)
        self.assertIn("daily_patterns", analysis_data)
        self.assertIn("emotional_analysis", analysis_data)
        self.assertIn("tomorrow_preparation", analysis_data)
        self.assertIn("sleep_preparation", analysis_data)
        
        # Check that current check-in is included
        self.assertEqual(analysis_data["current_checkin"], current_checkin)
    
    def test_get_daily_summary_data(self):
        """Test daily summary data preparation"""
        summary_data = self.assistant.get_daily_summary_data()
        
        # Check that summary data contains expected keys
        self.assertIn("complete_daily_data", summary_data)
        self.assertIn("mood_analysis", summary_data)
        self.assertIn("checkin_analysis", summary_data)
        self.assertIn("goal_progress", summary_data)
        self.assertIn("wellness_assessment", summary_data)
        self.assertIn("growth_insights", summary_data)
    
    def test_analyze_sleep_patterns(self):
        """Test sleep pattern analysis"""
        sleep_analysis = self.assistant._analyze_sleep_patterns()
        
        # Check that analysis contains expected keys
        self.assertIn("average_quality", sleep_analysis)
        self.assertIn("trend", sleep_analysis)
        self.assertIn("recommendations", sleep_analysis)
        
        # Check that average quality is calculated
        self.assertIsInstance(sleep_analysis["average_quality"], (int, float))
        self.assertGreater(sleep_analysis["average_quality"], 0)
    
    def test_analyze_morning_energy_patterns(self):
        """Test morning energy pattern analysis"""
        energy_analysis = self.assistant._analyze_morning_energy_patterns()
        
        # Check that analysis contains expected keys
        self.assertIn("average_energy", energy_analysis)
        self.assertIn("trend", energy_analysis)
        self.assertIn("recommendations", energy_analysis)
        
        # Check that average energy is calculated
        self.assertIsInstance(energy_analysis["average_energy"], (int, float))
        self.assertGreater(energy_analysis["average_energy"], 0)
    
    def test_generate_focus_suggestions(self):
        """Test focus suggestion generation"""
        high_energy_checkin = {"energy_level": "High"}
        low_energy_checkin = {"energy_level": "Low"}
        
        high_energy_suggestions = self.assistant._generate_focus_suggestions(high_energy_checkin)
        low_energy_suggestions = self.assistant._generate_focus_suggestions(low_energy_checkin)
        
        # Check that suggestions are generated
        self.assertIsInstance(high_energy_suggestions, list)
        self.assertIsInstance(low_energy_suggestions, list)
        self.assertGreater(len(high_energy_suggestions), 0)
        self.assertGreater(len(low_energy_suggestions), 0)
        
        # Check that suggestions are different for different energy levels
        self.assertNotEqual(high_energy_suggestions, low_energy_suggestions)
    
    def test_generate_morning_wellness_tips(self):
        """Test morning wellness tip generation"""
        good_sleep_checkin = {"sleep_quality": "Good"}
        poor_sleep_checkin = {"sleep_quality": "Poor"}
        
        good_sleep_tips = self.assistant._generate_morning_wellness_tips(good_sleep_checkin)
        poor_sleep_tips = self.assistant._generate_morning_wellness_tips(poor_sleep_checkin)
        
        # Check that tips are generated
        self.assertIsInstance(good_sleep_tips, list)
        self.assertIsInstance(poor_sleep_tips, list)
        self.assertGreater(len(good_sleep_tips), 0)
        self.assertGreater(len(poor_sleep_tips), 0)
        
        # Check that poor sleep gets additional tips
        self.assertGreaterEqual(len(poor_sleep_tips), len(good_sleep_tips))
    
    def test_analyze_progress_patterns(self):
        """Test progress pattern analysis"""
        morning_checkin = {"focus_today": "Test focus"}
        good_progress_checkin = {"day_progress": "Good"}
        challenging_progress_checkin = {"day_progress": "Challenging"}
        
        good_analysis = self.assistant._analyze_progress_patterns(morning_checkin, good_progress_checkin)
        challenging_analysis = self.assistant._analyze_progress_patterns(morning_checkin, challenging_progress_checkin)
        
        # Check that analysis contains expected keys
        self.assertIn("progress_level", good_analysis)
        self.assertIn("insights", good_analysis)
        self.assertIn("adjustments", good_analysis)
        
        # Check that progress levels are correct
        self.assertEqual(good_analysis["progress_level"], "Good")
        self.assertEqual(challenging_analysis["progress_level"], "Challenging")
    
    def test_analyze_energy_changes(self):
        """Test energy change analysis"""
        morning_checkin = {"energy_level": "High"}
        good_progress_checkin = {"day_progress": "Good"}
        challenging_progress_checkin = {"day_progress": "Challenging"}
        
        good_analysis = self.assistant._analyze_energy_changes(morning_checkin, good_progress_checkin)
        challenging_analysis = self.assistant._analyze_energy_changes(morning_checkin, challenging_progress_checkin)
        
        # Check that analysis contains expected keys
        self.assertIn("energy_trend", good_analysis)
        self.assertIn("insights", good_analysis)
        self.assertIn("maintenance_tips", good_analysis)
        
        # Check that trends are different
        self.assertNotEqual(good_analysis["energy_trend"], challenging_analysis["energy_trend"])
    
    def test_generate_plan_adjustments(self):
        """Test plan adjustment generation"""
        good_progress_checkin = {"day_progress": "Good"}
        challenging_progress_checkin = {"day_progress": "Challenging"}
        
        good_adjustments = self.assistant._generate_plan_adjustments(None, good_progress_checkin)
        challenging_adjustments = self.assistant._generate_plan_adjustments(None, challenging_progress_checkin)
        
        # Check that adjustments are generated
        self.assertIsInstance(good_adjustments, list)
        self.assertIsInstance(challenging_adjustments, list)
        self.assertGreater(len(good_adjustments), 0)
        self.assertGreater(len(challenging_adjustments), 0)
    
    def test_generate_break_recommendations(self):
        """Test break recommendation generation"""
        need_break_checkin = {"take_break": "Yes, I need a break"}
        in_zone_checkin = {"take_break": "No, I'm in the zone"}
        maybe_later_checkin = {"take_break": "Maybe later"}
        
        need_break_recs = self.assistant._generate_break_recommendations(need_break_checkin)
        in_zone_recs = self.assistant._generate_break_recommendations(in_zone_checkin)
        maybe_later_recs = self.assistant._generate_break_recommendations(maybe_later_checkin)
        
        # Check that recommendations are generated
        self.assertIsInstance(need_break_recs, list)
        self.assertIsInstance(in_zone_recs, list)
        self.assertIsInstance(maybe_later_recs, list)
        self.assertGreater(len(need_break_recs), 0)
        self.assertGreater(len(in_zone_recs), 0)
        self.assertGreater(len(maybe_later_recs), 0)
    
    def test_get_today_journey(self):
        """Test today's journey compilation"""
        journey = self.assistant._get_today_journey()
        
        # Check that journey contains expected keys
        self.assertIn("morning", journey)
        self.assertIn("afternoon", journey)
        self.assertIn("evening", journey)
        self.assertIn("complete", journey)
        
        # Check that complete flag is correct
        self.assertTrue(journey["complete"])  # We have all three check-ins for the same day
    
    def test_analyze_daily_patterns(self):
        """Test daily pattern analysis"""
        journey = self.assistant._get_today_journey()
        patterns = self.assistant._analyze_daily_patterns(journey)
        
        # Check that patterns contains expected keys
        self.assertIn("energy_flow", patterns)
        self.assertIn("productivity_curve", patterns)
        self.assertIn("challenges", patterns)
        self.assertIn("successes", patterns)
        
        # Check that patterns are lists
        self.assertIsInstance(patterns["challenges"], list)
        self.assertIsInstance(patterns["successes"], list)
    
    def test_analyze_emotional_patterns(self):
        """Test emotional pattern analysis"""
        accomplished_checkin = {"current_feeling": "Accomplished"}
        stressed_checkin = {"current_feeling": "Stressed"}
        
        accomplished_analysis = self.assistant._analyze_emotional_patterns(accomplished_checkin)
        stressed_analysis = self.assistant._analyze_emotional_patterns(stressed_checkin)
        
        # Check that analysis contains expected keys
        self.assertIn("emotional_state", accomplished_analysis)
        self.assertIn("processing_needs", accomplished_analysis)
        self.assertIn("coping_strategies", accomplished_analysis)
        
        # Check that emotional states are correct
        self.assertEqual(accomplished_analysis["emotional_state"], "Accomplished")
        self.assertEqual(stressed_analysis["emotional_state"], "Stressed")
    
    def test_generate_tomorrow_preparation(self):
        """Test tomorrow preparation generation"""
        journey = self.assistant._get_today_journey()
        good_feeling_checkin = {"current_feeling": "Good"}
        tired_feeling_checkin = {"current_feeling": "Tired"}
        
        good_preparation = self.assistant._generate_tomorrow_preparation(journey, good_feeling_checkin)
        tired_preparation = self.assistant._generate_tomorrow_preparation(journey, tired_feeling_checkin)
        
        # Check that preparation suggestions are generated
        self.assertIsInstance(good_preparation, list)
        self.assertIsInstance(tired_preparation, list)
        self.assertGreater(len(good_preparation), 0)
        self.assertGreater(len(tired_preparation), 0)
    
    def test_generate_sleep_preparation(self):
        """Test sleep preparation generation"""
        good_feeling_checkin = {"current_feeling": "Good"}
        stressed_feeling_checkin = {"current_feeling": "Stressed"}
        
        good_sleep_tips = self.assistant._generate_sleep_preparation(good_feeling_checkin)
        stressed_sleep_tips = self.assistant._generate_sleep_preparation(stressed_feeling_checkin)
        
        # Check that sleep tips are generated
        self.assertIsInstance(good_sleep_tips, list)
        self.assertIsInstance(stressed_sleep_tips, list)
        self.assertGreater(len(good_sleep_tips), 0)
        self.assertGreater(len(stressed_sleep_tips), 0)
        
        # Check that stressed feeling gets additional tips
        self.assertGreaterEqual(len(stressed_sleep_tips), len(good_sleep_tips))
    
    def test_analyze_goal_progress(self):
        """Test goal progress analysis"""
        journey = self.assistant._get_today_journey()
        progress = self.assistant._analyze_goal_progress(journey)
        
        # Check that progress contains expected keys
        self.assertIn("progress_indicators", progress)
        self.assertIn("challenges", progress)
        self.assertIn("overall_progress", progress)
        
        # Check that progress indicators and challenges are lists
        self.assertIsInstance(progress["progress_indicators"], list)
        self.assertIsInstance(progress["challenges"], list)
    
    def test_analyze_daily_wellness(self):
        """Test daily wellness analysis"""
        journey = self.assistant._get_today_journey()
        wellness = self.assistant._analyze_daily_wellness(journey)
        
        # Check that wellness contains expected keys
        self.assertIn("wellness_indicators", wellness)
        self.assertIn("stress_points", wellness)
        self.assertIn("overall_wellness", wellness)
        
        # Check that indicators and stress points are lists
        self.assertIsInstance(wellness["wellness_indicators"], list)
        self.assertIsInstance(wellness["stress_points"], list)
    
    def test_generate_growth_insights(self):
        """Test growth insight generation"""
        journey = self.assistant._get_today_journey()
        insights = self.assistant._generate_growth_insights(journey)
        
        # Check that insights are generated
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)


if __name__ == '__main__':
    unittest.main()
