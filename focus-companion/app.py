import streamlit as st
import os
import sys
from pathlib import Path

# Set up the working directory and Python path
current_dir = Path(__file__).parent
os.chdir(current_dir)
sys.path.insert(0, str(current_dir))

# Import the storage functions
from data.storage import save_user_profile, load_user_profile, reset_user_profile

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
        st.success("👋 Welcome back!")
        st.write(f"Your goal: {user_profile.get('goal', 'Not set')}")
        
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
