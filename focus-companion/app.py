import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the working directory and Python path
current_dir = Path(__file__).parent
os.chdir(current_dir)
sys.path.insert(0, str(current_dir))

# Import the storage functions
from data.storage import save_user_profile, load_user_profile, reset_user_profile, load_mood_data, load_checkin_data

# Import the assistant system
from assistant.fallback import FallbackAssistant

# Import authentication
from auth import require_beta_access, get_user_email, logout

# Set page config
st.set_page_config(
    page_title="Focus Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Require beta access for the main app
require_beta_access()

# Main app logic
def main():
    # Add logout option to sidebar
    with st.sidebar:
        st.write("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
        
        # Feedback section
        st.write("---")
        st.subheader("💬 Feedback")
        st.write("Help us improve Focus Companion!")
        
        # Feedback button
        if st.button("📝 Give Feedback", use_container_width=True):
            st.markdown("""
            ### 📝 We'd love your feedback!
            
            Please take a moment to share your thoughts about Focus Companion:
            
            **[📋 Open Feedback Form](https://tally.so/r/mBr11Q)**
            
            Your feedback helps us make the app better for everyone! 🚀
            """)
        
        # Quick feedback options
        st.write("**Quick feedback:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍", help="I like this feature"):
                st.success("Thanks for the feedback! 🙏")
        with col2:
            if st.button("👎", help="This needs improvement"):
                st.info("We'd love to hear more details in the feedback form above! 📝")
    
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
        
        # Show usage stats if user is logged in
        user_email = get_user_email()
        if user_email:
            from assistant.usage_limiter import UsageLimiter
            usage_limiter = UsageLimiter()
            stats = usage_limiter.get_usage_stats(user_email)
            
            with st.expander("📊 AI Usage Stats"):
                if "user" in stats:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Daily Usage", f"{stats['user']['daily_used']}/{stats['user']['daily_limit']}")
                    with col2:
                        st.metric("Monthly Usage", f"{stats['user']['monthly_used']}/{stats['user']['monthly_limit']}")
                    
                    # Show progress bars
                    daily_progress = stats['user']['daily_used'] / stats['user']['daily_limit']
                    monthly_progress = stats['user']['monthly_used'] / stats['user']['monthly_limit']
                    
                    st.progress(daily_progress, text="Daily Progress")
                    st.progress(monthly_progress, text="Monthly Progress")
                    
                    if daily_progress > 0.8:
                        st.warning("⚠️ You're approaching your daily AI usage limit")
                    if monthly_progress > 0.8:
                        st.warning("⚠️ You're approaching your monthly AI usage limit")
        
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
        
        # Additional navigation row
        col3, col4 = st.columns(2)
        with col3:
            if st.button("📖 Mood Journal", use_container_width=True):
                st.switch_page("pages/mood_journal.py")
        with col4:
            st.write("")  # Empty space for balance
        
        # Feedback section on main dashboard
        st.write("---")
        st.subheader("💬 Help Us Improve Focus Companion")
        
        col_feedback1, col_feedback2, col_feedback3 = st.columns(3)
        
        with col_feedback1:
            st.info("**How's your experience?**")
            st.write("We'd love to hear your thoughts!")
        
        with col_feedback2:
            if st.button("📝 Share Feedback", use_container_width=True, type="primary"):
                st.markdown("""
                ### 📝 Thank you for wanting to help!
                
                **[📋 Open Feedback Form](https://tally.so/r/mBr11Q)**
                
                Your feedback is invaluable for making Focus Companion better! 🚀
                """)
        
        with col_feedback3:
            st.success("**Beta Tester Perks**")
            st.write("Early access to new features!")
            st.write("Direct influence on development!")

if __name__ == "__main__":
    main()
