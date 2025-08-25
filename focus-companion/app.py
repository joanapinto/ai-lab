import streamlit as st
import os
import sys
from pathlib import Path

# Set up the working directory and Python path
current_dir = Path(__file__).parent
os.chdir(current_dir)
sys.path.insert(0, str(current_dir))

# Import the storage functions
from data.storage import save_user_profile, load_user_profile, reset_user_profile, load_mood_data, load_checkin_data

# Import the assistant system
from assistant.fallback import FallbackAssistant

# Set page config
st.set_page_config(
    page_title="Focus Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main app logic
def main():
    st.title("🧠 Focus Companion")
    st.write("Welcome to your personal focus assistant!")
    
    # Check if user has completed onboarding
    user_profile = load_user_profile()
    
    if not user_profile:
        st.info("👋 First time here? Let's get you set up!")
        if st.button("🚀 Start Onboarding", use_container_width=True):
            st.switch_page("pages/onboarding.py")
    else:
        # Load user data for assistant
        mood_data = load_mood_data()
        checkin_data = load_checkin_data()
        
        # Initialize assistant
        assistant = FallbackAssistant(user_profile, mood_data, checkin_data)
        
        # Personalized greeting
        greeting = assistant.get_personalized_greeting()
        st.success(greeting)
        
        # Show user goal
        st.write(f"**Your goal:** {user_profile.get('goal', 'Not set')}")
        
        # Daily encouragement
        encouragement = assistant.get_daily_encouragement()
        st.info(encouragement)
        
        # Quick tip
        tip = assistant.get_productivity_tip()
        st.info(f"💡 **Today's Tip:** {tip}")
        
        # Navigation options
        col1, col2 = st.columns(2)
        
        with col1:
            col1a, col1b = st.columns(2)
            with col1a:
                if st.button("📝 Daily Check-in", use_container_width=True):
                    st.switch_page("pages/daily_checkin.py")
            with col1b:
                if st.button("😊 Mood Tracker", use_container_width=True):
                    st.switch_page("pages/mood_tracker.py")
        
        with col2:
            col2a, col2b = st.columns(2)
            with col2a:
                if st.button("🤔 Reflection", use_container_width=True):
                    st.switch_page("pages/reflection.py")
            with col2b:
                if st.button("📊 History", use_container_width=True):
                    st.switch_page("pages/history.py")

if __name__ == "__main__":
    main()
