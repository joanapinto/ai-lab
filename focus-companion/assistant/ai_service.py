"""
AI Service for Focus Companion
Handles OpenAI API calls for personalized responses
"""

import os
import openai
from typing import Dict, List, Optional
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from .prompts import PromptTemplates
from .usage_limiter import UsageLimiter

# Load environment variables
load_dotenv()

class AIService:
    """Service for handling AI-powered responses"""
    
    def __init__(self):
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            st.warning("⚠️ OpenAI API key not found. AI features will be disabled.")
            self.client = None
        else:
            self.client = openai.OpenAI(api_key=api_key)
        
        # Initialize usage limiter
        self.usage_limiter = UsageLimiter()
    
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return self.client is not None
    
    def can_use_feature(self, feature: str, user_email: str = None) -> tuple[bool, str]:
        """
        Check if a feature can be used based on limits
        Returns (allowed, reason)
        """
        if not self.is_available():
            return False, "AI service not available"
        
        # Check if feature is enabled
        if not self.usage_limiter.is_feature_enabled(feature, user_email):
            return False, f"Feature '{feature}' is disabled for beta testing"
        
        # Check usage limits
        return self.usage_limiter.can_make_api_call(user_email)
    
    def generate_personalized_greeting(self, user_profile: Dict, mood_data: List[Dict], 
                                     checkin_data: List[Dict], user_email: str = None) -> str:
        """Generate a personalized AI greeting"""
        # Check if we can use this feature
        can_use, reason = self.can_use_feature("greeting", user_email)
        if not can_use:
            st.warning(f"🤖 AI greeting limited: {reason}")
            return None
        
        # Prepare context for the AI
        current_time = datetime.now()
        current_hour = current_time.hour
        
        # Determine time of day
        if 5 <= current_hour < 12:
            time_context = "morning"
        elif 12 <= current_hour < 18:
            time_context = "afternoon"
        else:
            time_context = "evening"
        
        # Get recent mood data (last 3 entries)
        recent_moods = mood_data[-3:] if mood_data else []
        mood_summary = ""
        if recent_moods:
            avg_mood = sum(m['intensity'] for m in recent_moods) / len(recent_moods)
            if avg_mood >= 7:
                mood_summary = "You've been in a positive mood recently"
            elif avg_mood >= 5:
                mood_summary = "Your mood has been stable"
            else:
                mood_summary = "You've been experiencing some challenges"
        
        # Get recent check-in patterns
        recent_checkins = checkin_data[-2:] if checkin_data else []
        checkin_summary = ""
        if recent_checkins:
            energy_levels = [c.get('energy_level', 'Unknown') for c in recent_checkins if 'energy_level' in c]
            if energy_levels:
                most_common_energy = max(set(energy_levels), key=energy_levels.count)
                checkin_summary = f"Your energy has been {most_common_energy.lower()}"
        
        # Use the existing prompt template for daily recommendations
        recent_data = {
            'time_context': time_context,
            'mood_summary': mood_summary,
            'checkin_summary': checkin_summary,
            'recent_moods': recent_moods,
            'recent_checkins': recent_checkins
        }
        
        prompt = PromptTemplates.daily_recommendation_prompt(user_profile, recent_data)
        
        # Add specific greeting instructions
        prompt += "\n\nPlease respond with a warm, personalized greeting (1-2 sentences) that acknowledges their current situation and recent patterns. Keep it concise and natural."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a supportive, encouraging assistant focused on helping users achieve their goals."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            result = response.choices[0].message.content.strip()
            
            # Record the API call
            self.usage_limiter.record_api_call(user_email)
            
            return result
            
        except Exception as e:
            st.error(f"Error generating AI greeting: {str(e)}")
            return None
    
    def generate_daily_encouragement(self, user_profile: Dict, mood_data: List[Dict], 
                                   checkin_data: List[Dict], user_email: str = None) -> str:
        """Generate personalized daily encouragement"""
        # Check if we can use this feature
        can_use, reason = self.can_use_feature("encouragement", user_email)
        if not can_use:
            st.warning(f"🤖 AI encouragement limited: {reason}")
            return None
        
        # Prepare recent data for analysis
        recent_data = {
            'mood_data': mood_data[-3:] if mood_data else [],
            'checkin_data': checkin_data[-3:] if checkin_data else [],
            'goal': user_profile.get('goal', 'Improve focus and productivity'),
            'tone': user_profile.get('tone', 'Gentle & Supportive')
        }
        
        # Use the existing prompt template for goal progress analysis
        progress_data = {
            'recent_moods': recent_data['mood_data'],
            'recent_checkins': recent_data['checkin_data'],
            'energy_trend': self._analyze_energy_trend(checkin_data),
            'mood_trend': self._analyze_mood_trend(mood_data)
        }
        
        prompt = PromptTemplates.goal_progress_prompt(user_profile.get('goal', 'Improve focus and productivity'), progress_data)
        
        # Add specific encouragement instructions
        prompt += "\n\nPlease provide an encouraging message (1-2 sentences) that acknowledges their progress and motivates them to continue. Keep it concise and personal."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an encouraging, supportive assistant helping users stay motivated."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=80,
                temperature=0.7
            )
            
            result = response.choices[0].message.content.strip()
            
            # Record the API call
            self.usage_limiter.record_api_call(user_email)
            
            return result
            
        except Exception as e:
            st.error(f"Error generating AI encouragement: {str(e)}")
            return None
    
    def generate_productivity_tip(self, user_profile: Dict, mood_data: List[Dict], 
                                checkin_data: List[Dict], user_email: str = None) -> str:
        """Generate a personalized productivity tip"""
        # Check if we can use this feature
        can_use, reason = self.can_use_feature("productivity_tip", user_email)
        if not can_use:
            st.warning(f"🤖 AI productivity tip limited: {reason}")
            return None
        
        # Prepare all data for comprehensive analysis
        all_data = {
            'user_profile': user_profile,
            'mood_data': mood_data[-7:] if mood_data else [],  # Last week
            'checkin_data': checkin_data[-7:] if checkin_data else [],  # Last week
            'energy_drainers': user_profile.get('energy_drainers', []),
            'situation': user_profile.get('situation', 'Not specified'),
            'availability': user_profile.get('availability', '1–2 hours')
        }
        
        # Use the existing prompt template for productivity insights
        prompt = PromptTemplates.productivity_insights_prompt(all_data)
        
        # Add specific tip instructions
        prompt += "\n\nPlease provide one specific, actionable productivity tip that considers their current situation and energy drainers. Keep it practical and implementable."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a productivity expert providing practical, personalized advice."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=60,
                temperature=0.7
            )
            
            result = response.choices[0].message.content.strip()
            
            # Record the API call
            self.usage_limiter.record_api_call(user_email)
            
            return result
            
        except Exception as e:
            st.error(f"Error generating AI productivity tip: {str(e)}")
            return None
    
    def _analyze_energy_trend(self, checkin_data: List[Dict]) -> str:
        """Analyze energy trend from check-in data"""
        if not checkin_data:
            return "No recent data"
        
        recent_checkins = checkin_data[-3:]
        energy_levels = [c.get('energy_level', 'Unknown') for c in recent_checkins if 'energy_level' in c]
        
        if not energy_levels:
            return "No energy data available"
        
        if len(set(energy_levels)) == 1:
            return f"Consistently {energy_levels[0].lower()}"
        else:
            return "Varying energy levels"
    
    def _analyze_mood_trend(self, mood_data: List[Dict]) -> str:
        """Analyze mood trend from mood data"""
        if not mood_data:
            return "No recent data"
        
        recent_moods = mood_data[-3:]
        avg_mood = sum(m.get('intensity', 5) for m in recent_moods) / len(recent_moods)
        
        if avg_mood >= 7:
            return "Positive mood trend"
        elif avg_mood >= 5:
            return "Stable mood"
        else:
            return "Lower mood trend"
    
    def generate_mood_analysis(self, mood_data: List[Dict], user_goal: str) -> str:
        """Generate comprehensive mood analysis using existing prompt template"""
        if not self.is_available():
            return None
        
        prompt = PromptTemplates.mood_analysis_prompt(mood_data, user_goal)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a supportive wellness assistant analyzing mood patterns to help users achieve their goals."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            st.error(f"Error generating mood analysis: {str(e)}")
            return None
    
    def generate_focus_optimization(self, checkin_data: List[Dict], mood_data: List[Dict]) -> str:
        """Generate focus optimization advice using existing prompt template"""
        if not self.is_available():
            return None
        
        prompt = PromptTemplates.focus_optimization_prompt(checkin_data, mood_data)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a productivity expert providing focus optimization advice based on user patterns."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            st.error(f"Error generating focus optimization: {str(e)}")
            return None
    
    def generate_stress_management(self, mood_data: List[Dict], checkin_data: List[Dict]) -> str:
        """Generate stress management advice using existing prompt template"""
        if not self.is_available():
            return None
        
        prompt = PromptTemplates.stress_management_prompt(mood_data, checkin_data)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a wellness expert providing stress management advice based on user patterns."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            st.error(f"Error generating stress management advice: {str(e)}")
            return None 