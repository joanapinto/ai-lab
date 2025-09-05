import streamlit as st
import os
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

# Add the parent directory to the Python path to find the data module
current_file = Path(__file__)
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from data.storage import save_user_profile, load_user_profile, save_checkin_data, load_checkin_data, load_mood_data
from assistant.fallback import FallbackAssistant
from auth import require_beta_access, get_user_email

st.set_page_config(page_title="Humsy - Daily Check-in", page_icon="📝")

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
        from auth import logout
        logout()

# Require beta access
require_beta_access()

st.title("📝 Daily Check-in")

# Load user profile
user_profile = load_user_profile()

if not user_profile:
    st.warning("Please complete onboarding first!")
    if st.button("🚀 Go to Onboarding", use_container_width=True):
        st.switch_page("pages/onboarding.py")
else:
    # Load user data for context
    mood_data = load_mood_data()
    checkin_data = load_checkin_data()
    
    # Initialize assistant for personalized insights
    assistant = FallbackAssistant(user_profile, mood_data, checkin_data)
    
    # Initialize AI service for task planning
    try:
        from assistant.ai_service import AIService
        ai_service = AIService()
        from auth import get_user_email
        user_email = get_user_email()
        ai_service_available = True
    except Exception as e:
        st.warning(f"🤖 AI service initialization failed: {str(e)}")
        ai_service_available = False
        ai_service = None
        user_email = None
    
    # Determine time of day with more granular awareness
    current_time = datetime.now()
    current_hour = current_time.hour
    current_minute = current_time.minute
    day_of_week = current_time.strftime("%A")
    
    # Enhanced time period detection
    if 5 <= current_hour < 12:
        time_period = "🕕 Morning"
        time_emoji = "🌅"
        time_context = "Start your day with intention"
    elif 12 <= current_hour < 18:
        time_period = "🕒 Afternoon"
        time_emoji = "☀️"
        time_context = "Midday energy and focus check"
    else:
        time_period = "🌙 Evening"
        time_emoji = "🌆"
        time_context = "Reflect on your day's progress"
    
    # Check if user has already checked in today
    today_checkins = [
        checkin for checkin in checkin_data 
        if datetime.fromisoformat(checkin['timestamp']).date() == current_time.date()
    ]
    
    # Get previous check-in context
    previous_checkin = None
    if today_checkins:
        today_checkins.sort(key=lambda x: x['timestamp'], reverse=True)
        previous_checkin = today_checkins[0]
    
    # Display enhanced header with context
    st.write(f"{time_emoji} **{time_period} Check-in**")
    st.write(f"**{day_of_week}** • {current_time.strftime('%B %d, %Y')} • {current_time.strftime('%I:%M %p')}")
    st.write(f"*{time_context}*")
    
    # Show goal reminder
    st.write(f"🎯 **Your goal:** {user_profile.get('goal', 'Improve focus and productivity')}")
    
    # Show previous check-in context if available
    if previous_checkin:
        st.info(f"📝 **Previous check-in today:** {previous_checkin['time_period'].title()} at {datetime.fromisoformat(previous_checkin['timestamp']).strftime('%I:%M %p')}")
    
    # Time-aware encouragement
    encouragement = assistant.get_daily_encouragement()
    st.success(encouragement)
    
    # Simple form without progress tracking
    

    
    with st.form("daily_checkin_form"):
        # Step 1: Basic Info
        st.subheader("📝 Step 1: Choose Your Check-in Mode")
        
        checkin_mode = st.radio(
            "What would you like to do?",
            ["📝 Just log my feelings", "🎯 Get help planning my day"],
            help="Select 'Just log' for quick mood tracking, or 'Get help' for smart task planning"
        )
        
        # User selected check-in mode
        
        # Morning flow (5 AM - 12 PM)
        if 5 <= current_hour < 12:
            # Get yesterday's evening check-in for context
            yesterday_evening = None
            if checkin_data:
                yesterday = current_time.date() - timedelta(days=1)
                yesterday_checkins = [
                    checkin for checkin in checkin_data
                    if datetime.fromisoformat(checkin['timestamp']).date() == yesterday
                    and checkin['time_period'] == 'evening'
                ]
                if yesterday_checkins:
                    yesterday_evening = yesterday_checkins[0]
            
            # Show yesterday's context if available
            if yesterday_evening:
                st.info(f"📝 **Yesterday's evening:** You felt {yesterday_evening.get('current_feeling', 'N/A')} and accomplished: {yesterday_evening.get('accomplishments', 'N/A')[:50]}...")
            
            # Step 2: Goals & Energy
            st.subheader("🎯 Step 2: Goals & Energy")
            
            # Time-aware sleep question
            if current_hour < 8:
                sleep_context = "How did you sleep last night?"
            else:
                sleep_context = "How did you sleep?"
            
            sleep_quality = st.selectbox(
                f"😴 {sleep_context}",
                ["Excellent", "Good", "Okay", "Poor", "Terrible"]
            )
            
                    # User answered sleep question
            
            # Suggest focus based on previous patterns
            focus_suggestion = ""
            if previous_checkin and previous_checkin.get('focus_today'):
                focus_suggestion = f"Previous focus: {previous_checkin['focus_today']}"
            
            focus_today = st.text_area(
                "🎯 What do you want to focus on today?",
                placeholder="e.g., Complete project proposal, Exercise for 30 minutes, Read 20 pages",
                help=focus_suggestion if focus_suggestion else "Be specific about what you want to accomplish"
            )
            
            # Time-aware energy question
            if current_hour < 7:
                energy_context = "How's your morning energy?"
            elif current_hour < 10:
                energy_context = "How's your energy now?"
            else:
                energy_context = "What's your energy like?"
            
            energy_level = st.selectbox(
                f"🔋 {energy_context}",
                ["High", "Good", "Moderate", "Low", "Very low"]
            )
            
                    # User answered energy question
            
            # Morning wellness reminder
            if energy_level in ["Low", "Very low"]:
                st.warning("💡 **Tip:** Consider a short walk, stretching, or a healthy breakfast to boost your energy!")
            
            # Step 3: Additional Context
            st.subheader("💭 Step 3: Additional Context")
            
            # Current feeling
            current_feeling = st.selectbox(
                "😊 How are you feeling right now?",
                ["Excited", "Good", "Okay", "Tired", "Stressed", "Focused"]
            )
            
            # Optional notes field
            additional_notes = st.text_area(
                "📝 Any additional thoughts? (Optional)",
                placeholder="e.g., Feeling excited about today, Need to remember to call mom, Weather is affecting my mood",
                help="Share any context that might help with your check-in"
            )
            
            submitted = st.form_submit_button("💾 Save Morning Check-in")
            
            if submitted:
                checkin_data = {
                    "timestamp": datetime.now().isoformat(),
                    "time_period": "morning",
                    "sleep_quality": sleep_quality,
                    "focus_today": focus_today,
                    "energy_level": energy_level,
                    "current_feeling": current_feeling,
                    "additional_notes": additional_notes,
                    "day_of_week": day_of_week,
                    "checkin_hour": current_hour
                }
                # Save the check-in data to persistent storage
                save_checkin_data(checkin_data)
                st.success("✅ Morning check-in saved successfully!")
                
                # Completion celebration
                st.success("🎉 **Check-in Complete!** You've successfully completed your morning check-in!")
                
                # Show completion summary
                st.write("---")
                st.subheader("📋 Check-in Summary")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Time Period:** {time_period}")
                    st.write(f"**Sleep Quality:** {sleep_quality}")
                    st.write(f"**Energy Level:** {energy_level}")
                with col2:
                    st.write(f"**Focus Today:** {focus_today[:50]}{'...' if len(focus_today) > 50 else ''}")
                    if additional_notes:
                        st.write(f"**Notes:** {additional_notes[:50]}{'...' if len(additional_notes) > 50 else ''}")
                
                # Feedback prompt after successful check-in
                st.write("---")
                st.info("💬 **How was this check-in experience?**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("👍 Great!", key="feedback_good_morning"):
                        st.success("Thanks! We're glad it's working well for you! 🙏")
                with col2:
                    if st.button("🤔 Could be better", key="feedback_ok_morning"):
                        st.info("We'd love to hear your suggestions! [📝 Feedback Form](https://tally.so/r/mBr11Q)")
                with col3:
                    if st.button("📝 Share detailed feedback", key="feedback_detailed_morning"):
                        st.markdown("**[📋 Open Feedback Form](https://tally.so/r/mBr11Q)**")
                
                # Generate smart task plan if user requested help
                if checkin_mode == "🎯 Get help planning my day":
                    st.subheader("🎯 Your Smart Task Plan")
                    
                    # Prepare current check-in data for AI
                    current_checkin_data = {
                        'time_period': 'morning',
                        'sleep_quality': sleep_quality,
                        'energy_level': energy_level,
                        'focus_today': focus_today,
                        'current_feeling': current_feeling,
                        'day_progress': 'Not applicable for morning'
                    }
                    
                    # Generate AI-powered task plan
                    if ai_service_available and ai_service:
                        task_plan = ai_service.generate_ai_task_plan(user_profile, current_checkin_data, mood_data, user_email)
                        
                        # Fallback to rule-based plan if AI fails
                        if not task_plan:
                            st.info("🤖 AI task planning unavailable, using smart fallback system...")
                            task_plan = assistant.generate_smart_task_plan(checkin_data, focus_today)
                        else:
                            st.success("🤖 AI-powered personalized plan generated!")
                    else:
                        st.info("🤖 AI service not available, using smart fallback system...")
                        task_plan = assistant.generate_smart_task_plan(checkin_data, focus_today)
                    
                    # Display tasks
                    st.write("**📋 Recommended Tasks:**")
                    for i, task in enumerate(task_plan['tasks'], 1):
                        st.write(f"{i}. {task}")
                    
                    # Display recommendations
                    if task_plan['recommendations']:
                        st.write("**💡 Smart Recommendations:**")
                        for rec in task_plan['recommendations']:
                            st.info(rec)
                    
                    # Display estimated duration
                    st.write(f"**⏰ Estimated Duration:** {task_plan['estimated_duration']}")
                    
                    # Add task completion tracking
                    st.write("**✅ Task Completion:**")
                    task_completion = {}
                    for task in task_plan['tasks']:
                        task_completion[task] = st.checkbox(f"Complete: {task}")
                    
                    # Save task plan to user data
                    checkin_data['task_plan'] = task_plan
                    checkin_data['task_completion'] = task_completion
                    save_checkin_data(checkin_data)
        
        # Afternoon flow (12 PM - 6 PM)
        elif 12 <= current_hour < 18:
            # Get morning check-in for context
            morning_checkin = None
            if today_checkins:
                morning_checkins = [
                    checkin for checkin in today_checkins
                    if checkin['time_period'] == 'morning'
                ]
                if morning_checkins:
                    morning_checkin = morning_checkins[0]
            
            # Show morning context if available
            if morning_checkin:
                st.info(f"📝 **This morning:** You planned to focus on: {morning_checkin.get('focus_today', 'N/A')} and your energy was {morning_checkin.get('energy_level', 'N/A')}")
            
            # Step 2: Goals & Energy
            st.subheader("🎯 Step 2: Goals & Energy")
            
            # Energy level for afternoon
            energy_level = st.selectbox(
                "🔋 How's your energy now?",
                ["High", "Good", "Moderate", "Low", "Very low"]
            )
            
            # Focus today (what they're focusing on)
            focus_today = st.text_area(
                "🎯 What are you focusing on today?",
                placeholder="e.g., Work project, Exercise, Reading, Social activities",
                help="What's your main focus or priority today?"
            )
            
            # Current feeling
            current_feeling = st.selectbox(
                "😊 How are you feeling right now?",
                ["Motivated", "Good", "Okay", "Tired", "Stressed"]
            )
            
            # Time-aware progress question
            if current_hour < 14:
                progress_context = "How's your morning progress?"
            elif current_hour < 16:
                progress_context = "How's the day going so far?"
            else:
                progress_context = "How's your afternoon going?"
            
            day_progress = st.selectbox(
                f"📊 {progress_context}",
                ["Great", "Good", "Okay", "Challenging", "Difficult"]
            )
            
                    # User answered progress question
            
            # Suggest plan adjustments based on progress
            if day_progress in ["Challenging", "Difficult"]:
                st.warning("💡 **Tip:** Consider breaking down your tasks into smaller, more manageable steps!")
            
            adjust_plan = st.text_area(
                "🔄 Want to adjust your plan? (Optional)",
                placeholder="e.g., Move difficult tasks to tomorrow, Take a longer break, Focus on one priority",
                help="What would help you feel more productive?"
            )
            
            # Time-aware break suggestion
            if current_hour >= 15:
                break_context = "☕ Take a break? (It's getting late in the day)"
            else:
                break_context = "☕ Take a break?"
            
            take_break = st.radio(
                break_context,
                ["Yes, I need a break", "No, I'm in the zone", "Maybe later"]
            )
            
            # User answered break question
            
            # Break encouragement
            if take_break == "Yes, I need a break":
                st.info("💡 **Great choice!** Taking breaks helps maintain focus and prevents burnout.")
            elif take_break == "No, I'm in the zone":
                st.success("🚀 **Flow state!** Enjoy your productive momentum!")
            
            # Step 3: Additional Context
            st.subheader("💭 Step 3: Additional Context")
            
            # Optional notes field
            additional_notes = st.text_area(
                "📝 Any additional thoughts? (Optional)",
                placeholder="e.g., Need to adjust my schedule, Feeling more focused now, Should take a walk",
                help="Share any context that might help with your check-in"
            )
            
            submitted = st.form_submit_button("💾 Save Afternoon Check-in")
            
            if submitted:
                checkin_data = {
                    "timestamp": datetime.now().isoformat(),
                    "time_period": "afternoon",
                    "energy_level": energy_level,
                    "focus_today": focus_today,
                    "current_feeling": current_feeling,
                    "day_progress": day_progress,
                    "adjust_plan": adjust_plan,
                    "take_break": take_break,
                    "additional_notes": additional_notes,
                    "day_of_week": day_of_week,
                    "checkin_hour": current_hour
                }
                # Save the check-in data to persistent storage
                save_checkin_data(checkin_data)
                st.success("✅ Afternoon check-in saved successfully!")
                
                # Completion celebration
                st.success("🎉 **Check-in Complete!** You've successfully completed your afternoon check-in!")
                
                # Show completion summary
                st.write("---")
                st.subheader("📋 Check-in Summary")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Time Period:** {time_period}")
                    st.write(f"**Day Progress:** {day_progress}")
                    st.write(f"**Break Decision:** {take_break}")
                with col2:
                    if adjust_plan:
                        st.write(f"**Plan Adjustment:** {adjust_plan[:50]}{'...' if len(adjust_plan) > 50 else ''}")
                    if additional_notes:
                        st.write(f"**Notes:** {additional_notes[:50]}{'...' if len(additional_notes) > 50 else ''}")
                
                # Generate smart task plan if user requested help
                if checkin_mode == "🎯 Get help planning my day":
                    st.subheader("🎯 Your Smart Afternoon Plan")
                    
                    # Prepare current check-in data for AI
                    current_checkin_data = {
                        'time_period': 'afternoon',
                        'sleep_quality': 'Not applicable for afternoon',
                        'energy_level': energy_level,
                        'focus_today': focus_today,
                        'current_feeling': current_feeling,
                        'day_progress': day_progress
                    }
                    
                    # Generate AI-powered task plan
                    if ai_service_available and ai_service:
                        task_plan = ai_service.generate_ai_task_plan(user_profile, current_checkin_data, mood_data, user_email)
                        
                        # Fallback to rule-based plan if AI fails
                        if not task_plan:
                            st.info("🤖 AI task planning unavailable, using smart fallback system...")
                            task_plan = assistant.generate_smart_task_plan(checkin_data)
                        else:
                            st.success("🤖 AI-powered personalized plan generated!")
                    else:
                        st.info("🤖 AI service not available, using smart fallback system...")
                        task_plan = assistant.generate_smart_task_plan(checkin_data)
                    
                    # Display tasks
                    st.write("**📋 Recommended Tasks:**")
                    for i, task in enumerate(task_plan['tasks'], 1):
                        st.write(f"{i}. {task}")
                    
                    # Display recommendations
                    if task_plan['recommendations']:
                        st.write("**💡 Smart Recommendations:**")
                        for rec in task_plan['recommendations']:
                            st.info(rec)
                    
                    # Display estimated duration
                    st.write(f"**⏰ Estimated Duration:** {task_plan['estimated_duration']}")
                    
                    # Add task completion tracking
                    st.write("**✅ Task Completion:**")
                    task_completion = {}
                    for task in task_plan['tasks']:
                        task_completion[task] = st.checkbox(f"Complete: {task}")
                    
                    # Save task plan to user data
                    checkin_data['task_plan'] = task_plan
                    checkin_data['task_completion'] = task_completion
                    save_checkin_data(checkin_data)
        
        # Evening flow (6 PM - 5 AM)
        else:
            # Get today's previous check-ins for context
            morning_checkin = None
            afternoon_checkin = None
            
            if today_checkins:
                for checkin in today_checkins:
                    if checkin['time_period'] == 'morning':
                        morning_checkin = checkin
                    elif checkin['time_period'] == 'afternoon':
                        afternoon_checkin = checkin
            
            # Show today's journey
            if morning_checkin or afternoon_checkin:
                journey_summary = "📝 **Today's journey:** "
                if morning_checkin:
                    journey_summary += f"Started with focus on '{morning_checkin.get('focus_today', 'N/A')}' "
                if afternoon_checkin:
                    journey_summary += f"• Afternoon was {afternoon_checkin.get('day_progress', 'N/A')}"
                st.info(journey_summary)
            
            # Step 2: Goals & Energy
            st.subheader("🎯 Step 2: Goals & Energy")
            
            # Energy level for evening
            energy_level = st.selectbox(
                "🔋 How's your energy now?",
                ["High", "Good", "Moderate", "Low", "Very low"]
            )
            
            # Focus today (what they focused on)
            focus_today = st.text_area(
                "🎯 What did you focus on today?",
                placeholder="e.g., Work project, Exercise, Reading, Social activities",
                help="What was your main focus or priority today?"
            )
            
            # Time-aware accomplishment question
            if current_hour < 20:
                accomplishment_context = "What did you accomplish today?"
            else:
                accomplishment_context = "What did you accomplish today? (It's getting late)"
            
            accomplishments = st.text_area(
                f"🏆 {accomplishment_context}",
                placeholder="e.g., Completed project proposal, Exercised for 30 minutes, Read 20 pages",
                help="Celebrate your wins, no matter how small!"
            )
            
            # User entered accomplishments
            
            challenges = st.text_area(
                "🚧 Any challenges? (Optional)",
                placeholder="e.g., Had trouble focusing, Felt overwhelmed, Technical difficulties",
                help="Understanding challenges helps improve future days"
            )
            
            # Time-aware feeling question
            if current_hour < 22:
                feeling_context = "How do you feel now?"
            else:
                feeling_context = "How do you feel now? (Getting ready for bed)"
            
            current_feeling = st.selectbox(
                f"😊 {feeling_context}",
                ["Accomplished", "Good", "Okay", "Tired", "Stressed"]
            )
            
            # User answered feeling question
            
            # Evening wellness tips
            if current_feeling in ["Tired", "Stressed"]:
                st.warning("💡 **Evening tip:** Consider a relaxing activity like reading, meditation, or gentle stretching to wind down.")
            elif current_feeling == "Accomplished":
                st.success("🎉 **Great job today!** You should be proud of your accomplishments!")
            
            # Step 3: Additional Context
            st.subheader("💭 Step 3: Additional Context")
            
            # Tomorrow preparation
            if current_hour < 22:
                tomorrow_focus = st.text_area(
                    "🌙 What would you like to focus on tomorrow? (Optional)",
                    placeholder="e.g., Continue with the project, Exercise in the morning, Call a friend",
                    help="Planning ahead can help you start tomorrow with intention"
                )
            else:
                tomorrow_focus = st.text_area(
                    "🌙 Any thoughts for tomorrow? (Optional)",
                    placeholder="e.g., Need to remember to..., Looking forward to..., Should prepare for...",
                    help="Capture any thoughts before bed"
                )
            
            submitted = st.form_submit_button("💾 Save Evening Check-in")
            
            if submitted:
                checkin_data = {
                    "timestamp": datetime.now().isoformat(),
                    "time_period": "evening",
                    "energy_level": energy_level,
                    "focus_today": focus_today,
                    "accomplishments": accomplishments,
                    "challenges": challenges,
                    "current_feeling": current_feeling,
                    "tomorrow_focus": tomorrow_focus,
                    "day_of_week": day_of_week,
                    "checkin_hour": current_hour
                }
                # Save the check-in data to persistent storage
                save_checkin_data(checkin_data)
                st.success("✅ Evening check-in saved successfully!")
                
                # Completion celebration
                st.success("🎉 **Check-in Complete!** You've successfully completed your evening check-in!")
                
                # Show completion summary
                st.write("---")
                st.subheader("📋 Check-in Summary")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Time Period:** {time_period}")
                    st.write(f"**Current Feeling:** {current_feeling}")
                    st.write(f"**Accomplishments:** {accomplishments[:50]}{'...' if len(accomplishments) > 50 else ''}")
                with col2:
                    if challenges:
                        st.write(f"**Challenges:** {challenges[:50]}{'...' if len(challenges) > 50 else ''}")
                    if tomorrow_focus:
                        st.write(f"**Tomorrow's Focus:** {tomorrow_focus[:50]}{'...' if len(tomorrow_focus) > 50 else ''}")
                
                # Generate smart task plan if user requested help
                if checkin_mode == "🎯 Get help planning my day":
                    st.subheader("🌙 Your Smart Evening Plan")
                    
                    # Prepare current check-in data for AI
                    current_checkin_data = {
                        'time_period': 'evening',
                        'sleep_quality': 'Not applicable for evening',
                        'energy_level': energy_level,
                        'focus_today': focus_today,
                        'current_feeling': current_feeling,
                        'day_progress': 'Not applicable for evening'
                    }
                    
                    # Generate AI-powered task plan
                    if ai_service_available and ai_service:
                        task_plan = ai_service.generate_ai_task_plan(user_profile, current_checkin_data, mood_data, user_email)
                        
                        # Fallback to rule-based plan if AI fails
                        if not task_plan:
                            st.info("🤖 AI task planning unavailable, using smart fallback system...")
                            task_plan = assistant.generate_smart_task_plan(checkin_data)
                        else:
                            st.success("🤖 AI-powered personalized plan generated!")
                    else:
                        st.info("🤖 AI service not available, using smart fallback system...")
                        task_plan = assistant.generate_smart_task_plan(checkin_data)
                    
                    # Display tasks
                    st.write("**📋 Recommended Tasks:**")
                    for i, task in enumerate(task_plan['tasks'], 1):
                        st.write(f"{i}. {task}")
                    
                    # Display recommendations
                    if task_plan['recommendations']:
                        st.write("**💡 Smart Recommendations:**")
                        for rec in task_plan['recommendations']:
                            st.info(rec)
                    
                    # Display estimated duration
                    st.write(f"**⏰ Estimated Duration:** {task_plan['estimated_duration']}")
                    
                    # Add task completion tracking
                    st.write("**✅ Task Completion:**")
                    task_completion = {}
                    for task in task_plan['tasks']:
                        task_completion[task] = st.checkbox(f"Complete: {task}")
                    
                    # Save task plan to user data
                    checkin_data['task_plan'] = task_plan
                    checkin_data['task_completion'] = task_completion
                    save_checkin_data(checkin_data)
