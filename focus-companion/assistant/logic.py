"""
AI Assistant Logic for Focus Companion
Provides intelligent insights and recommendations based on user data
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd

class FocusAssistant:
    """AI-powered assistant for focus and wellness insights"""
    
    def __init__(self, user_profile: Dict, mood_data: List[Dict], checkin_data: List[Dict]):
        self.user_profile = user_profile
        self.mood_data = mood_data
        self.checkin_data = checkin_data
        self.user_goal = user_profile.get('goal', 'Improve focus and productivity')
        self.user_tone = user_profile.get('tone', 'Gentle & Supportive')
        self.joy_sources = user_profile.get('joy_sources', [])
        self.energy_drainers = user_profile.get('energy_drainers', [])
        self.therapy_coaching = user_profile.get('therapy_coaching', 'No')
        self.availability = user_profile.get('availability', '1–2 hours')
        self.energy = user_profile.get('energy', 'Okay')
        self.emotional_patterns = user_profile.get('emotional_patterns', 'Not sure yet')
        self.small_habit = user_profile.get('small_habit', '')
        self.reminders = user_profile.get('reminders', 'Yes')
        self.situation = user_profile.get('situation', 'Freelancer')
    
    def get_morning_analysis_data(self, current_checkin: Dict) -> Dict:
        """Prepare data for morning check-in analysis"""
        # Get yesterday's evening check-in
        yesterday_evening = None
        if self.checkin_data:
            yesterday = datetime.now().date() - timedelta(days=1)
            yesterday_checkins = [
                checkin for checkin in self.checkin_data
                if datetime.fromisoformat(checkin['timestamp']).date() == yesterday
                and checkin['time_period'] == 'evening'
            ]
            if yesterday_checkins:
                yesterday_evening = yesterday_checkins[0]
        
        # Analyze sleep patterns
        sleep_analysis = self._analyze_sleep_patterns()
        
        # Analyze morning energy patterns
        energy_analysis = self._analyze_morning_energy_patterns()
        
        return {
            "previous_evening": yesterday_evening,
            "current_checkin": current_checkin,
            "sleep_analysis": sleep_analysis,
            "energy_analysis": energy_analysis,
            "focus_suggestions": self._generate_focus_suggestions(current_checkin),
            "wellness_tips": self._generate_morning_wellness_tips(current_checkin)
        }
    
    def get_afternoon_analysis_data(self, current_checkin: Dict) -> Dict:
        """Prepare data for afternoon check-in analysis"""
        # Get today's morning check-in
        today_morning = None
        today_checkins = [
            checkin for checkin in self.checkin_data
            if datetime.fromisoformat(checkin['timestamp']).date() == datetime.now().date()
            and checkin['time_period'] == 'morning'
        ]
        if today_checkins:
            today_morning = today_checkins[0]
        
        # Analyze progress patterns
        progress_analysis = self._analyze_progress_patterns(today_morning, current_checkin)
        
        # Analyze energy changes
        energy_changes = self._analyze_energy_changes(today_morning, current_checkin)
        
        return {
            "morning_checkin": today_morning,
            "current_checkin": current_checkin,
            "progress_analysis": progress_analysis,
            "energy_changes": energy_changes,
            "plan_adjustments": self._generate_plan_adjustments(today_morning, current_checkin),
            "break_recommendations": self._generate_break_recommendations(current_checkin)
        }
    
    def get_evening_analysis_data(self, current_checkin: Dict) -> Dict:
        """Prepare data for evening check-in analysis"""
        # Get today's complete journey
        today_journey = self._get_today_journey()
        
        # Analyze daily patterns
        daily_patterns = self._analyze_daily_patterns(today_journey)
        
        # Analyze emotional patterns
        emotional_analysis = self._analyze_emotional_patterns(current_checkin)
        
        return {
            "daily_journey": today_journey,
            "current_checkin": current_checkin,
            "daily_patterns": daily_patterns,
            "emotional_analysis": emotional_analysis,
            "tomorrow_preparation": self._generate_tomorrow_preparation(today_journey, current_checkin),
            "sleep_preparation": self._generate_sleep_preparation(current_checkin)
        }
    
    def get_daily_summary_data(self) -> Dict:
        """Prepare data for complete daily summary"""
        today_journey = self._get_today_journey()
        mood_analysis = self.analyze_mood_patterns()
        checkin_analysis = self.analyze_checkin_patterns()
        
        return {
            "complete_daily_data": today_journey,
            "mood_analysis": mood_analysis,
            "checkin_analysis": checkin_analysis,
            "goal_progress": self._analyze_goal_progress(today_journey),
            "wellness_assessment": self._analyze_daily_wellness(today_journey),
            "growth_insights": self._generate_growth_insights(today_journey)
        }
    
    def analyze_mood_patterns(self) -> Dict:
        """Analyze mood patterns and provide insights"""
        if not self.mood_data:
            return {"insights": [], "patterns": []}
        
        df = pd.DataFrame(self.mood_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = pd.to_datetime(df['date'])
        
        insights = []
        patterns = []
        
        # Analyze mood by day of week
        df['day_of_week'] = df['timestamp'].dt.day_name()
        day_avg = df.groupby('day_of_week')['intensity'].mean().sort_values(ascending=False)
        
        if not day_avg.empty:
            best_day = day_avg.index[0]
            worst_day = day_avg.index[-1]
            patterns.append(f"You tend to feel best on {best_day}s")
            patterns.append(f"Your mood is typically lower on {worst_day}s")
        
        # Analyze mood by time of day
        df['hour'] = df['timestamp'].dt.hour
        hour_avg = df.groupby('hour')['intensity'].mean()
        
        if not hour_avg.empty:
            best_hour = hour_avg.idxmax()
            worst_hour = hour_avg.idxmin()
            patterns.append(f"Your peak mood time is around {best_hour}:00")
            patterns.append(f"Your mood tends to dip around {worst_hour}:00")
        
        # Recent trend analysis
        recent_data = df[df['timestamp'] > datetime.now() - timedelta(days=7)]
        if not recent_data.empty:
            recent_avg = recent_data['intensity'].mean()
            overall_avg = df['intensity'].mean()
            
            if recent_avg > overall_avg + 1:
                insights.append("🎉 Your mood has been improving recently! Keep up the great work.")
            elif recent_avg < overall_avg - 1:
                insights.append("💙 Your mood has been lower than usual. Consider reaching out for support.")
        
        return {
            "insights": insights,
            "patterns": patterns,
            "best_day": day_avg.index[0] if not day_avg.empty else None,
            "best_hour": best_hour if 'best_hour' in locals() else None,
            "recent_trend": "improving" if recent_avg > overall_avg else "declining" if recent_avg < overall_avg else "stable"
        }
    
    def analyze_checkin_patterns(self) -> Dict:
        """Analyze daily check-in patterns"""
        if not self.checkin_data:
            return {"insights": [], "recommendations": []}
        
        df = pd.DataFrame(self.checkin_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        insights = []
        recommendations = []
        most_common_sleep = None
        most_common_energy = None
        
        # Analyze sleep patterns
        morning_checkins = df[df['time_period'] == 'morning']
        if not morning_checkins.empty and 'sleep_quality' in morning_checkins.columns:
            sleep_quality = morning_checkins['sleep_quality'].value_counts()
            most_common_sleep = sleep_quality.index[0] if not sleep_quality.empty else None
            
            if most_common_sleep in ['Poor', 'Terrible']:
                recommendations.append("😴 Consider improving your sleep routine for better daily focus")
            elif most_common_sleep in ['Excellent', 'Good']:
                insights.append("😴 Your sleep quality is consistently good - this helps your daily focus!")
        
        # Analyze energy patterns
        if 'energy_level' in df.columns:
            energy_levels = df['energy_level'].value_counts()
            if not energy_levels.empty:
                most_common_energy = energy_levels.index[0]
                if most_common_energy in ['Low', 'Very low']:
                    recommendations.append("🔋 Your energy levels are often low. Consider adjusting your routine or diet.")
                elif most_common_energy in ['High', 'Good']:
                    insights.append("🔋 You maintain good energy levels - great for productivity!")
        
        # Analyze focus patterns
        if 'focus_today' in df.columns:
            focus_entries = df[df['focus_today'].notna() & (df['focus_today'] != '')]
            if not focus_entries.empty:
                insights.append(f"🎯 You've set {len(focus_entries)} focus goals recently")
        
        return {
            "insights": insights,
            "recommendations": recommendations,
            "sleep_quality": most_common_sleep,
            "energy_level": most_common_energy
        }
    
    def generate_daily_recommendation(self) -> str:
        """Generate a personalized daily recommendation"""
        mood_analysis = self.analyze_mood_patterns()
        checkin_analysis = self.analyze_checkin_patterns()
        
        recommendations = []
        
        # Time-based recommendations
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            recommendations.append("🌅 Start your day with a clear focus goal")
        elif 12 <= current_hour < 18:
            recommendations.append("☀️ Take a short break to maintain your energy")
        else:
            recommendations.append("🌆 Reflect on your accomplishments and plan for tomorrow")
        
        # Mood-based recommendations
        if mood_analysis.get('recent_trend') == 'declining':
            recommendations.append("💙 Consider a self-care activity today")
        elif mood_analysis.get('recent_trend') == 'improving':
            recommendations.append("🎉 Build on your positive momentum")
        
        # Energy-based recommendations
        if checkin_analysis.get('energy_level') in ['Low', 'Very low']:
            recommendations.append("🔋 Try a short walk or stretching to boost your energy")
        
        # Goal-focused recommendations
        recommendations.append(f"🎯 Remember your goal: {self.user_goal}")
        
        return " | ".join(recommendations)
    
    def get_weekly_summary(self) -> Dict:
        """Generate a comprehensive weekly summary"""
        mood_analysis = self.analyze_mood_patterns()
        checkin_analysis = self.analyze_checkin_patterns()
        
        # Count recent activities
        recent_moods = len([m for m in self.mood_data 
                          if datetime.fromisoformat(m['timestamp']) > datetime.now() - timedelta(days=7)])
        recent_checkins = len([c for c in self.checkin_data 
                             if datetime.fromisoformat(c['timestamp']) > datetime.now() - timedelta(days=7)])
        
        summary = {
            "mood_entries": recent_moods,
            "checkin_entries": recent_checkins,
            "mood_trend": mood_analysis.get('recent_trend', 'stable'),
            "best_day": mood_analysis.get('best_day'),
            "sleep_quality": checkin_analysis.get('sleep_quality'),
            "energy_level": checkin_analysis.get('energy_level'),
            "insights": mood_analysis.get('insights', []) + checkin_analysis.get('insights', []),
            "recommendations": checkin_analysis.get('recommendations', [])
        }
        
        return summary
    
    def get_personalized_greeting(self) -> str:
        """Generate a personalized greeting based on user data and time"""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            time_greeting = "Good morning"
        elif 12 <= current_hour < 18:
            time_greeting = "Good afternoon"
        else:
            time_greeting = "Good evening"
        
        # Add personal touch based on tone preference
        if self.user_tone == "Gentle & supportive":
            tone_phrase = "I'm here to support you"
        elif self.user_tone == "Direct & motivating":
            tone_phrase = "Let's make today productive"
        else:
            tone_phrase = "Ready to help you focus"
        
        return f"{time_greeting}! {tone_phrase} on your goal: {self.user_goal}"
    
    def get_personalized_joy_suggestions(self) -> List[str]:
        """Get personalized suggestions based on user's joy sources"""
        suggestions = []
        
        for joy_source in self.joy_sources:
            if joy_source == "Friends":
                suggestions.append("👥 Connect with a friend or family member")
            elif joy_source == "Movement":
                suggestions.append("🏃‍♂️ Do some light exercise or stretching")
            elif joy_source == "Creating":
                suggestions.append("🎨 Spend time on a creative project")
            elif joy_source == "Helping others":
                suggestions.append("🤝 Do something kind for someone else")
            elif joy_source == "Nature":
                suggestions.append("🌿 Spend time outdoors or with plants")
            elif joy_source == "Rest":
                suggestions.append("😌 Take a moment to rest and recharge")
            elif joy_source == "Learning":
                suggestions.append("📚 Read or learn something new")
        
        return suggestions
    
    def get_energy_drainer_avoidance_tips(self) -> List[str]:
        """Get tips to avoid or manage energy drainers"""
        tips = []
        
        for drainer in self.energy_drainers:
            if drainer == "Overwhelm":
                tips.append("📝 Break tasks into smaller, manageable steps")
            elif drainer == "Lack of sleep":
                tips.append("😴 Prioritize getting 7-9 hours of sleep")
            elif drainer == "Isolation":
                tips.append("👥 Reach out to someone for connection")
            elif drainer == "Criticism":
                tips.append("💙 Practice self-compassion and positive self-talk")
            elif drainer == "Deadlines":
                tips.append("⏰ Start tasks early to reduce deadline pressure")
        
        return tips
    
    def get_situation_specific_advice(self) -> str:
        """Get advice specific to user's situation"""
        situation_advice = {
            "Freelancer": "💼 As a freelancer, consider setting clear work boundaries and regular breaks",
            "New parent": "👶 Parenting is demanding - remember to take care of yourself too",
            "PhD student": "🎓 Research can be isolating - try to connect with colleagues regularly",
            "Full-time job": "🏢 Balance work demands with personal time and self-care",
            "Unemployed": "💪 Use this time to build skills and maintain a positive routine"
        }
        
        return situation_advice.get(self.situation, "🌟 Focus on what you can control and celebrate small wins")
    
    def get_small_habit_reminder(self) -> str:
        """Get a reminder about the user's small habit goal"""
        if self.small_habit and self.energy in ["Low", "Very low"]:
            return f"🌱 Remember your small habit goal: {self.small_habit}. Even 5 minutes counts!"
        return ""
    
    def generate_smart_task_plan(self, checkin_data: Dict, user_goals: str = None) -> Dict:
        """Generate intelligent task planning based on user's current state and goals"""
        current_hour = datetime.now().hour
        time_period = checkin_data.get('time_period', 'morning')
        
        # Analyze current state
        sleep_quality = checkin_data.get('sleep_quality', 'Good')
        energy_level = checkin_data.get('energy_level', 'Good')
        current_feeling = checkin_data.get('current_feeling', 'Good')
        day_progress = checkin_data.get('day_progress', 'Good')
        
        # Get user's focus goal
        focus_goal = checkin_data.get('focus_today', user_goals or self.user_goal)
        
        # Generate task plan based on time period and state
        if time_period == 'morning':
            return self._generate_morning_task_plan(sleep_quality, energy_level, focus_goal)
        elif time_period == 'afternoon':
            return self._generate_afternoon_task_plan(energy_level, day_progress, focus_goal)
        else:  # evening
            return self._generate_evening_task_plan(current_feeling, focus_goal)
    
    def _generate_morning_task_plan(self, sleep_quality: str, energy_level: str, focus_goal: str) -> Dict:
        """Generate morning task plan based on sleep and energy"""
        tasks = []
        recommendations = []
        
        # Adjust based on sleep quality
        if sleep_quality in ['Poor', 'Terrible']:
            tasks.extend([
                "🌅 Gentle morning routine (10 min)",
                "💧 Hydrate with water",
                "🧘 Light stretching or meditation"
            ])
            recommendations.append("Start with gentle activities to build momentum")
        elif sleep_quality in ['Excellent', 'Good']:
            tasks.extend([
                "🎯 Tackle your most important task first",
                "📝 Review and prioritize today's goals",
                "🏃‍♂️ Consider exercise if energy is high"
            ])
            recommendations.append("Great sleep! You're ready for focused work")
        
        # Adjust based on energy level
        if energy_level in ['Low', 'Very low']:
            tasks.extend([
                "☕ Have a healthy breakfast",
                "🚶‍♂️ Take a short walk outside",
                "📚 Start with lighter, more enjoyable tasks"
            ])
            recommendations.append("Build energy gradually with nourishing activities")
        elif energy_level in ['High', 'Good']:
            tasks.extend([
                "⚡ Use your high energy for complex tasks",
                "🎯 Break down your main goal into 2-3 key actions",
                "⏰ Set specific time blocks for focused work"
            ])
            recommendations.append("Perfect energy for productive deep work")
        
        # Add focus goal breakdown
        if focus_goal:
            tasks.append(f"🎯 Main focus: {focus_goal}")
            tasks.append("📋 Break this into 3 smaller steps")
        
        # Add personalized joy-based activities
        joy_suggestions = self.get_personalized_joy_suggestions()
        if joy_suggestions:
            tasks.append("💫 Energy boost: " + joy_suggestions[0])
        
        # Add small habit reminder if applicable
        habit_reminder = self.get_small_habit_reminder()
        if habit_reminder:
            recommendations.append(habit_reminder)
        
        # Add situation-specific advice
        situation_advice = self.get_situation_specific_advice()
        if situation_advice:
            recommendations.append(situation_advice)
        
        return {
            "tasks": tasks,
            "recommendations": recommendations,
            "estimated_duration": self._estimate_task_duration(energy_level, sleep_quality),
            "priority_order": "energy_based"
        }
    
    def _generate_afternoon_task_plan(self, energy_level: str, day_progress: str, focus_goal: str) -> Dict:
        """Generate afternoon task plan based on energy and progress"""
        tasks = []
        recommendations = []
        
        # Adjust based on day progress
        if day_progress in ['Challenging', 'Difficult']:
            tasks.extend([
                "🔄 Review what's working and what's not",
                "📝 Break down remaining tasks into smaller chunks",
                "☕ Take a proper break to reset"
            ])
            recommendations.append("It's okay to adjust your approach")
        elif day_progress in ['Great', 'Good']:
            tasks.extend([
                "🚀 Build on your momentum",
                "🎯 Focus on your next priority",
                "💡 Consider adding one more meaningful task"
            ])
            recommendations.append("Great progress! Keep the momentum going")
        
        # Adjust based on energy level
        if energy_level in ['Low', 'Very low']:
            tasks.extend([
                "🍎 Have a healthy snack",
                "🚶‍♂️ Take a 10-minute walk",
                "📚 Switch to lighter, administrative tasks"
            ])
            recommendations.append("Focus on energy restoration and lighter tasks")
        elif energy_level in ['High', 'Good']:
            tasks.extend([
                "⚡ Tackle your most challenging remaining task",
                "🎯 Deep work session (45-90 minutes)",
                "📊 Review and adjust your plan for the rest of the day"
            ])
            recommendations.append("Use your energy for focused, important work")
        
        # Add energy drainer avoidance tips
        drainer_tips = self.get_energy_drainer_avoidance_tips()
        if drainer_tips:
            recommendations.append("💡 Avoid energy drainers: " + drainer_tips[0])
        
        # Add joy-based activity for energy boost
        joy_suggestions = self.get_personalized_joy_suggestions()
        if joy_suggestions and energy_level in ['Low', 'Very low']:
            tasks.append("💫 Quick energy boost: " + joy_suggestions[0])
        
        return {
            "tasks": tasks,
            "recommendations": recommendations,
            "estimated_duration": self._estimate_task_duration(energy_level, "Good"),
            "priority_order": "progress_based"
        }
    
    def _generate_evening_task_plan(self, current_feeling: str, focus_goal: str) -> Dict:
        """Generate evening task plan based on current feeling"""
        tasks = []
        recommendations = []
        
        # Adjust based on current feeling
        if current_feeling in ['Tired', 'Stressed']:
            tasks.extend([
                "🧘 Gentle evening routine",
                "📖 Light reading or listening",
                "🛁 Relaxing activity (bath, tea, etc.)"
            ])
            recommendations.append("Focus on rest and recovery")
        elif current_feeling in ['Accomplished', 'Good']:
            tasks.extend([
                "📝 Reflect on today's wins",
                "🎯 Plan tomorrow's priorities",
                "🎉 Celebrate your accomplishments"
            ])
            recommendations.append("Great day! Plan for tomorrow's success")
        
        # Add preparation tasks
        tasks.extend([
            "🌙 Prepare for tomorrow",
            "📋 Review tomorrow's schedule",
            "😴 Wind down routine"
        ])
        
        return {
            "tasks": tasks,
            "recommendations": recommendations,
            "estimated_duration": "1-2 hours",
            "priority_order": "wellness_based"
        }
    
    def _estimate_task_duration(self, energy_level: str, sleep_quality: str) -> str:
        """Estimate task duration based on energy and sleep"""
        if energy_level in ['High', 'Good'] and sleep_quality in ['Excellent', 'Good']:
            return "4-6 hours of focused work"
        elif energy_level in ['Moderate']:
            return "3-4 hours of moderate work"
        else:
            return "2-3 hours of lighter tasks"
    
    # Private helper methods for specific analyses
    
    def _analyze_sleep_patterns(self) -> Dict:
        """Analyze sleep quality patterns"""
        morning_checkins = [c for c in self.checkin_data if c.get('time_period') == 'morning']
        if not morning_checkins:
            return {"average_quality": None, "trend": "stable", "recommendations": []}
        
        sleep_qualities = [c.get('sleep_quality') for c in morning_checkins if c.get('sleep_quality')]
        if not sleep_qualities:
            return {"average_quality": None, "trend": "stable", "recommendations": []}
        
        # Map quality to numeric values
        quality_map = {"Excellent": 5, "Good": 4, "Okay": 3, "Poor": 2, "Terrible": 1}
        numeric_qualities = [quality_map.get(q, 3) for q in sleep_qualities]
        avg_quality = sum(numeric_qualities) / len(numeric_qualities)
        
        recommendations = []
        if avg_quality < 3:
            recommendations.append("Consider establishing a consistent bedtime routine")
            recommendations.append("Try to avoid screens 1 hour before bed")
            recommendations.append("Create a relaxing pre-sleep environment")
        
        return {
            "average_quality": avg_quality,
            "trend": "improving" if avg_quality > 3.5 else "declining" if avg_quality < 2.5 else "stable",
            "recommendations": recommendations
        }
    
    def _analyze_morning_energy_patterns(self) -> Dict:
        """Analyze morning energy patterns"""
        morning_checkins = [c for c in self.checkin_data if c.get('time_period') == 'morning']
        if not morning_checkins:
            return {"average_energy": None, "trend": "stable", "recommendations": []}
        
        energy_levels = [c.get('energy_level') for c in morning_checkins if c.get('energy_level')]
        if not energy_levels:
            return {"average_energy": None, "trend": "stable", "recommendations": []}
        
        # Map energy to numeric values
        energy_map = {"High": 5, "Good": 4, "Moderate": 3, "Low": 2, "Very low": 1}
        numeric_energy = [energy_map.get(e, 3) for e in energy_levels]
        avg_energy = sum(numeric_energy) / len(numeric_energy)
        
        recommendations = []
        if avg_energy < 3:
            recommendations.append("Consider morning exercise or stretching")
            recommendations.append("Try a protein-rich breakfast")
            recommendations.append("Ensure adequate hydration first thing")
        
        return {
            "average_energy": avg_energy,
            "trend": "improving" if avg_energy > 3.5 else "declining" if avg_energy < 2.5 else "stable",
            "recommendations": recommendations
        }
    
    def _generate_focus_suggestions(self, current_checkin: Dict) -> List[str]:
        """Generate focus suggestions based on current check-in"""
        suggestions = []
        energy_level = current_checkin.get('energy_level', 'Moderate')
        
        if energy_level in ['High', 'Good']:
            suggestions.append("Tackle your most challenging task first")
            suggestions.append("Set ambitious but achievable goals")
            suggestions.append("Use your high energy for creative work")
        elif energy_level in ['Low', 'Very low']:
            suggestions.append("Start with simple, routine tasks")
            suggestions.append("Break large tasks into smaller steps")
            suggestions.append("Consider a short walk to boost energy")
        else:
            suggestions.append("Balance challenging and routine tasks")
            suggestions.append("Take regular short breaks")
            suggestions.append("Stay hydrated throughout the day")
        
        return suggestions
    
    def _generate_morning_wellness_tips(self, current_checkin: Dict) -> List[str]:
        """Generate morning wellness tips"""
        tips = [
            "Start with a glass of water",
            "Take 5 minutes for deep breathing",
            "Consider a short morning walk",
            "Eat a nutritious breakfast",
            "Set positive intentions for the day"
        ]
        
        sleep_quality = current_checkin.get('sleep_quality', 'Okay')
        if sleep_quality in ['Poor', 'Terrible']:
            tips.append("Consider a gentle morning routine to ease into the day")
        
        return tips
    
    def _analyze_progress_patterns(self, morning_checkin: Dict, current_checkin: Dict) -> Dict:
        """Analyze progress patterns from morning to afternoon"""
        if not morning_checkin:
            return {"progress_level": "unknown", "insights": [], "adjustments": []}
        
        morning_focus = morning_checkin.get('focus_today', '')
        afternoon_progress = current_checkin.get('day_progress', 'Okay')
        
        insights = []
        adjustments = []
        
        if afternoon_progress in ['Great', 'Good']:
            insights.append("You're making excellent progress on your morning goals")
            adjustments.append("Continue with your current approach")
        elif afternoon_progress in ['Challenging', 'Difficult']:
            insights.append("You're facing some challenges with your morning plan")
            adjustments.append("Consider breaking tasks into smaller steps")
            adjustments.append("Reassess priorities for the remaining day")
        
        return {
            "progress_level": afternoon_progress,
            "insights": insights,
            "adjustments": adjustments
        }
    
    def _analyze_energy_changes(self, morning_checkin: Dict, current_checkin: Dict) -> Dict:
        """Analyze energy changes from morning to afternoon"""
        if not morning_checkin:
            return {"energy_trend": "unknown", "insights": [], "maintenance_tips": []}
        
        morning_energy = morning_checkin.get('energy_level', 'Moderate')
        afternoon_progress = current_checkin.get('day_progress', 'Okay')
        
        insights = []
        maintenance_tips = []
        
        if afternoon_progress in ['Challenging', 'Difficult']:
            maintenance_tips.append("Take a 10-minute break to recharge")
            maintenance_tips.append("Consider a healthy snack")
            maintenance_tips.append("Do some light stretching")
        
        return {
            "energy_trend": "maintaining" if afternoon_progress in ['Great', 'Good'] else "declining",
            "insights": insights,
            "maintenance_tips": maintenance_tips
        }
    
    def _generate_plan_adjustments(self, morning_checkin: Dict, current_checkin: Dict) -> List[str]:
        """Generate plan adjustment suggestions"""
        adjustments = []
        progress = current_checkin.get('day_progress', 'Okay')
        
        if progress in ['Challenging', 'Difficult']:
            adjustments.append("Prioritize the most important tasks")
            adjustments.append("Consider moving non-urgent tasks to tomorrow")
            adjustments.append("Focus on one task at a time")
        else:
            adjustments.append("Build on your momentum")
            adjustments.append("Consider adding one more priority task")
            adjustments.append("Use extra time for planning tomorrow")
        
        return adjustments
    
    def _generate_break_recommendations(self, current_checkin: Dict) -> List[str]:
        """Generate break recommendations"""
        recommendations = []
        take_break = current_checkin.get('take_break', 'Maybe later')
        
        if take_break == "Yes, I need a break":
            recommendations.append("Step away from your workspace for 10 minutes")
            recommendations.append("Do some light stretching or walking")
            recommendations.append("Practice deep breathing exercises")
        elif take_break == "No, I'm in the zone":
            recommendations.append("Enjoy your productive flow state")
            recommendations.append("Remember to take a break when you naturally pause")
        else:
            recommendations.append("Consider a short 5-minute break")
            recommendations.append("Stay hydrated and move around")
        
        return recommendations
    
    def _get_today_journey(self) -> Dict:
        """Get today's complete journey from all check-ins"""
        today = datetime.now().date()
        today_checkins = [
            checkin for checkin in self.checkin_data
            if datetime.fromisoformat(checkin['timestamp']).date() == today
        ]
        
        journey = {
            "morning": None,
            "afternoon": None,
            "evening": None,
            "complete": len(today_checkins) == 3
        }
        
        for checkin in today_checkins:
            journey[checkin['time_period']] = checkin
        
        return journey
    
    def _analyze_daily_patterns(self, today_journey: Dict) -> Dict:
        """Analyze patterns across the day"""
        patterns = {
            "energy_flow": "stable",
            "productivity_curve": "steady",
            "challenges": [],
            "successes": []
        }
        
        morning = today_journey.get('morning')
        afternoon = today_journey.get('afternoon')
        evening = today_journey.get('evening')
        
        if morning and afternoon:
            morning_energy = morning.get('energy_level', 'Moderate')
            afternoon_progress = afternoon.get('day_progress', 'Okay')
            
            if afternoon_progress in ['Great', 'Good'] and morning_energy in ['High', 'Good']:
                patterns["energy_flow"] = "optimal"
                patterns["successes"].append("High morning energy led to productive afternoon")
            elif afternoon_progress in ['Challenging', 'Difficult']:
                patterns["challenges"].append("Afternoon productivity challenges")
        
        return patterns
    
    def _analyze_emotional_patterns(self, current_checkin: Dict) -> Dict:
        """Analyze emotional patterns from evening check-in"""
        current_feeling = current_checkin.get('current_feeling', 'Okay')
        accomplishments = current_checkin.get('accomplishments', '')
        challenges = current_checkin.get('challenges', '')
        
        analysis = {
            "emotional_state": current_feeling,
            "processing_needs": [],
            "coping_strategies": []
        }
        
        if current_feeling in ['Tired', 'Stressed']:
            analysis["processing_needs"].append("Process any difficult emotions from the day")
            analysis["coping_strategies"].append("Practice relaxation techniques")
            analysis["coping_strategies"].append("Consider journaling about challenges")
        elif current_feeling == 'Accomplished':
            analysis["processing_needs"].append("Celebrate your achievements")
            analysis["coping_strategies"].append("Reflect on what made today successful")
        
        return analysis
    
    def _generate_tomorrow_preparation(self, today_journey: Dict, current_checkin: Dict) -> List[str]:
        """Generate tomorrow preparation suggestions"""
        preparation = []
        current_feeling = current_checkin.get('current_feeling', 'Okay')
        
        if current_feeling in ['Tired', 'Stressed']:
            preparation.append("Plan a lighter day tomorrow")
            preparation.append("Prioritize rest and recovery")
        else:
            preparation.append("Build on today's momentum")
            preparation.append("Set clear priorities for tomorrow")
        
        preparation.append("Review and adjust your routine if needed")
        preparation.append("Prepare your workspace for tomorrow")
        
        return preparation
    
    def _generate_sleep_preparation(self, current_checkin: Dict) -> List[str]:
        """Generate sleep preparation suggestions"""
        sleep_tips = [
            "Create a relaxing evening routine",
            "Avoid screens 1 hour before bed",
            "Practice gentle stretching or meditation",
            "Ensure your sleep environment is comfortable"
        ]
        
        current_feeling = current_checkin.get('current_feeling', 'Okay')
        if current_feeling in ['Tired', 'Stressed']:
            sleep_tips.append("Consider a warm bath or shower")
            sleep_tips.append("Practice deep breathing exercises")
        
        return sleep_tips
    
    def _analyze_goal_progress(self, today_journey: Dict) -> Dict:
        """Analyze progress toward user's main goal"""
        progress_indicators = []
        challenges = []
        
        for period, checkin in today_journey.items():
            if checkin and period != 'complete':
                if checkin.get('focus_today'):
                    progress_indicators.append(f"Set focus goals in {period}")
                if checkin.get('accomplishments'):
                    progress_indicators.append(f"Made progress in {period}")
                if checkin.get('day_progress') in ['Challenging', 'Difficult']:
                    challenges.append(f"Faced challenges in {period}")
        
        return {
            "progress_indicators": progress_indicators,
            "challenges": challenges,
            "overall_progress": "good" if len(progress_indicators) > len(challenges) else "needs_improvement"
        }
    
    def _analyze_daily_wellness(self, today_journey: Dict) -> Dict:
        """Analyze overall daily wellness"""
        wellness_indicators = []
        stress_points = []
        
        for period, checkin in today_journey.items():
            if checkin and period != 'complete':
                if checkin.get('sleep_quality') in ['Excellent', 'Good']:
                    wellness_indicators.append("Good sleep quality")
                if checkin.get('energy_level') in ['High', 'Good']:
                    wellness_indicators.append("Maintained good energy")
                if checkin.get('current_feeling') in ['Accomplished', 'Good']:
                    wellness_indicators.append("Positive emotional state")
                
                if checkin.get('current_feeling') in ['Tired', 'Stressed']:
                    stress_points.append(f"Stress in {period}")
        
        return {
            "wellness_indicators": wellness_indicators,
            "stress_points": stress_points,
            "overall_wellness": "good" if len(wellness_indicators) > len(stress_points) else "needs_attention"
        }
    
    def _generate_growth_insights(self, today_journey: Dict) -> List[str]:
        """Generate personal growth insights"""
        insights = []
        
        for period, checkin in today_journey.items():
            if checkin and period != 'complete':
                if checkin.get('accomplishments'):
                    insights.append(f"Successfully accomplished tasks in {period}")
                if checkin.get('challenges'):
                    insights.append(f"Faced and worked through challenges in {period}")
                if checkin.get('focus_today'):
                    insights.append(f"Demonstrated goal-setting in {period}")
        
        if not insights:
            insights.append("Every day provides opportunities for growth and learning")
        
        return insights
