"""
Prompt Templates for Focus Companion AI Assistant
Provides structured prompts for generating personalized insights and recommendations
"""

from typing import Dict, List

class PromptTemplates:
    """Collection of prompt templates for different AI interactions"""
    
    @staticmethod
    def mood_analysis_prompt(mood_data: List[Dict], user_goal: str) -> str:
        """Generate prompt for mood pattern analysis"""
        return f"""
        Analyze the following mood data for a user focused on: {user_goal}
        
        Mood Entries: {mood_data}
        
        Please provide:
        1. Key patterns in mood over time
        2. Correlation between mood and productivity
        3. Specific recommendations for improving mood and focus
        4. Encouraging insights based on positive trends
        
        Focus on actionable, supportive advice that aligns with their goal.
        """
    
    @staticmethod
    def daily_recommendation_prompt(user_profile: Dict, recent_data: Dict) -> str:
        """Generate prompt for daily recommendations"""
        return f"""
        User Profile: {user_profile}
        Recent Activity: {recent_data}
        
        Generate a personalized daily recommendation that:
        1. Acknowledges their current situation and energy level
        2. Provides specific, actionable advice
        3. Maintains their preferred tone: {user_profile.get('tone', 'Gentle & supportive')}
        4. Supports their goal: {user_profile.get('goal', 'Improve focus')}
        5. Is encouraging and motivating
        
        Keep it concise and practical.
        """
    
    @staticmethod
    def weekly_reflection_prompt(weekly_data: Dict, user_goal: str) -> str:
        """Generate prompt for weekly reflection insights"""
        return f"""
        Weekly Summary: {weekly_data}
        User Goal: {user_goal}
        
        Provide a thoughtful weekly reflection that:
        1. Celebrates achievements and progress
        2. Identifies patterns and insights
        3. Offers constructive feedback
        4. Suggests improvements for next week
        5. Maintains an encouraging, growth-oriented tone
        
        Focus on both emotional wellness and goal progress.
        """
    
    @staticmethod
    def focus_optimization_prompt(checkin_data: List[Dict], mood_data: List[Dict]) -> str:
        """Generate prompt for focus optimization advice"""
        return f"""
        Check-in Data: {checkin_data}
        Mood Data: {mood_data}
        
        Analyze patterns to provide focus optimization advice:
        1. Identify optimal times for deep work
        2. Suggest energy management strategies
        3. Recommend break patterns
        4. Address common focus blockers
        5. Provide environment optimization tips
        
        Base recommendations on actual user patterns and preferences.
        """
    
    @staticmethod
    def sleep_optimization_prompt(sleep_data: List[Dict], energy_data: List[Dict]) -> str:
        """Generate prompt for sleep and energy optimization"""
        return f"""
        Sleep Quality Data: {sleep_data}
        Energy Level Data: {energy_data}
        
        Provide sleep and energy optimization advice:
        1. Identify sleep quality patterns
        2. Suggest sleep routine improvements
        3. Recommend energy-boosting activities
        4. Address sleep-energy correlations
        5. Provide practical lifestyle adjustments
        
        Focus on evidence-based, practical recommendations.
        """
    
    @staticmethod
    def goal_progress_prompt(user_goal: str, progress_data: Dict) -> str:
        """Generate prompt for goal progress analysis"""
        return f"""
        User Goal: {user_goal}
        Progress Data: {progress_data}
        
        Analyze progress toward the user's goal:
        1. Assess current progress level
        2. Identify successful strategies
        3. Suggest adjustments or improvements
        4. Provide motivation and encouragement
        5. Recommend next steps
        
        Be specific and actionable while maintaining encouragement.
        """
    
    @staticmethod
    def stress_management_prompt(mood_data: List[Dict], checkin_data: List[Dict]) -> str:
        """Generate prompt for stress management advice"""
        return f"""
        Mood Data: {mood_data}
        Check-in Data: {checkin_data}
        
        Provide stress management advice based on patterns:
        1. Identify stress triggers and patterns
        2. Suggest coping strategies
        3. Recommend preventive measures
        4. Provide relaxation techniques
        5. Suggest lifestyle adjustments
        
        Focus on practical, accessible stress management techniques.
        """
    
    @staticmethod
    def productivity_insights_prompt(all_data: Dict) -> str:
        """Generate prompt for productivity insights"""
        return f"""
        Complete User Data: {all_data}
        
        Provide comprehensive productivity insights:
        1. Identify peak productivity times
        2. Suggest workflow optimizations
        3. Recommend focus techniques
        4. Address productivity blockers
        5. Suggest habit improvements
        
        Base insights on actual user patterns and preferences.
        """

class ResponseFormats:
    """Standard response formats for consistent AI outputs"""
    
    @staticmethod
    def daily_recommendation_format() -> str:
        return """
        Format your response as:
        
        🌟 **Today's Focus**: [Main recommendation]
        
        💡 **Quick Tips**:
        - [Tip 1]
        - [Tip 2]
        - [Tip 3]
        
        🎯 **Remember**: [Goal reminder]
        """
    
    @staticmethod
    def weekly_summary_format() -> str:
        return """
        Format your response as:
        
        📊 **This Week's Progress**:
        [Summary of achievements and patterns]
        
        🎉 **Celebrations**:
        [Positive highlights]
        
        🔍 **Insights**:
        [Key learnings and patterns]
        
        🚀 **Next Week's Focus**:
        [Specific recommendations]
        """
    
    @staticmethod
    def mood_insight_format() -> str:
        return """
        Format your response as:
        
        📈 **Mood Patterns**:
        [Key patterns identified]
        
        💭 **Insights**:
        [What these patterns mean]
        
        🛠️ **Recommendations**:
        [Actionable advice]
        
        🌟 **Positive Notes**:
        [Encouraging observations]
        """
