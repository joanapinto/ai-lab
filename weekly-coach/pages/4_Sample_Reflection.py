import streamlit as st

st.set_page_config(page_title="Sample Weekly Reflection", page_icon="📝")

def sample_reflection_demo():
    st.title("📝 Sample Weekly Reflection")
    st.markdown("See how weekly reflections provide insights")
    
    # Add a back button
    if st.button("← Back to Home"):
        st.switch_page("main.py")
    
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
    
    st.markdown("---")
    st.markdown("### 🚀 Ready to start your own reflections?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 Start Setup", type="primary", use_container_width=True):
            st.switch_page("pages/1_Setup.py")
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("main.py")

if __name__ == "__main__":
    sample_reflection_demo() 