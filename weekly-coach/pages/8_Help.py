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