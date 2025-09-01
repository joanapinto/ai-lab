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
from .ai_cache import ai_cache, PromptOptimizer

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
        # Admin user bypass - unlimited access for testing
        ADMIN_EMAIL = "joanapnpinto@gmail.com"
        if user_email == ADMIN_EMAIL:
            return True, "Admin user - unlimited access"
        
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
        
        # Check cache first
        if user_email:
            cached_response = ai_cache.get_cached_response("greeting", user_email, recent_data)
            if cached_response:
                return cached_response

        # Use optimized prompt
        prompt = PromptOptimizer.optimize_greeting_prompt(user_profile, recent_data)
        
        try:
            # Show enhanced loading feedback
            with st.spinner("🤖 AI is crafting your personalized greeting..."):
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
            
            # Cache the response
            if user_email:
                ai_cache.cache_response("greeting", user_email, recent_data, result)
            
            # Record the API call with detailed information
            tokens_used = response.usage.total_tokens if response.usage else None
            cost_usd = (tokens_used * 0.000002) if tokens_used else None  # GPT-3.5-turbo pricing
            
            self.usage_limiter.record_api_call(
                user_email=user_email,
                feature="greeting",
                tokens_used=tokens_used,
                cost_usd=cost_usd
            )
            
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
            # Show enhanced loading feedback
            with st.spinner("🤖 AI is crafting your daily encouragement..."):
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
            
            # Record the API call with detailed information
            tokens_used = response.usage.total_tokens if response.usage else None
            cost_usd = (tokens_used * 0.000002) if tokens_used else None  # GPT-3.5-turbo pricing
            
            self.usage_limiter.record_api_call(
                user_email=user_email,
                feature="encouragement",
                tokens_used=tokens_used,
                cost_usd=cost_usd
            )
            
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
            # Show enhanced loading feedback
            with st.spinner("🤖 AI is crafting your personalized productivity tip..."):
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
            
            # Record the API call with detailed information
            tokens_used = response.usage.total_tokens if response.usage else None
            cost_usd = (tokens_used * 0.000002) if tokens_used else None  # GPT-3.5-turbo pricing
            
            self.usage_limiter.record_api_call(
                user_email=user_email,
                feature="productivity_tip",
                tokens_used=tokens_used,
                cost_usd=cost_usd
            )
            
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

    def generate_weekly_summary(self, user_profile: Dict, week_analysis: Dict, user_email: str = None) -> str:
        """Generate personalized weekly summary"""
        # Check if we can use this feature
        can_use, reason = self.can_use_feature("weekly_summary", user_email)
        if not can_use:
            st.warning(f"🤖 Weekly summary limited: {reason}")
            return None

        # Prepare comprehensive context for the AI
        total_checkins = week_analysis['total_checkins']
        total_moods = week_analysis['total_mood_entries']
        
        # Find most active day
        day_counts = {}
        for day in week_analysis['checkin_days']:
            day_counts[day] = day_counts.get(day, 0) + 1
        most_active_day = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else None
        
        # Find highest energy day
        highest_energy_day = None
        highest_energy = 0
        for day, energies in week_analysis['energy_patterns'].items():
            energy_scores = []
            for energy in energies:
                if energy == 'High': energy_scores.append(5)
                elif energy == 'Good': energy_scores.append(4)
                elif energy == 'Moderate': energy_scores.append(3)
                elif energy == 'Low': energy_scores.append(2)
                elif energy == 'Very low': energy_scores.append(1)
            
            if energy_scores:
                avg_energy = sum(energy_scores) / len(energy_scores)
                if avg_energy > highest_energy:
                    highest_energy = avg_energy
                    highest_energy_day = day
        
        # Find most common mood
        all_moods = []
        for day_data in week_analysis['mood_patterns'].values():
            all_moods.extend(day_data['moods'])
        most_common_mood = max(set(all_moods), key=all_moods.count) if all_moods else None
        
        # Calculate average mood intensity
        all_intensities = []
        for day_data in week_analysis['mood_patterns'].values():
            all_intensities.extend(day_data['intensities'])
        avg_mood_intensity = sum(all_intensities) / len(all_intensities) if all_intensities else 5
        
        # Check cache first
        if user_email:
            cached_response = ai_cache.get_cached_response("weekly_summary", user_email, week_analysis)
            if cached_response:
                return cached_response

        # Use optimized prompt
        prompt = PromptOptimizer.optimize_weekly_summary_prompt(user_profile, week_analysis)

        try:
            # Show enhanced loading feedback
            with st.spinner("🤖 AI is analyzing your weekly patterns and crafting personalized insights..."):
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a supportive wellness coach who celebrates progress and provides encouraging insights."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=400,
                    temperature=0.8
                )
            result = response.choices[0].message.content.strip()
            
            # Cache the response
            if user_email:
                ai_cache.cache_response("weekly_summary", user_email, week_analysis, result)
            
            # Record the API call with detailed information
            tokens_used = response.usage.total_tokens if response.usage else None
            cost_usd = (tokens_used * 0.000002) if tokens_used else None  # GPT-3.5-turbo pricing
            
            self.usage_limiter.record_api_call(
                user_email=user_email,
                feature="weekly_summary",
                tokens_used=tokens_used,
                cost_usd=cost_usd
            )
            
            return result
            
        except Exception as e:
            st.error(f"Error generating weekly summary: {str(e)}")
            return None

    def generate_ai_task_plan(self, user_profile: Dict, checkin_data: Dict, mood_data: List[Dict], user_email: str = None) -> Dict:
        """Generate AI-powered personalized task plan"""
        # Check if we can use this feature
        can_use, reason = self.can_use_feature("task_planning", user_email)
        if not can_use:
            st.warning(f"🤖 AI task planning limited: {reason}")
            return None

        # Prepare comprehensive context for the AI
        current_time = datetime.now()
        current_hour = current_time.hour
        
        # Determine time period
        if 5 <= current_hour < 12:
            time_period = "morning"
        elif 12 <= current_hour < 18:
            time_period = "afternoon"
        else:
            time_period = "evening"
        
        # Get recent context
        recent_moods = mood_data[-3:] if mood_data else []
        
        # Handle checkin_data - it could be a list of all checkins or a single checkin dict
        if isinstance(checkin_data, list):
            recent_checkins = checkin_data[-2:] if checkin_data else []
        else:
            # If it's a single checkin dict, we don't have recent checkins for context
            recent_checkins = []
        
        # Build comprehensive context
        context = {
            'time_period': time_period,
            'current_hour': current_hour,
            'user_goal': user_profile.get('goal', 'Improve focus and productivity'),
            'user_tone': user_profile.get('tone', 'Friendly'),
            'availability': user_profile.get('availability', '2-4 hours'),
            'energy_drainers': user_profile.get('energy_drainers', []),
            'joy_sources': user_profile.get('joy_sources', []),
            'situation': user_profile.get('situation', 'Not specified'),
            'small_habit': user_profile.get('small_habit', ''),
            'current_checkin': checkin_data,
            'recent_moods': recent_moods,
            'recent_checkins': recent_checkins,
            'all_checkins': checkin_data if isinstance(checkin_data, list) else [],
            'focus_today': checkin_data.get('focus_today', 'Not specified'),
            'energy_level': checkin_data.get('energy_level', 'Not specified'),
            'current_feeling': checkin_data.get('current_feeling', 'Not specified'),
            'sleep_quality': checkin_data.get('sleep_quality', 'Not specified'),
            'day_progress': checkin_data.get('day_progress', 'Not specified')
        }

        # Check cache first
        if user_email:
            cached_response = ai_cache.get_cached_response("task_planning", user_email, context)
            if cached_response:
                try:
                    import json
                    return json.loads(cached_response)
                except:
                    pass

        # Generate AI prompt for task planning
        prompt = f"""
You are an expert productivity coach and life strategist who creates deeply personalized, thoughtful daily plans. Your goal is to help users feel empowered, not overwhelmed, while making meaningful progress toward their goals.

USER CONTEXT:
- Primary Goal: {context['user_goal']}
- Communication Style: {context['user_tone']}
- Available Time: {context['availability']}
- Current Time: {context['time_period']} ({current_hour}:00)
- Life Situation: {context['situation']}

CURRENT STATE ANALYSIS:
- Sleep Quality: {checkin_data.get('sleep_quality', 'Not specified')}
- Energy Level: {checkin_data.get('energy_level', 'Not specified')}
- Emotional State: {checkin_data.get('current_feeling', 'Not specified')}
- Day Progress: {checkin_data.get('day_progress', 'Not specified')}
- Main Focus: {checkin_data.get('focus_today', 'Not specified')}

PERSONAL PREFERENCES & PATTERNS:
- Energy Drainers (Avoid): {context['energy_drainers']}
- Joy Sources (Incorporate): {context['joy_sources']}
- Small Habit: {context['small_habit']}
- Recent Mood Pattern: {[m.get('mood', 'Unknown') for m in recent_moods]}
- Recent Energy Pattern: {[c.get('energy_level', 'Unknown') for c in recent_checkins]}

DEEP PLANNING APPROACH:
1. **Energy-Aware Task Design**: Match task complexity to their current energy level
2. **Emotional Intelligence**: Consider their emotional state and provide appropriate support
3. **Goal Alignment**: Break down their main focus into manageable, meaningful steps
4. **Joy Integration**: Weave in their joy sources naturally to boost motivation
5. **Overwhelm Prevention**: Structure tasks to feel achievable, not daunting
6. **Progress Momentum**: Design tasks that build on each other and create a sense of accomplishment
7. **Flexibility**: Account for their availability and life situation

TASK BREAKDOWN STRATEGY:
- **High Energy + Good Sleep**: Focus on complex, creative, or challenging tasks
- **Moderate Energy**: Mix of focused work and lighter activities
- **Low Energy**: Gentle, restorative activities that still move them forward
- **Poor Sleep**: Extra gentle approach with lots of self-care
- **Stressed/Overwhelmed**: Focus on calming, grounding activities first
- **Motivated/Accomplished**: Build on momentum with next-level tasks

CREATE A PERSONALIZED {context['time_period'].upper()} PLAN THAT:
1. **Deeply reflects their specific focus** - Break down their main goal into 3-5 thoughtful, actionable steps
2. **Matches their energy perfectly** - Tasks should feel right for their current state
3. **Incorporates their joy sources naturally** - Use what energizes them to boost motivation
4. **Avoids their energy drainers** - Steer clear of what depletes them
5. **Prevents overwhelm** - Structure tasks to feel achievable and satisfying
6. **Builds momentum** - Each task should naturally lead to the next
7. **Provides emotional support** - Consider their feelings and offer appropriate encouragement

FORMAT: Return a JSON object with:
{{
    "tasks": [
        "Specific, actionable task that directly relates to their focus",
        "Next logical step that builds on the first",
        "Task that incorporates their joy sources",
        "Task that moves them toward their goal",
        "Optional: Small habit or self-care task"
    ],
    "recommendations": [
        "Specific advice for their current energy/emotional state",
        "Strategy to avoid their energy drainers",
        "Encouragement that matches their tone preference"
    ],
    "estimated_duration": "Realistic time estimate based on their availability",
    "priority_order": "energy_based or goal_based",
    "personalized_note": "Thoughtful, encouraging message that acknowledges their specific situation and feelings"
}}

IMPORTANT: Make each task specific to their stated focus. If they want to "work on project X," don't give generic tasks - break down what "working on project X" actually means for them right now. Consider their energy level, emotional state, and make the plan feel like it was crafted specifically for them in this moment.
"""

        try:
            # Show enhanced loading feedback
            with st.spinner(f"🤖 AI is crafting your personalized {context['time_period']} plan..."):
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert productivity coach and life strategist with deep empathy and understanding of human psychology. You specialize in creating thoughtful, personalized daily plans that help people feel empowered and make meaningful progress without feeling overwhelmed. You understand that productivity is deeply personal and varies greatly based on energy, emotions, life circumstances, and individual preferences. Your goal is to craft plans that feel like they were made specifically for this person in this moment."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=600,
                    temperature=0.7
                )
                
                result = response.choices[0].message.content.strip()
                
                # Parse JSON response
                try:
                    import json
                    task_plan = json.loads(result)
                    
                    # Cache the response
                    if user_email:
                        ai_cache.cache_response("task_planning", user_email, context, result)
                    
                    # Record the API call
                    tokens_used = response.usage.total_tokens if response.usage else None
                    cost_usd = (tokens_used * 0.000002) if tokens_used else None
                    
                    self.usage_limiter.record_api_call(
                        user_email=user_email,
                        feature="task_planning",
                        tokens_used=tokens_used,
                        cost_usd=cost_usd
                    )
                    
                    return task_plan
                    
                except json.JSONDecodeError:
                    st.error("Error parsing AI task plan response")
                    return None
                
        except Exception as e:
            st.error(f"Error generating AI task plan: {str(e)}")
            return None 