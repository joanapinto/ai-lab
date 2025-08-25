"""
Fallback System for Focus Companion
Provides intelligent responses when AI features are not available
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

class FallbackAssistant:
    """Fallback assistant that provides intelligent responses without AI"""
    
    def __init__(self, user_profile: Dict, mood_data: List[Dict], checkin_data: List[Dict]):
        self.user_profile = user_profile
        self.mood_data = mood_data
        self.checkin_data = checkin_data
        self.user_goal = user_profile.get('goal', 'Improve focus and productivity')
        self.user_tone = user_profile.get('tone', 'Gentle & supportive')
    
    def get_daily_encouragement(self) -> str:
        """Get a daily encouragement message"""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            messages = [
                f"🌅 Good morning! Ready to tackle your goal: {self.user_goal}",
                f"🌅 Rise and shine! Today is a new opportunity to work on: {self.user_goal}",
                f"🌅 Morning! Let's start the day focused on: {self.user_goal}"
            ]
        elif 12 <= current_hour < 18:
            messages = [
                f"☀️ Good afternoon! How's your progress on: {self.user_goal}",
                f"☀️ Afternoon check-in! Still working toward: {self.user_goal}",
                f"☀️ Midday reminder: You're making progress on: {self.user_goal}"
            ]
        else:
            messages = [
                f"🌆 Good evening! Reflect on your work toward: {self.user_goal}",
                f"🌆 Evening! How did you do today with: {self.user_goal}",
                f"🌆 Night check-in! Remember your focus on: {self.user_goal}"
            ]
        
        return random.choice(messages)
    
    def get_mood_insight(self) -> str:
        """Get a basic mood insight based on recent data"""
        if not self.mood_data:
            return "💡 Start tracking your mood to discover patterns and insights!"
        
        recent_moods = [m for m in self.mood_data 
                       if datetime.fromisoformat(m['timestamp']) > datetime.now() - timedelta(days=7)]
        
        if not recent_moods:
            return "💡 Log your mood regularly to see how it affects your focus and productivity!"
        
        # Calculate average mood intensity
        avg_intensity = sum(m['intensity'] for m in recent_moods) / len(recent_moods)
        
        if avg_intensity >= 7:
            return "🎉 Your mood has been positive recently! This is great for maintaining focus and productivity."
        elif avg_intensity >= 5:
            return "😊 Your mood has been stable. Consider what activities boost your energy and mood."
        else:
            return "💙 Your mood has been lower than usual. Remember to be kind to yourself and reach out for support if needed."
    
    def get_productivity_tip(self) -> str:
        """Get a random productivity tip"""
        tips = [
            "💡 Try the Pomodoro Technique: 25 minutes of focused work, then a 5-minute break",
            "💡 Eliminate distractions by putting your phone in another room",
            "💡 Start with your most important task when your energy is highest",
            "💡 Take regular breaks to maintain focus and prevent burnout",
            "💡 Create a dedicated workspace to signal your brain it's time to focus",
            "💡 Use time-blocking to schedule specific tasks for specific times",
            "💡 Practice the 2-minute rule: if it takes less than 2 minutes, do it now",
            "💡 Batch similar tasks together to reduce context switching",
            "💡 Set clear, specific goals for each work session",
            "💡 Review and plan your day the night before"
        ]
        
        return random.choice(tips)
    
    def get_wellness_reminder(self) -> str:
        """Get a wellness reminder"""
        reminders = [
            "💧 Remember to stay hydrated throughout the day",
            "🌱 Take a moment to stretch and move your body",
            "😌 Practice deep breathing when you feel overwhelmed",
            "☀️ Get some natural light and fresh air",
            "🍎 Fuel your body with nutritious food",
            "😴 Prioritize good sleep for better focus tomorrow",
            "🎵 Listen to music that helps you focus",
            "🧘 Try a quick meditation or mindfulness exercise",
            "👥 Connect with someone who supports your goals",
            "🎯 Celebrate small wins and progress"
        ]
        
        return random.choice(reminders)
    
    def get_goal_reminder(self) -> str:
        """Get a personalized goal reminder"""
        goal_reminders = [
            f"🎯 Remember your goal: {self.user_goal}",
            f"🎯 Every small step brings you closer to: {self.user_goal}",
            f"🎯 Stay focused on what matters: {self.user_goal}",
            f"🎯 Your progress toward {self.user_goal} is worth celebrating",
            f"🎯 Keep moving forward with: {self.user_goal}"
        ]
        
        return random.choice(goal_reminders)
    
    def get_weekly_motivation(self) -> str:
        """Get weekly motivation message"""
        motivations = [
            "🚀 New week, new opportunities to make progress!",
            "🌟 You've got this! Every day is a chance to improve",
            "💪 Consistency beats perfection - keep showing up",
            "🎯 Small actions compound into big results",
            "🌈 Progress, not perfection, is the goal",
            "🔥 Your future self will thank you for today's efforts",
            "⭐ You're building habits that will serve you well",
            "🎊 Celebrate your commitment to growth and improvement"
        ]
        
        return random.choice(motivations)
    
    def get_personalized_greeting(self) -> str:
        """Get a personalized greeting based on user preferences"""
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
    
    def get_activity_suggestion(self) -> str:
        """Get a suggestion for a focus or wellness activity"""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            activities = [
                "🌅 Start with a 5-minute meditation",
                "📝 Write down your top 3 priorities for today",
                "🏃 Take a short walk to boost your energy",
                "📚 Read something inspiring for 10 minutes",
                "🎯 Set a specific, achievable goal for this morning"
            ]
        elif 12 <= current_hour < 18:
            activities = [
                "☀️ Take a 10-minute break to recharge",
                "🚶 Go for a short walk outside",
                "💧 Drink a glass of water and stretch",
                "🎵 Listen to focus music for 15 minutes",
                "🧘 Do a quick breathing exercise"
            ]
        else:
            activities = [
                "🌆 Reflect on today's accomplishments",
                "📖 Read something relaxing before bed",
                "🛁 Take time to unwind and decompress",
                "📝 Plan tomorrow's priorities",
                "😴 Prepare for a good night's sleep"
            ]
        
        return random.choice(activities)
    
    def get_encouragement_for_situation(self, situation: str) -> str:
        """Get encouragement specific to user's situation"""
        situation_encouragement = {
            "New parent": [
                "👶 Being a new parent is challenging - you're doing great!",
                "💕 Your little one is lucky to have such a dedicated parent",
                "🌟 Parenthood and personal growth can happen together"
            ],
            "PhD student": [
                "🎓 Your research and dedication will pay off",
                "📚 Every study session brings you closer to your degree",
                "🔬 You're contributing valuable knowledge to your field"
            ],
            "Freelancer": [
                "💼 Your independence and flexibility are strengths",
                "🚀 Every project builds your portfolio and skills",
                "⭐ You're building your own success story"
            ],
            "Full-time job": [
                "💼 Your commitment to growth in your career is admirable",
                "🏢 Balancing work and personal development takes skill",
                "📈 You're investing in your future success"
            ],
            "Unemployed": [
                "💪 This is a temporary phase - you're building your next chapter",
                "🎯 Use this time to develop skills and clarity",
                "🌟 Your resilience during this time will serve you well"
            ]
        }
        
        if situation in situation_encouragement:
            return random.choice(situation_encouragement[situation])
        else:
            return "🌟 You're on a journey of growth and improvement - that's worth celebrating!"
