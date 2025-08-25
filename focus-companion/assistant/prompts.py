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
    
    @staticmethod
    def morning_checkin_prompt(user_profile: Dict, previous_data: Dict, current_checkin: Dict) -> str:
        """Generate prompt for morning check-in analysis and recommendations"""
        return f"""
        User Profile: {user_profile}
        Previous Evening Check-in: {previous_data}
        Current Morning Check-in: {current_checkin}
        
        Provide morning-focused insights and recommendations:
        
        1. **Sleep Analysis**: 
           - Assess sleep quality impact on daily energy
           - Suggest sleep routine improvements if needed
           - Connect sleep patterns to productivity
        
        2. **Energy Assessment**:
           - Analyze current energy level for the day ahead
           - Suggest energy-boosting activities if low
           - Recommend optimal timing for important tasks
        
        3. **Focus Planning**:
           - Help refine the day's focus goals
           - Suggest task prioritization based on energy
           - Recommend morning routine adjustments
        
        4. **Motivation & Mindset**:
           - Provide encouraging morning motivation
           - Address any concerns from previous day
           - Set positive tone for the day ahead
        
        5. **Wellness Tips**:
           - Suggest morning wellness practices
           - Recommend hydration and nutrition
           - Suggest movement or exercise ideas
        
        Tone: {user_profile.get('tone', 'Gentle & supportive')}
        Goal: {user_profile.get('goal', 'Improve focus and productivity')}
        
        Keep recommendations practical and actionable for the morning hours.
        """
    
    @staticmethod
    def afternoon_checkin_prompt(user_profile: Dict, morning_data: Dict, current_checkin: Dict) -> str:
        """Generate prompt for afternoon check-in analysis and recommendations"""
        return f"""
        User Profile: {user_profile}
        Morning Check-in: {morning_data}
        Current Afternoon Check-in: {current_checkin}
        
        Provide afternoon-focused insights and recommendations:
        
        1. **Progress Assessment**:
           - Evaluate progress against morning goals
           - Identify what's working well
           - Highlight areas needing adjustment
        
        2. **Energy Management**:
           - Analyze energy changes since morning
           - Suggest energy maintenance strategies
           - Recommend optimal afternoon activities
        
        3. **Plan Adjustment**:
           - Help refine remaining day's plan
           - Suggest task reprioritization if needed
           - Recommend realistic afternoon goals
        
        4. **Break & Recovery**:
           - Assess break needs and timing
           - Suggest effective break activities
           - Recommend stress management techniques
        
        5. **Focus Optimization**:
           - Identify focus challenges and solutions
           - Suggest environment adjustments
           - Recommend focus techniques for afternoon
        
        6. **Motivation Boost**:
           - Provide mid-day encouragement
           - Celebrate progress made so far
           - Maintain momentum for rest of day
        
        Tone: {user_profile.get('tone', 'Gentle & supportive')}
        Goal: {user_profile.get('goal', 'Improve focus and productivity')}
        
        Focus on maintaining momentum and optimizing the remaining day.
        """
    
    @staticmethod
    def evening_checkin_prompt(user_profile: Dict, daily_journey: Dict, current_checkin: Dict) -> str:
        """Generate prompt for evening check-in analysis and recommendations"""
        return f"""
        User Profile: {user_profile}
        Daily Journey (Morning + Afternoon): {daily_journey}
        Current Evening Check-in: {current_checkin}
        
        Provide evening-focused insights and recommendations:
        
        1. **Day Reflection**:
           - Celebrate accomplishments and progress
           - Acknowledge challenges and learning
           - Provide perspective on the day's journey
        
        2. **Emotional Processing**:
           - Help process any difficult emotions
           - Validate feelings and experiences
           - Suggest healthy coping strategies
        
        3. **Wellness Assessment**:
           - Evaluate overall daily wellness
           - Suggest evening relaxation techniques
           - Recommend stress relief activities
        
        4. **Tomorrow Preparation**:
           - Help plan for tomorrow based on today's learnings
           - Suggest adjustments to routine or approach
           - Set positive intentions for next day
        
        5. **Sleep Preparation**:
           - Suggest evening routine improvements
           - Recommend sleep hygiene practices
           - Help wind down from the day
        
        6. **Growth & Learning**:
           - Identify key learnings from the day
           - Suggest areas for personal growth
           - Encourage self-compassion and kindness
        
        Tone: {user_profile.get('tone', 'Gentle & supportive')}
        Goal: {user_profile.get('goal', 'Improve focus and productivity')}
        
        Focus on reflection, processing, and preparation for rest and tomorrow.
        """
    
    @staticmethod
    def daily_summary_prompt(user_profile: Dict, complete_daily_data: Dict) -> str:
        """Generate prompt for complete daily summary and insights"""
        return f"""
        User Profile: {user_profile}
        Complete Daily Data (Morning + Afternoon + Evening): {complete_daily_data}
        
        Provide a comprehensive daily summary and insights:
        
        1. **Daily Overview**:
           - Summarize the complete day's journey
           - Highlight key moments and transitions
           - Identify overall daily theme or pattern
        
        2. **Goal Progress**:
           - Assess progress toward user's main goal
           - Identify successful strategies used
           - Suggest improvements for future days
        
        3. **Pattern Recognition**:
           - Identify recurring patterns or themes
           - Connect morning energy to afternoon productivity
           - Analyze evening reflection patterns
        
        4. **Wellness Assessment**:
           - Evaluate overall daily wellness
           - Identify stress points and coping strategies
           - Suggest wellness improvements
        
        5. **Tomorrow's Preparation**:
           - Suggest specific improvements for tomorrow
           - Recommend routine adjustments
           - Set positive intentions and goals
        
        6. **Growth Insights**:
           - Identify personal growth opportunities
           - Suggest habit improvements
           - Encourage continued progress
        
        Tone: {user_profile.get('tone', 'Gentle & supportive')}
        Goal: {user_profile.get('goal', 'Improve focus and productivity')}
        
        Provide a balanced, encouraging summary that celebrates progress while suggesting improvements.
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
    
    @staticmethod
    def morning_checkin_format() -> str:
        return """
        Format your response as:
        
        🌅 **Morning Energy Assessment**:
        [Analysis of sleep and energy]
        
        🎯 **Focus Planning**:
        [Specific focus recommendations]
        
        💪 **Motivation & Mindset**:
        [Encouraging morning message]
        
        🌟 **Wellness Tips**:
        [Morning wellness suggestions]
        
        📋 **Today's Action Plan**:
        [3 specific actionable steps]
        """
    
    @staticmethod
    def afternoon_checkin_format() -> str:
        return """
        Format your response as:
        
        📊 **Progress Assessment**:
        [Evaluation of morning progress]
        
        🔋 **Energy Management**:
        [Energy optimization suggestions]
        
        🔄 **Plan Adjustments**:
        [Specific plan refinements]
        
        ☕ **Break & Recovery**:
        [Break and stress management tips]
        
        🚀 **Afternoon Focus**:
        [3 specific afternoon priorities]
        """
    
    @staticmethod
    def evening_checkin_format() -> str:
        return """
        Format your response as:
        
        🌆 **Day Reflection**:
        [Celebration of accomplishments]
        
        💭 **Emotional Processing**:
        [Support for feelings and challenges]
        
        🌙 **Evening Wellness**:
        [Relaxation and preparation tips]
        
        🌟 **Tomorrow's Preparation**:
        [Specific improvements for tomorrow]
        
        📝 **Key Learnings**:
        [3 important insights from today]
        """
    
    @staticmethod
    def daily_summary_format() -> str:
        return """
        Format your response as:
        
        📅 **Daily Overview**:
        [Complete day summary]
        
        🎯 **Goal Progress**:
        [Progress toward main goal]
        
        🔍 **Pattern Recognition**:
        [Key patterns and insights]
        
        💚 **Wellness Assessment**:
        [Overall wellness evaluation]
        
        🚀 **Tomorrow's Focus**:
        [3 specific improvements]
        
        🌟 **Growth Celebration**:
        [Personal growth highlights]
        """
