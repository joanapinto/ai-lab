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
        
        # Beta tester guide
        if st.button("📋 Beta Tester Guide", use_container_width=True):
            st.markdown("""
            ### 🚀 **Beta Tester Guide**
            
            **🎯 Quick Start:**
            1. **Start with a morning check-in** - It's the heart of the app!
            2. **Track your mood** - Build patterns and insights
            3. **Try the AI features** - Personalized greetings and tips
            4. **Explore weekly reflections** - Learn from your patterns
            
            **💡 Pro Tips:**
            - **Be consistent** - Daily check-ins build the most valuable insights
            - **Use the AI features** - They get smarter with your data
            - **Don't worry about perfection** - Just log how you're feeling
            - **Try different times** - Morning, afternoon, and evening check-ins
            
            **🤖 AI Features:**
            - **Personalized greetings** - AI that knows your patterns
            - **Smart task planning** - Based on your energy and goals
            - **Usage limits** - 20 AI calls per day, 400 per month
            - **Graceful fallback** - Works perfectly even without AI
            
            **⚠️ Beta Expectations:**
            - This is a **beta version** - some things might change
            - **AI features** have usage limits to control costs
            - **Data is saved locally** - your privacy is protected
            - **Updates** will add new features based on your feedback
            
            **🎁 Beta Perks:**
            - **Early access** to new features
            - **Direct influence** on development
            - **Priority support** for issues
            - **Exclusive insights** into the development process
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
    
    # Check if user has completed onboarding
    user_profile = load_user_profile()
    
    # Beta tester welcome message
    if user_profile:
        # Check if this is a new user (first time seeing the welcome)
        if "beta_welcome_shown" not in st.session_state:
            st.session_state.beta_welcome_shown = True
            
            st.success("🎉 **Welcome to Focus Companion Beta!**")
            
            with st.expander("📋 Beta Tester Guide", expanded=True):
                st.markdown("""
                ### 🚀 **Welcome, Beta Tester!**
                
                You're among the first to try Focus Companion! Here's how to get the most value:
                
                **🎯 Quick Start:**
                1. **Start with a morning check-in** - It's the heart of the app!
                2. **Track your mood** - Build patterns and insights
                3. **Try the AI features** - Personalized greetings and tips
                4. **Explore weekly reflections** - Learn from your patterns
                
                **💡 Pro Tips:**
                - **Be consistent** - Daily check-ins build the most valuable insights
                - **Use the AI features** - They get smarter with your data
                - **Don't worry about perfection** - Just log how you're feeling
                - **Try different times** - Morning, afternoon, and evening check-ins
                
                **🤖 AI Features:**
                - **Personalized greetings** - AI that knows your patterns
                - **Smart task planning** - Based on your energy and goals
                - **Usage limits** - 20 AI calls per day, 400 per month
                - **Graceful fallback** - Works perfectly even without AI
                
                **📝 Feedback:**
                - **Share your thoughts** - Use the feedback forms throughout the app
                - **Report bugs** - Help us improve the experience
                - **Suggest features** - Your input shapes the future!
                
                **⚠️ Beta Expectations:**
                - This is a **beta version** - some things might change
                - **AI features** have usage limits to control costs
                - **Data is saved locally** - your privacy is protected
                - **Updates** will add new features based on your feedback
                
                **🎁 Beta Perks:**
                - **Early access** to new features
                - **Direct influence** on development
                - **Priority support** for issues
                - **Exclusive insights** into the development process
                """)
                
                # Quick action buttons
                st.markdown("### 🚀 Ready to get started?")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📝 Start Morning Check-in", use_container_width=True, type="primary"):
                        st.switch_page("pages/daily_checkin.py")
                with col2:
                    if st.button("😊 Track My Mood", use_container_width=True):
                        st.switch_page("pages/mood_tracker.py")
                with col3:
                    if st.button("📊 View My History", use_container_width=True):
                        st.switch_page("pages/history.py")
                
                st.markdown("---")
                st.info("💡 **Tip:** You can always access this guide from the sidebar under 'Feedback'")
        
        st.write("Welcome to your personal focus assistant!")
    else:
        st.write("Welcome to your personal focus assistant!")
    
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
            
            with st.expander("🤖 AI Usage Statistics", expanded=False):
                # Global usage
                st.subheader("🌍 Global Usage")
                col1, col2, col3 = st.columns(3)
                with col1:
                    daily_used = stats["global"]["daily_used"]
                    daily_limit = stats["global"]["daily_limit"]
                    st.metric("Daily API Calls", f"{daily_used}/{daily_limit}")
                    st.progress(daily_used / daily_limit)
                
                with col2:
                    monthly_used = stats["global"]["monthly_used"]
                    monthly_limit = stats["global"]["monthly_limit"]
                    st.metric("Monthly API Calls", f"{monthly_used}/{monthly_limit}")
                    st.progress(monthly_used / monthly_limit)
                
                with col3:
                    total_cost = stats["global"]["total_cost"]
                    st.metric("Total Cost", f"${total_cost:.4f}")
                
                # User usage
                if "user" in stats:
                    st.subheader("👤 Your Usage")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        user_daily = stats["user"]["daily_used"]
                        user_daily_limit = stats["user"]["daily_limit"]
                        st.metric("Your Daily Calls", f"{user_daily}/{user_daily_limit}")
                        st.progress(user_daily / user_daily_limit)
                    
                    with col2:
                        user_monthly = stats["user"]["monthly_used"]
                        user_monthly_limit = stats["user"]["monthly_limit"]
                        st.metric("Your Monthly Calls", f"{user_monthly}/{user_monthly_limit}")
                        st.progress(user_monthly / user_monthly_limit)
                    
                    with col3:
                        user_cost = stats["user"]["total_cost"]
                        st.metric("Your Cost", f"${user_cost:.4f}")
                    
                    # Feature breakdown
                    if "feature_usage" in stats["user"]:
                        st.subheader("🔧 Feature Usage")
                        feature_usage = stats["user"]["feature_usage"]
                        if feature_usage:
                            for feature, count in feature_usage.items():
                                st.write(f"• **{feature.title()}**: {count} calls")
                        else:
                            st.info("No AI features used yet")
                    
                    # Show warnings if approaching limits
                    if user_daily >= user_daily_limit * 0.8:
                        st.warning("⚠️ You're approaching your daily AI usage limit!")
                    if user_monthly >= user_monthly_limit * 0.8:
                        st.warning("⚠️ You're approaching your monthly AI usage limit!")
        
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
            if st.button("📈 Insights", use_container_width=True):
                st.switch_page("pages/insights.py")
        
        # Additional navigation row
        col5, col6 = st.columns(2)
        with col5:
            if st.button("📊 Weekly Summary", use_container_width=True):
                st.switch_page("pages/weekly_summary.py")
        with col6:
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
