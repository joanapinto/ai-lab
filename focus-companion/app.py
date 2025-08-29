import streamlit as st
import os
import sys
from datetime import datetime, timedelta
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
        
        # Enhanced Dashboard Header
        st.write("---")
        st.subheader("🎯 Your Wellness Dashboard")
        
        # User goal and progress
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**Your Goal:** {user_profile.get('goal', 'Not set')}")
        with col2:
            # Calculate weekly consistency
            week_checkins = [c for c in checkin_data if (datetime.now() - datetime.fromisoformat(c['timestamp'])).days <= 7]
            consistency = len(set([datetime.fromisoformat(c['timestamp']).date() for c in week_checkins])) / 7 * 100
            st.metric("Weekly Consistency", f"{consistency:.0f}%")
        
        # Personalized greeting with enhanced styling
        greeting = assistant.get_personalized_greeting()
        if greeting:
            st.success(f"🤖 **AI Greeting:** {greeting}")
        
        # GPT Quota Badge
        display_gpt_quota_badge(user_email)
        
        # Mood and Energy Summary
        st.write("---")
        st.subheader("😊 How You've Been Feeling")
        
        # Get recent mood data
        recent_moods = mood_data[-5:] if mood_data else []
        recent_checkins = checkin_data[-5:] if checkin_data else []
        
        if recent_moods or recent_checkins:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if recent_moods:
                    avg_mood = sum(m.get('intensity', 5) for m in recent_moods) / len(recent_moods)
                    st.metric("Average Mood", f"{avg_mood:.1f}/10")
                    
                    # Mood trend
                    if len(recent_moods) >= 2:
                        first_mood = recent_moods[0].get('intensity', 5)
                        last_mood = recent_moods[-1].get('intensity', 5)
                        trend = "↗️" if last_mood > first_mood else "↘️" if last_mood < first_mood else "→"
                        st.write(f"**Trend:** {trend}")
                else:
                    st.info("No mood data yet")
            
            with col2:
                if recent_checkins:
                    energy_levels = [c.get('energy_level', 'Unknown') for c in recent_checkins if 'energy_level' in c]
                    if energy_levels:
                        most_common = max(set(energy_levels), key=energy_levels.count)
                        st.metric("Most Common Energy", most_common)
                        
                        # Energy distribution
                        high_energy = energy_levels.count('High') + energy_levels.count('Good')
                        energy_percent = (high_energy / len(energy_levels)) * 100
                        # Cap progress at 1.0 to avoid Streamlit error
                        progress_value = min(energy_percent / 100, 1.0)
                        st.progress(progress_value, text=f"{energy_percent:.0f}% High Energy")
                else:
                    st.info("No check-in data yet")
            
            with col3:
                # Activity streak
                if checkin_data:
                    today = datetime.now().date()
                    yesterday = today - timedelta(days=1)
                    
                    today_checkins = [c for c in checkin_data if datetime.fromisoformat(c['timestamp']).date() == today]
                    yesterday_checkins = [c for c in checkin_data if datetime.fromisoformat(c['timestamp']).date() == yesterday]
                    
                    if today_checkins:
                        st.success("✅ **Today:** Checked in")
                    elif yesterday_checkins:
                        st.warning("⚠️ **Today:** No check-in yet")
                    else:
                        st.info("📝 **Today:** Ready to start")
                else:
                    st.info("📝 Ready for your first check-in")
        
        # Daily encouragement and tips
        st.write("---")
        st.subheader("💡 Daily Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            encouragement = assistant.get_daily_encouragement()
            if encouragement:
                st.info(f"💬 **Encouragement:** {encouragement}")
        
        with col2:
            tip = assistant.get_productivity_tip()
            if tip:
                st.info(f"💡 **Today's Tip:** {tip}")
        
        # Quick Actions with Progress Indicators
        st.write("---")
        st.subheader("🚀 Quick Actions")
        
        # Calculate completion status for different features
        today_checkins = [c for c in checkin_data if datetime.fromisoformat(c['timestamp']).date() == datetime.now().date()]
        today_moods = [m for m in mood_data if datetime.fromisoformat(m['timestamp']).date() == datetime.now().date()]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            checkin_status = "✅ Complete" if today_checkins else "📝 Pending"
            checkin_color = "success" if today_checkins else "info"
            if st.button(f"📝 Daily Check-in\n{checkin_status}", use_container_width=True, type="primary" if not today_checkins else "secondary"):
                st.switch_page("pages/daily_checkin.py")
        
        with col2:
            mood_status = "✅ Complete" if today_moods else "😊 Pending"
            mood_color = "success" if today_moods else "info"
            if st.button(f"😊 Track Mood\n{mood_status}", use_container_width=True, type="primary" if not today_moods else "secondary"):
                st.switch_page("pages/mood_tracker.py")
        
        with col3:
            if st.button("📊 Weekly Summary", use_container_width=True):
                st.switch_page("pages/weekly_summary.py")
        
        with col4:
            # Only show insights button for admin
            ADMIN_EMAIL = "joanapnpinto@gmail.com"
            if user_email == ADMIN_EMAIL:
                if st.button("📈 View Insights", use_container_width=True):
                    st.switch_page("pages/insights.py")
            else:
                # Show a placeholder or different button for non-admin users
                st.button("📈 View Insights", use_container_width=True, disabled=True, help="Admin only during beta testing")
        
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
                        # Cap progress at 1.0 to avoid Streamlit error
                        progress_value = min(user_daily / user_daily_limit, 1.0)
                        st.progress(progress_value)
                    
                    with col2:
                        user_monthly = stats["user"]["monthly_used"]
                        user_monthly_limit = stats["user"]["monthly_limit"]
                        st.metric("Your Monthly Calls", f"{user_monthly}/{user_monthly_limit}")
                        # Cap progress at 1.0 to avoid Streamlit error
                        progress_value = min(user_monthly / user_monthly_limit, 1.0)
                        st.progress(progress_value)
                    
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
                    
                    # Cache statistics
                    try:
                        from assistant.ai_cache import ai_cache
                        cache_stats = ai_cache.get_cache_stats()
                        if cache_stats['total_entries'] > 0:
                            st.subheader("⚡ Cache Performance")
                            st.info(f"**Cache hits:** {cache_stats['total_entries']} entries | **Size:** {cache_stats['cache_size_mb']:.2f} MB")
                            st.write("💡 *Smart caching is reducing API calls and improving response times*")
                    except Exception:
                        pass  # Silently fail if cache not available
        

        
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

def display_gpt_quota_badge(user_email):
    """Display GPT quota usage badge"""
    if not user_email:
        return
    
    try:
        from assistant.usage_limiter import UsageLimiter
        usage_limiter = UsageLimiter()
        
        # Get user's current usage
        user_usage = usage_limiter.db.get_user_api_usage(user_email, days=1)
        daily_used = sum(user_usage["daily_usage"].values())
        daily_limit = usage_limiter.user_daily_limit
        
        # Calculate usage percentage
        usage_percentage = (daily_used / daily_limit) * 100
        
        # Determine badge color and message
        if usage_percentage >= 80:
            badge_color = "error"
            message = f"⚠️ You've used {daily_used}/{daily_limit} AI insights today. Almost at your limit!"
        elif usage_percentage >= 60:
            badge_color = "warning"
            message = f"📊 You've used {daily_used}/{daily_limit} AI insights today. Want more? Upgrade coming soon!"
        else:
            badge_color = "info"
            message = f"🤖 You've used {daily_used}/{daily_limit} AI insights today. {daily_limit - daily_used} remaining!"
        
        # Display the badge
        if badge_color == "error":
            st.error(message)
        elif badge_color == "warning":
            st.warning(message)
        else:
            st.info(message)
            
    except Exception as e:
        # Silently fail if there's an issue with usage tracking
        pass

if __name__ == "__main__":
    main()
