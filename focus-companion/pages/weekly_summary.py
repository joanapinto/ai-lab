"""
Weekly Summary Page for Focus Companion
AI-generated insights and rewards based on user's weekly data
"""

import streamlit as st
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add the parent directory to Python path
current_file = Path(__file__)
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from data.storage import load_user_profile, load_checkin_data, load_mood_data
from data.insights import DatabaseInsights
from assistant.ai_service import AIService
from assistant.fallback import FallbackAssistant
from auth import require_beta_access, get_user_email

st.set_page_config(
            page_title="Weekly Summary - Humsy",
    page_icon="📊",
    layout="wide"
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

# Custom navigation sidebar
with st.sidebar:
    st.subheader("🧭 Navigation")
    
    # Main pages
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("👤 Profile", use_container_width=True):
        st.switch_page("pages/profile.py")
    
    if st.button("📝 Daily Check-in", use_container_width=True):
        st.switch_page("pages/daily_checkin.py")
    
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
        from auth import logout
        logout()

# Require beta access
require_beta_access()

def get_week_date_range():
    """Get the date range for the current week (Monday to Sunday)"""
    today = datetime.now()
    # Find Monday of current week
    monday = today - timedelta(days=today.weekday())
    # Find Sunday of current week
    sunday = monday + timedelta(days=6)
    return monday.date(), sunday.date()

def get_week_data(checkin_data, mood_data, start_date, end_date):
    """Filter data for the current week"""
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
    
    return week_checkins, week_moods

def analyze_weekly_patterns(checkins, moods):
    """Analyze patterns in weekly data"""
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

def generate_weekly_summary_prompt(user_profile, week_analysis, start_date, end_date):
    """Generate a comprehensive prompt for AI weekly summary with structured questions"""
    
    # Calculate key metrics
    total_checkins = week_analysis['total_checkins']
    total_moods = week_analysis['total_mood_entries']
    
    # Find most active day
    day_counts = {}
    for day in week_analysis['checkin_days']:
        day_counts[day] = day_counts.get(day, 0) + 1
    most_active_day = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else None
    
    # Find highest energy day
    highest_energy_day = None
    highest_energy = 0
    for day, energies in week_analysis['energy_patterns'].items():
        # Convert energy levels to numbers for comparison
        energy_scores = []
        for energy in energies:
            if energy == 'High': energy_scores.append(5)
            elif energy == 'Good': energy_scores.append(4)
            elif energy == 'Moderate': energy_scores.append(3)
            elif energy == 'Low': energy_scores.append(2)
            elif energy == 'Very low': energy_scores.append(1)
        
        if energy_scores:
            avg_energy = sum(energy_scores) / len(energy_scores)
            if avg_energy > highest_energy:
                highest_energy = avg_energy
                highest_energy_day = day
    
    # Find most common mood
    all_moods = []
    for day_data in week_analysis['mood_patterns'].values():
        all_moods.extend(day_data['moods'])
    most_common_mood = max(set(all_moods), key=all_moods.count) if all_moods else None
    
    # Calculate average mood intensity
    all_intensities = []
    for day_data in week_analysis['mood_patterns'].values():
        all_intensities.extend(day_data['intensities'])
    avg_mood_intensity = sum(all_intensities) / len(all_intensities) if all_intensities else 5
    
    # Build the structured prompt
    prompt = f"""
You are a supportive wellness coach analyzing a user's weekly data to provide personalized insights.

USER CONTEXT:
- Goal: {user_profile.get('goal', 'Improve focus and productivity')}
- Tone: {user_profile.get('tone', 'Friendly')}
- Availability: {user_profile.get('availability', '2-4 hours')}

WEEKLY DATA ({start_date} to {end_date}):
- Check-ins: {total_checkins} | Mood entries: {total_moods}
- Active days: {', '.join(set(week_analysis['checkin_days'])) if week_analysis['checkin_days'] else 'None'}
- Energy patterns: {dict(week_analysis['energy_patterns'])}
- Mood patterns: {dict(week_analysis['mood_patterns'])}
- Accomplishments: {week_analysis['accomplishments']}
- Challenges: {week_analysis['challenges']}

TASK: Answer these 3-5 key questions based on their data:

1. **What mood dominated your week?** (Analyze mood patterns, intensity trends, emotional consistency)

2. **What gave you energy most consistently?** (Identify energy patterns, successful activities, positive triggers)

3. **What habits could help you next week?** (Suggest specific, actionable habits based on their patterns and goals)

4. **What's one thing you should celebrate?** (Highlight their biggest win or progress, no matter how small)

5. **What's one gentle improvement to consider?** (Suggest one specific, achievable improvement)

FORMAT: Answer each question in 1-2 sentences. Be specific, encouraging, and actionable. Reference their actual data and patterns.

TONE: {user_profile.get('tone', 'Friendly')}, supportive, and motivating.
"""
    
    return prompt

def main():
    st.title("📊 Weekly Summary")
    st.write("Your personalized AI-generated insights for this week")
    
    # Get user email
    user_email = get_user_email()
    if not user_email:
        st.error("Please log in to view your weekly summary")
        return
    
    # Load user data
    user_profile = load_user_profile(user_email)
    if not user_profile:
        st.warning("Please complete onboarding first!")
        if st.button("🚀 Go to Onboarding", use_container_width=True):
            st.switch_page("pages/onboarding.py")
        return
    
    # Get week date range
    start_date, end_date = get_week_date_range()
    
    # Display week range
    st.write(f"**Week of:** {start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}")
    
    # Load data
    checkin_data = load_checkin_data(user_email)
    mood_data = load_mood_data(user_email)
    
    # Filter data for current week
    week_checkins, week_moods = get_week_data(checkin_data, mood_data, start_date, end_date)
    
    # Analyze patterns
    week_analysis = analyze_weekly_patterns(week_checkins, week_moods)
    
    if not week_analysis or (week_analysis['total_checkins'] == 0 and week_analysis['total_mood_entries'] == 0):
        st.info("📝 **No data for this week yet!**")
        st.write("Start your wellness journey by completing your first check-in or mood entry.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Start Check-in", use_container_width=True):
                st.switch_page("pages/daily_checkin.py")
        with col2:
            if st.button("😊 Track Mood", use_container_width=True):
                st.switch_page("pages/mood_tracker.py")
        return
    
    # Display quick stats
    st.write("---")
    st.subheader("📈 This Week's Quick Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Check-ins", week_analysis['total_checkins'])
    with col2:
        st.metric("Mood Entries", week_analysis['total_mood_entries'])
    with col3:
        st.metric("Active Days", len(set(week_analysis['checkin_days'])))
    with col4:
        total_activities = week_analysis['total_checkins'] + week_analysis['total_mood_entries']
        st.metric("Total Activities", total_activities)
    
    # Generate AI summary
    st.write("---")
    st.subheader("🤖 Your AI-Generated Weekly Summary")
    
    # Show GPT quota badge
    display_gpt_quota_badge(user_email)
    
    # Show enhanced loading state with progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simulate progress steps
    status_text.text("🤖 Analyzing your weekly data...")
    progress_bar.progress(25)
    
    status_text.text("📊 Identifying patterns and trends...")
    progress_bar.progress(50)
    
    status_text.text("🧠 Crafting personalized insights...")
    progress_bar.progress(75)
    
    try:
        # Initialize AI service
        ai_service = AIService()
        
        # Generate prompt
        prompt = generate_weekly_summary_prompt(user_profile, week_analysis, start_date, end_date)
        
        # Get AI summary
        summary = ai_service.generate_weekly_summary(user_profile, week_analysis, user_email)
        
        # Complete progress
        progress_bar.progress(100)
        status_text.text("✅ Weekly insights ready!")
        
        if summary:
            st.success("✨ **Your Weekly Insights**")
            
            # Display structured summary
            display_structured_summary(summary)
            
            # Record AI usage
            ai_service.usage_limiter.record_api_call(
                user_email=user_email,
                feature="weekly_summary",
                tokens_used=None,  # Will be calculated by AI service
                cost_usd=None
            )
        else:
            # Fallback to rule-based summary
            st.info("📊 **Your Weekly Summary**")
            generate_fallback_summary(week_analysis, user_profile)
            
    except Exception as e:
        # Complete progress even on error
        progress_bar.progress(100)
        status_text.text("⚠️ Using fallback summary")
        st.warning("🤖 AI summary temporarily unavailable. Here's your weekly overview:")
        generate_fallback_summary(week_analysis, user_profile)
    
    # Display detailed patterns
    st.write("---")
    st.subheader("📊 Detailed Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📅 Check-in Patterns**")
        if week_analysis['checkin_days']:
            day_counts = {}
            for day in week_analysis['checkin_days']:
                day_counts[day] = day_counts.get(day, 0) + 1
            
            for day, count in sorted(day_counts.items(), key=lambda x: x[1], reverse=True):
                st.write(f"• **{day}**: {count} check-in{'s' if count > 1 else ''}")
        else:
            st.write("No check-ins this week")
        
        st.write("**⏰ Time Periods**")
        for period, count in week_analysis['time_periods'].items():
            st.write(f"• **{period.title()}**: {count} time{'s' if count > 1 else ''}")
    
    with col2:
        st.write("**😊 Mood Patterns**")
        if week_analysis['mood_patterns']:
            for day, data in week_analysis['mood_patterns'].items():
                if data['moods']:
                    most_common = max(set(data['moods']), key=data['moods'].count)
                    avg_intensity = sum(data['intensities']) / len(data['intensities'])
                    st.write(f"• **{day}**: {most_common} (avg intensity: {avg_intensity:.1f})")
        else:
            st.write("No mood entries this week")
        
        st.write("**🔋 Energy Patterns**")
        if week_analysis['energy_patterns']:
            for day, energies in week_analysis['energy_patterns'].items():
                most_common = max(set(energies), key=energies.count)
                st.write(f"• **{day}**: {most_common}")
        else:
            st.write("No energy data this week")
    
    # Accomplishments and challenges
    if week_analysis['accomplishments'] or week_analysis['challenges']:
        st.write("---")
        st.subheader("🎯 Key Highlights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if week_analysis['accomplishments']:
                st.write("**🏆 Accomplishments**")
                for accomplishment in week_analysis['accomplishments'][:3]:  # Show top 3
                    st.write(f"• {accomplishment[:100]}{'...' if len(accomplishment) > 100 else ''}")
        
        with col2:
            if week_analysis['challenges']:
                st.write("**🚧 Challenges**")
                for challenge in week_analysis['challenges'][:3]:  # Show top 3
                    st.write(f"• {challenge[:100]}{'...' if len(challenge) > 100 else ''}")
    
    # Next week suggestions
    st.write("---")
    st.subheader("🚀 Looking Ahead")
    
    # Calculate consistency score
    consistency_score = (len(set(week_analysis['checkin_days'])) / 7) * 100
    
    if consistency_score >= 70:
        st.success(f"🎉 **Excellent consistency!** You checked in on {len(set(week_analysis['checkin_days']))} out of 7 days this week.")
        st.write("Keep up the great work! Consider adding mood tracking to get even more insights.")
    elif consistency_score >= 50:
        st.info(f"👍 **Good progress!** You checked in on {len(set(week_analysis['checkin_days']))} out of 7 days this week.")
        st.write("Try to check in daily next week to build a stronger habit.")
    else:
        st.warning(f"💪 **Getting started!** You checked in on {len(set(week_analysis['checkin_days']))} out of 7 days this week.")
        st.write("Every check-in counts! Start with just one check-in per day.")
    
    # Action buttons
    st.write("---")
    st.subheader("📝 Continue Your Journey")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Daily Check-in", use_container_width=True):
            st.switch_page("pages/daily_checkin.py")
    
    with col2:
        if st.button("😊 Track Mood", use_container_width=True):
            st.switch_page("pages/mood_tracker.py")
    
    with col3:
        if st.button("📊 View History", use_container_width=True):
            st.switch_page("pages/history.py")

def display_structured_summary(summary):
    """Display the AI summary in a structured format"""
    
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
                display_question_answer(current_question, ' '.join(current_answer))
            
            # Start new question
            current_question = line
            current_answer = []
        else:
            # Add to current answer
            current_answer.append(line)
    
    # Display the last question
    if current_question and current_answer:
        display_question_answer(current_question, ' '.join(current_answer))

def display_question_answer(question, answer):
    """Display a single question and answer with nice formatting"""
    
    # Extract question text
    if '**' in question:
        question_text = question.split('**')[1].split('**')[0]
    else:
        question_text = question
    
    # Create a nice card-like display
    with st.container():
        st.markdown(f"### {question_text}")
        st.info(answer)
        st.write("---")

def generate_fallback_summary(week_analysis, user_profile):
    """Generate a rule-based summary when AI is unavailable"""
    
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