import streamlit as st

st.set_page_config(page_title="Help & Tips", page_icon="❓")

def main():
    st.title("❓ Help & Tips")
    st.markdown("Everything you need to know about using Weekly Coach GPT")
    
    # Add a back button
    if st.button("← Back to Dashboard"):
        st.switch_page("main.py")
    
    # Quick navigation
    st.markdown("### 📋 Quick Navigation")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎯 Setup"):
            st.switch_page("pages/1_Setup.py")
    with col2:
        if st.button("📋 Weekly Plan"):
            st.switch_page("pages/2_Weekly_Plan.py")
    with col3:
        if st.button("🌤️ Daily Check-in"):
            st.switch_page("pages/3_Daily_Checkin.py")
    with col4:
        if st.button("📊 Progress"):
            st.switch_page("pages/5_Progress.py")
    
    st.markdown("---")
    
    # Getting Started
    st.markdown("### 🚀 Getting Started")
    
    with st.expander("How do I get started?"):
        st.markdown("""
        1. **Complete Setup** - Go to Setup and tell us about your goals and preferences
        2. **Create Your First Plan** - Generate a personalized weekly plan
        3. **Start Daily Check-ins** - Track your progress each day
        4. **Weekly Reflections** - Review your week and learn from it
        """)
    
    with st.expander("What information do I need to provide?"):
        st.markdown("""
        **Essential:**
        - Your main long-term goal
        - Your motivation for achieving it
        
        **Optional but helpful:**
        - Deadline (if any)
        - Coaching style preference
        - Focus areas
        - Working hours
        - Notification frequency
        """)
    
    # Features Guide
    st.markdown("### 🎯 Features Guide")
    
    with st.expander("Weekly Planning"):
        st.markdown("""
        **What it does:**
        - Creates personalized weekly plans based on your goal
        - Breaks down tasks by day
        - Considers your mood, availability, and focus areas
        
        **Tips:**
        - Be specific about your mood and availability
        - Mention any particular focus for the week
        - Plans can be adjusted as needed
        """)
    
    with st.expander("Daily Check-ins"):
        st.markdown("""
        **What it does:**
        - Tracks your daily progress
        - Provides personalized motivation and guidance
        - Updates your completion status
        
        **Tips:**
        - Check in regularly for best results
        - Be honest about your progress
        - Even quick check-ins are valuable
        """)
    
    with st.expander("Progress Tracking"):
        st.markdown("""
        **What it tracks:**
        - Total check-ins and weeks
        - Completion rates
        - Streak days
        - Achievements and insights
        
        **How to view:**
        - Progress dashboard shows key metrics
        - Achievement badges unlock as you progress
        - Insights are generated from your patterns
        """)
    
    with st.expander("Weekly Reflections"):
        st.markdown("""
        **What it does:**
        - Helps you review your week
        - Generates insights from your patterns
        - Suggests improvements for next week
        
        **Tips:**
        - Reflect honestly on your achievements
        - Note what worked and what didn't
        - Use insights to improve future plans
        """)
    
    # Troubleshooting
    st.markdown("### 🔧 Troubleshooting")
    
    with st.expander("Common Issues"):
        st.markdown("""
        **"No weekly plan found"**
        - Create your first weekly plan in the Weekly Plan section
        
        **"Please complete setup first"**
        - Go to Setup and provide your goal and preferences
        
        **Error generating plan/check-in**
        - Check your internet connection
        - Try again in a few minutes
        - Contact support if the issue persists
        """)
    
    with st.expander("How to reset my data"):
        st.markdown("""
        **To start over completely:**
        1. Go to Setup page
        2. Click "Reset and start over"
        3. This will delete all your data and start fresh
        
        **Note:** This action cannot be undone!
        """)
    
    # Best Practices
    st.markdown("### 💡 Best Practices")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎯 Goal Setting**")
        st.markdown("- Be specific and measurable")
        st.markdown("- Break large goals into smaller ones")
        st.markdown("- Set realistic deadlines")
        
        st.markdown("**📝 Planning**")
        st.markdown("- Consider your actual available time")
        st.markdown("- Account for meetings and breaks")
        st.markdown("- Be flexible with your plans")
    
    with col2:
        st.markdown("**🌤️ Daily Habits**")
        st.markdown("- Check in at the same time each day")
        st.markdown("- Be honest about your progress")
        st.markdown("- Celebrate small wins")
        
        st.markdown("**📊 Progress**")
        st.markdown("- Focus on progress, not perfection")
        st.markdown("- Learn from setbacks")
        st.markdown("- Adjust strategies as needed")
    
    # Sample Demos
    st.markdown("---")
    st.markdown("### 🎯 Sample Demos")
    st.markdown("See examples of how the app works before you start. These demos show you exactly what to expect from each feature.")
    
    with st.expander("📋 Sample Weekly Plan", expanded=False):
        st.markdown("### 🎯 Example Goal")
        st.markdown("*Build 3 AI tools by December*")
        
        st.markdown("### 📋 Sample Weekly Plan")
        st.markdown("""
        # Weekly Plan for Building AI Tools
        
        ## 🎯 Main Objective
        Make significant progress on AI tool development with focused daily tasks.
        
        ## 📅 Daily Breakdown
        
        **Monday:** Research and plan the first AI tool
        - Spend 2 hours researching existing solutions
        - Define the core features and requirements
        - Create a basic project structure
        
        **Tuesday:** Start coding the first tool
        - Set up the development environment
        - Implement the basic framework
        - Create the main functionality
        
        **Wednesday:** Continue development and testing
        - Add error handling and validation
        - Write unit tests for core functions
        - Test with sample data
        
        **Thursday:** Polish and document
        - Improve user interface
        - Write documentation
        - Create a demo version
        
        **Friday:** Review and plan next tool
        - Test the complete tool
        - Gather feedback
        - Plan the second AI tool
        
        **Saturday:** Learning and research
        - Study new AI techniques
        - Research tools 2 and 3
        - Update skills as needed
        
        **Sunday:** Rest and reflection
        - Review the week's progress
        - Plan improvements
        - Prepare for next week
        
        ## 💡 Tips for Success
        - Focus on one tool at a time
        - Test frequently as you build
        - Document your progress
        - Stay consistent with daily work
        """)
    
    with st.expander("🌤️ Sample Daily Check-in", expanded=False):
        st.markdown("### 🎯 Example Goal")
        st.markdown("*Build 3 AI tools by December*")
        
        st.markdown("### 📋 Today's Task")
        st.markdown("*Research and plan the first AI tool*")
        
        st.markdown("### 🌤️ Sample Check-in")
        st.markdown("""
        ## 🤖 Your AI Coach Says:
        
        **Great to see you checking in today!** 🌟
        
        I can see you're feeling **motivated** and ready to tackle today's task of researching and planning your first AI tool. That's excellent energy to start the week with!
        
        **For today's focus on "finishing the research phase":**
        
        🎯 **Your Action Plan:**
        - Spend 1-2 hours researching existing AI tools in your target area
        - Take notes on what features work well and what could be improved
        - Define 3-5 core features for your tool
        - Create a simple project outline
        
        💡 **Pro Tips:**
        - Start with a broad search, then narrow down to specific use cases
        - Look at both successful and failed projects to learn from both
        - Don't get overwhelmed by trying to include every feature - focus on the core value
        
        🔥 **Motivation Boost:**
        Remember why you're building these AI tools - you're not just coding, you're creating solutions that could help people! Every great tool started with research and planning, just like you're doing today.
        
        **You've got this!** Take it step by step, and don't hesitate to check in again if you need any guidance. Your consistency is building momentum toward your goal! 🚀
        """)
    
    with st.expander("📝 Sample Weekly Reflection", expanded=False):
        st.markdown("### 🎯 Example Goal")
        st.markdown("*Build 3 AI tools by December*")
        
        st.markdown("### 📝 Sample Weekly Reflection")
        st.markdown("""
        ## 🤖 Your AI Coach's Analysis:
        
        **Excellent work this week!** 🎉
        
        ### 📊 Week Summary
        You've made **significant progress** toward your goal of building 3 AI tools by December. This week you completed the research phase and started the development of your first tool, which is exactly what you planned to achieve.
        
        ### 🎯 Key Achievements
        - ✅ **Completed comprehensive research** on existing AI tools
        - ✅ **Defined clear requirements** for your first tool
        - ✅ **Started coding** and made good progress on the framework
        - ✅ **Maintained consistent daily work** habits
        - ✅ **Stayed focused** despite some technical challenges
        
        ### 💡 Success Patterns Identified
        1. **Morning productivity** - You're most effective when you start early
        2. **Breaking tasks into smaller chunks** - This helps you maintain momentum
        3. **Regular check-ins** - Daily accountability keeps you on track
        4. **Research before coding** - This approach saves time and improves quality
        
        ### ⚠️ Challenges & Solutions
        - **Technical complexity** - You faced some challenging coding problems
        - **Time management** - Some tasks took longer than expected
        - **Solution:** Consider setting aside dedicated time for problem-solving and building in buffer time for unexpected challenges
        
        ### 🚀 Recommendations for Next Week
        1. **Continue with the current momentum** - You're on the right track
        2. **Allocate more time for testing** - This will save time later
        3. **Document as you go** - This will help with future tools
        4. **Celebrate small wins** - You're making real progress!
        
        ### 📈 Progress Toward Goal
        You're approximately **25%** toward your goal of building 3 AI tools. At this pace, you're well-positioned to meet your December deadline. Keep up the excellent work!
        
        **Remember:** Every great developer started exactly where you are. Your consistency and dedication are building the foundation for success! 🌟
        """)
    
    # Contact & Support
    st.markdown("---")
    st.markdown("### 📞 Need More Help?")
    
    st.markdown("""
    **Still have questions?**
    - Check the troubleshooting section above
    - Try resetting and starting over
    - The app is designed to be self-explanatory
    
    **Feature Requests:**
    - This is a personal project
    - Feel free to suggest improvements
    """)
    
    st.markdown("---")
    st.markdown("*Weekly Coach GPT - Your AI-powered personal coach for goal achievement*")

if __name__ == "__main__":
    main() 