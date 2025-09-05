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
    page_title="Humsy",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit's default navigation
hide_streamlit_navigation = """
<style>
    /* Hide the automatic pages navigation */
    .stSidebar > div:first-child > div:first-child > div:nth-child(2) {
        display: none;
    }
    
    /* Hide the default page navigation */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Hide any remaining automatic navigation */
    .css-1544g2n {
        display: none;
    }
</style>
"""
st.markdown(hide_streamlit_navigation, unsafe_allow_html=True)

# Require beta access for the main app
require_beta_access()

# Main app logic
def main():
    # Main navigation sidebar
    with st.sidebar:
        st.subheader("🧭 Navigation")
        
        # Main pages
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
        
        if st.button("👤 Profile", use_container_width=True):
            st.switch_page("pages/profile.py")
        
        if st.button("📝 Daily Check-in", use_container_width=True):
            st.switch_page("pages/daily_checkin.py")
        
        if st.button("😊 Mood Tracker", use_container_width=True):
            st.switch_page("pages/mood_tracker.py")
        
        if st.button("🌱 Weekly Reflection", use_container_width=True):
            st.switch_page("pages/reflection.py")
        
        if st.button("📊 Insights", use_container_width=True):
            st.switch_page("pages/history.py")
        
        st.write("---")
        
        # Admin insights access
        user_email = get_user_email()
        if user_email == "joanapnpinto@gmail.com":
            st.subheader("🔓 Admin Tools")
            if st.button("📊 Database Insights", use_container_width=True):
                st.switch_page("pages/insights.py")
        
        st.write("---")
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    st.title("🧠 Humsy")
    
    # Check if user has completed onboarding
    user_profile = load_user_profile()
    
    # Beta tester welcome message
    if user_profile:
        # Check if this is a new user (first time seeing the welcome)
        if "beta_welcome_shown" not in st.session_state:
            st.session_state.beta_welcome_shown = True
            
            st.success("🎉 **Welcome to Humsy Beta!**")
            
            with st.expander("📋 Beta Tester Guide", expanded=True):
                st.markdown("""
                ### 🚀 **Welcome, Beta Tester!**
                
                You're among the first to try Humsy! Here's how to get the most value:
                
                **🎯 Quick Start:**
                1. **Start with a morning check-in** - It's the heart of the app!
                2. **Track your mood** - Enhanced mood tracking with multiple emotions and reasons
                3. **Try the AI features** - Personalized greetings and smart task planning
                4. **Explore weekly reflections** - Learn from your patterns
                5. **Use the sidebar navigation** - Easy access to all features
                
                **💡 Pro Tips:**
                - **Be consistent** - Daily check-ins build the most valuable insights
                - **Track multiple moods** - You can feel happy AND calm at the same time!
                - **Add reasons for your moods** - Helps identify patterns and triggers
                - **Use the AI features** - They get smarter with your data
                - **Don't worry about perfection** - Just log how you're feeling
                
                **😊 Enhanced Mood Tracking:**
                - **Multiple emotions** - Select several moods that describe how you feel
                - **Mood reasons** - Track what's influencing your emotions
                - **Visual analytics** - See your mood patterns over time
                - **Smart insights** - AI-powered mood analysis and recommendations
                
                **🤖 AI Features:**
                - **Personalized greetings** - AI that knows your patterns and mood trends
                - **Smart task planning** - Based on your energy, mood, and goals
                - **Mood analysis** - Insights into your emotional patterns
                - **Usage limits** - 20 AI calls per day, 400 per month
                - **Graceful fallback** - Works perfectly even without AI
                
                **🧭 Navigation:**
                - **Sidebar menu** - Quick access to all features
                - **Mood Tracker** - Dedicated button between Daily Check-in and Weekly Reflection
                - **Consistent experience** - Same navigation across all pages
                
                **📝 Feedback:**
                - **Share your thoughts** - Use the feedback forms throughout the app
                - **Report bugs** - Help us improve the experience
                - **Suggest features** - Your input shapes the future!
                
                **⚠️ Beta Expectations:**
                - This is a **beta version** - some things might change
                - **AI features** have usage limits to control costs
                - **Data is saved locally** - your privacy is protected
                - **Updates** will add new features based on your feedback
                - **Recent improvements** - Fixed data compatibility and enhanced mood tracking
                
                **🎁 Beta Perks:**
                - **Early access** to new features
                - **Direct influence** on development
                - **Priority support** for issues
                - **Exclusive insights** into the development process
                - **Enhanced mood tracking** - More detailed emotional insights
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
            current_goal = user_profile.get('goal', 'Not set')
            st.write(f"**Your Goal:** {current_goal}")
            if st.button("✏️ Want to change?", use_container_width=True):
                st.switch_page("pages/profile.py")
        with col2:
            # Calculate weekly consistency
            week_checkins = [c for c in checkin_data if (datetime.now() - datetime.fromisoformat(c['timestamp'])).days <= 7]
            consistency = len(set([datetime.fromisoformat(c['timestamp']).date() for c in week_checkins])) / 7 * 100
            st.metric("Weekly Consistency", f"{consistency:.0f}%")
            st.caption("📊 % of days you checked in this week")
        
        # Personalized greeting with enhanced styling
        greeting = assistant.get_personalized_greeting()
        if greeting:
            st.success(f"🤖 **AI Greeting:** {greeting}")
        
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
                # Add expander for longer tips
                if len(tip) > 100:
                    with st.expander("📖 Read full tip"):
                        st.write(tip)
        
        # Daily reminder right after insights
        st.write("---")
        st.subheader("💭 Daily Reminder")
        st.info("🌟 **Remember:** Small steps lead to big changes. Every check-in brings you closer to your goals!")
        
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
            if st.button("📈 View Insights", use_container_width=True):
                st.switch_page("pages/history.py")
        
        # Show usage stats if user is logged in
        user_email = get_user_email()
        if user_email:
            # GPT Quota Badge
            display_gpt_quota_badge(user_email)
            
            # Admin check for insights access
            ADMIN_EMAIL = "joanapnpinto@gmail.com"
            if user_email == ADMIN_EMAIL:
                st.success("🔓 **Admin Access**: You can access Database Insights from the sidebar or navigation.")
            else:
                st.info("🔒 **Beta Testing**: Database Insights are admin-only during beta testing.")
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
                    # Cap progress at 1.0 to avoid Streamlit error
                    progress_value = min(daily_used / daily_limit, 1.0)
                    st.progress(progress_value)
                
                with col2:
                    monthly_used = stats["global"]["monthly_used"]
                    monthly_limit = stats["global"]["monthly_limit"]
                    st.metric("Monthly API Calls", f"{monthly_used}/{monthly_limit}")
                    # Cap progress at 1.0 to avoid Streamlit error
                    progress_value = min(monthly_used / monthly_limit, 1.0)
                    st.progress(progress_value)
                
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

def generate_weekly_summary_inline(user_email, user_profile, mood_data, checkin_data):
    """Generate and display weekly summary inline in the main app"""
    
    if not user_email or not user_profile:
        st.error("Please complete onboarding first!")
        return
    
    # Get week date range
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    start_date, end_date = monday.date(), sunday.date()
    
    # Filter data for current week
    week_checkins = []
    week_moods = []
    
    for checkin in checkin_data:
        checkin_date = datetime.fromisoformat(checkin['timestamp']).date()
        if start_date <= checkin_date <= end_date:
            week_checkins.append(checkin)
    
    for mood in mood_data:
        mood_date = datetime.fromisoformat(mood['timestamp']).date()
        if start_date <= mood_date <= end_date:
            week_moods.append(mood)
    
    # Analyze patterns
    week_analysis = analyze_weekly_patterns_inline(week_checkins, week_moods)
    
    if not week_analysis or (week_analysis['total_checkins'] == 0 and week_analysis['total_mood_entries'] == 0):
        st.info("📝 **No data for this week yet!** Start your wellness journey by completing your first check-in or mood entry.")
        return
    
    # Display week range
    st.write("---")
    st.subheader(f"📊 Weekly Summary ({start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')})")
    
    # Show loading animation
    with st.spinner("🤖 Generating your personalized weekly insights..."):
        try:
            # Initialize AI service
            from assistant.ai_service import AIService
            ai_service = AIService()
            
            # Generate prompt
            prompt = generate_weekly_summary_prompt_inline(user_profile, week_analysis, start_date, end_date)
            
            # Get AI summary with loading animation
            summary = ai_service.generate_weekly_summary(user_profile, week_analysis, user_email)
            
            if summary:
                st.success("✨ **Your Weekly Insights**")
                
                # Display structured summary
                display_structured_summary_inline(summary)
                
                # Add a "View Full Summary" button
                if st.button("📖 View Full Weekly Summary Page", use_container_width=True):
                    st.switch_page("pages/weekly_summary.py")
                
            else:
                # Fallback to rule-based summary
                st.info("📊 **Your Weekly Summary**")
                generate_fallback_summary_inline(week_analysis, user_profile)
                
        except Exception as e:
            st.warning("🤖 AI summary temporarily unavailable. Here's your weekly overview:")
            generate_fallback_summary_inline(week_analysis, user_profile)

def analyze_weekly_patterns_inline(checkins, moods):
    """Analyze patterns in weekly data for inline summary"""
    if not checkins and not moods:
        return None
    
    analysis = {
        'total_checkins': len(checkins),
        'total_mood_entries': len(moods),
        'checkin_days': [],
        'mood_days': [],
        'energy_patterns': {},
        'mood_patterns': {},
        'time_periods': {},
        'accomplishments': [],
        'challenges': []
    }
    
    # Analyze check-ins
    for checkin in checkins:
        date = datetime.fromisoformat(checkin['timestamp']).date()
        day_name = date.strftime('%A')
        analysis['checkin_days'].append(day_name)
        
        # Energy patterns
        if 'energy_level' in checkin:
            energy = checkin['energy_level']
            if day_name not in analysis['energy_patterns']:
                analysis['energy_patterns'][day_name] = []
            analysis['energy_patterns'][day_name].append(energy)
        
        # Time periods
        time_period = checkin.get('time_period', 'unknown')
        if time_period not in analysis['time_periods']:
            analysis['time_periods'][time_period] = 0
        analysis['time_periods'][time_period] += 1
        
        # Accomplishments and challenges
        if 'accomplishments' in checkin and checkin['accomplishments']:
            analysis['accomplishments'].append(checkin['accomplishments'])
        if 'challenges' in checkin and checkin['challenges']:
            analysis['challenges'].append(checkin['challenges'])
    
    # Analyze mood data
    for mood in moods:
        date = datetime.fromisoformat(mood['timestamp']).date()
        day_name = date.strftime('%A')
        analysis['mood_days'].append(day_name)
        
        mood_type = mood.get('mood', 'unknown')
        intensity = mood.get('intensity', 5)
        
        if day_name not in analysis['mood_patterns']:
            analysis['mood_patterns'][day_name] = {'moods': [], 'intensities': []}
        analysis['mood_patterns'][day_name]['moods'].append(mood_type)
        analysis['mood_patterns'][day_name]['intensities'].append(intensity)
    
    return analysis

def generate_weekly_summary_prompt_inline(user_profile, week_analysis, start_date, end_date):
    """Generate optimized prompt for inline weekly summary"""
    
    # Extract essential data
    essential_data = {
        'checkins': week_analysis['total_checkins'],
        'moods': week_analysis['total_mood_entries'],
        'active_days': len(set(week_analysis['checkin_days'])),
        'goal': user_profile.get('goal', 'Improve focus and productivity'),
        'tone': user_profile.get('tone', 'Friendly')
    }
    
    # Find key patterns efficiently
    if week_analysis['energy_patterns']:
        energy_days = list(week_analysis['energy_patterns'].keys())
        essential_data['energy_days'] = energy_days[:3]  # Top 3 days
    
    if week_analysis['mood_patterns']:
        all_moods = []
        for day_data in week_analysis['mood_patterns'].values():
            all_moods.extend(day_data['moods'])
        if all_moods:
            essential_data['top_mood'] = max(set(all_moods), key=all_moods.count)
    
    # Create concise prompt
    prompt = f"""
Analyze weekly wellness data and provide encouraging insights.

User: {essential_data['goal']} | Tone: {essential_data['tone']}
Data: {essential_data['checkins']} check-ins, {essential_data['moods']} moods, {essential_data['active_days']} active days
Patterns: Energy peaks on {essential_data.get('energy_days', ['N/A'])} | Top mood: {essential_data.get('top_mood', 'N/A')}

Answer these 3 key questions in 1-2 sentences each:
1. **What mood dominated your week?**
2. **What gave you energy most consistently?**
3. **What's one habit that could help you next week?**
"""
    
    return prompt

def display_structured_summary_inline(summary):
    """Display the AI summary in a structured format for inline display"""
    
    # Split the summary into sections based on numbered questions
    lines = summary.strip().split('\n')
    current_question = None
    current_answer = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a new question (starts with number and **)
        if line.startswith(('1.', '2.', '3.', '4.', '5.')) and '**' in line:
            # Save previous question if exists
            if current_question and current_answer:
                display_question_answer_inline(current_question, ' '.join(current_answer))
            
            # Start new question
            current_question = line
            current_answer = []
        else:
            # Add to current answer
            current_answer.append(line)
    
    # Display the last question
    if current_question and current_answer:
        display_question_answer_inline(current_question, ' '.join(current_answer))

def display_question_answer_inline(question, answer):
    """Display a single question and answer with nice formatting for inline"""
    
    # Extract question text
    if '**' in question:
        question_text = question.split('**')[1].split('**')[0]
    else:
        question_text = question
    
    # Create a nice card-like display
    with st.container():
        st.markdown(f"**{question_text}**")
        st.info(answer)

def generate_fallback_summary_inline(week_analysis, user_profile):
    """Generate a rule-based summary when AI is unavailable for inline display"""
    
    total_checkins = week_analysis['total_checkins']
    total_moods = week_analysis['total_mood_entries']
    
    # Basic summary
    summary = f"Great job this week! You completed {total_checkins} check-in{'s' if total_checkins != 1 else ''} "
    summary += f"and logged {total_moods} mood entr{'ies' if total_moods != 1 else 'y'}. "
    
    # Consistency message
    active_days = len(set(week_analysis['checkin_days']))
    if active_days >= 5:
        summary += "You've been very consistent with your wellness routine! "
    elif active_days >= 3:
        summary += "You're building a great habit. Keep it up! "
    else:
        summary += "Every check-in helps you understand your patterns better. "
    
    # Energy insights
    if week_analysis['energy_patterns']:
        # Find highest energy day
        highest_energy_day = None
        highest_energy = 0
        for day, energies in week_analysis['energy_patterns'].items():
            high_count = energies.count('High')
            if high_count > highest_energy:
                highest_energy = high_count
                highest_energy_day = day
        
        if highest_energy_day:
            summary += f"Your energy was highest on {highest_energy_day}. "
    
    # Mood insights
    if week_analysis['mood_patterns']:
        all_moods = []
        for day_data in week_analysis['mood_patterns'].values():
            all_moods.extend(day_data['moods'])
        
        if all_moods:
            most_common_mood = max(set(all_moods), key=all_moods.count)
            summary += f"Your most common mood was {most_common_mood}. "
    
    # Accomplishments
    if week_analysis['accomplishments']:
        summary += f"You accomplished {len(week_analysis['accomplishments'])} thing{'s' if len(week_analysis['accomplishments']) != 1 else ''} this week. "
    
    # Encouragement
    summary += "Keep up the great work on your wellness journey!"
    
    st.write(summary)

if __name__ == "__main__":
    main()
