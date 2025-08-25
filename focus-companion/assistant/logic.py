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
        self.user_tone = user_profile.get('tone', 'Gentle & supportive')
    
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
        
        # Analyze sleep patterns
        morning_checkins = df[df['time_period'] == 'morning']
        if not morning_checkins.empty:
            sleep_quality = morning_checkins['sleep_quality'].value_counts()
            most_common_sleep = sleep_quality.index[0] if not sleep_quality.empty else None
            
            if most_common_sleep in ['Poor', 'Terrible']:
                recommendations.append("😴 Consider improving your sleep routine for better daily focus")
            elif most_common_sleep in ['Excellent', 'Good']:
                insights.append("😴 Your sleep quality is consistently good - this helps your daily focus!")
        
        # Analyze energy patterns
        energy_levels = df['energy_level'].value_counts()
        if not energy_levels.empty:
            most_common_energy = energy_levels.index[0]
            if most_common_energy in ['Low', 'Very low']:
                recommendations.append("🔋 Your energy levels are often low. Consider adjusting your routine or diet.")
            elif most_common_energy in ['High', 'Good']:
                insights.append("🔋 You maintain good energy levels - great for productivity!")
        
        # Analyze focus patterns
        focus_entries = df[df['focus_today'].notna() & (df['focus_today'] != '')]
        if not focus_entries.empty:
            insights.append(f"🎯 You've set {len(focus_entries)} focus goals recently")
        
        return {
            "insights": insights,
            "recommendations": recommendations,
            "sleep_quality": most_common_sleep if 'most_common_sleep' in locals() else None,
            "energy_level": most_common_energy if 'most_common_energy' in locals() else None
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
