import streamlit as st

st.set_page_config(page_title="Sample Daily Check-in", page_icon="🌤️")

def sample_checkin_demo():
    st.title("🌤️ Sample Daily Check-in")
    st.markdown("See how daily check-ins work")
    
    # Add a back button
    if st.button("← Back to Home"):
        st.switch_page("main.py")
    
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
    
    st.markdown("---")
    st.markdown("### 🚀 Ready to start your own check-ins?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 Start Setup", type="primary", use_container_width=True):
            st.switch_page("pages/1_Setup.py")
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("main.py")

if __name__ == "__main__":
    sample_checkin_demo() 