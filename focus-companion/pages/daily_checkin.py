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
from auth import require_beta_access

st.set_page_config(page_title="Focus Companion - Daily Check-in", page_icon="📝")

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
    
    # Initialize progress tracking in session state
    if 'checkin_progress' not in st.session_state:
        st.session_state.checkin_progress = 0
    if 'checkin_steps_completed' not in st.session_state:
        st.session_state.checkin_steps_completed = {
            'basic_info': False,
            'goals_energy': False,
            'feelings_progress': False,
            'complete': False
        }
    
    # Progress tracking
    st.write("---")
    st.subheader("📊 Check-in Progress")
    
    # Reset progress button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Reset Progress", help="Start over with a fresh check-in"):
            st.session_state.checkin_steps_completed = {
                'basic_info': False,
                'goals_energy': False,
                'feelings_progress': False,
                'complete': False
            }
            st.rerun()
    
    # Calculate progress based on completed steps
    completed_steps = sum(st.session_state.checkin_steps_completed.values())
    total_steps = len(st.session_state.checkin_steps_completed)
    progress_percentage = (completed_steps / total_steps) * 100
    
    # Overall progress bar
    progress_col1, progress_col2 = st.columns([3, 1])
    with progress_col1:
        progress_text = "Ready to start your check-in"
        if progress_percentage > 0:
            progress_text = f"Step {completed_steps} of {total_steps} completed"
        if progress_percentage == 100:
            progress_text = "Check-in complete! 🎉"
        
        st.progress(progress_percentage / 100, text=progress_text)
    with progress_col2:
        st.metric("Progress", f"{int(progress_percentage)}%")
    
    # Progress indicators for different sections
    col1, col2, col3, col4 = st.columns(4)
    
    # Step 1: Basic Info
    with col1:
        if st.session_state.checkin_steps_completed['basic_info']:
            st.success("✅ **Step 1:** Basic Info")
            st.progress(1.0, text="Completed")
        else:
            st.info("📝 **Step 1:** Basic Info")
            st.progress(0.0, text="Pending")
    
    # Step 2: Goals & Energy
    with col2:
        if st.session_state.checkin_steps_completed['goals_energy']:
            st.success("✅ **Step 2:** Goals & Energy")
            st.progress(1.0, text="Completed")
        else:
            st.info("🎯 **Step 2:** Goals & Energy")
            st.progress(0.0, text="Pending")
    
    # Step 3: Feelings & Progress
    with col3:
        if st.session_state.checkin_steps_completed['feelings_progress']:
            st.success("✅ **Step 3:** Feelings & Progress")
            st.progress(1.0, text="Completed")
        else:
            st.info("💭 **Step 3:** Feelings & Progress")
            st.progress(0.0, text="Pending")
    
    # Step 4: Complete
    with col4:
        if st.session_state.checkin_steps_completed['complete']:
            st.success("✅ **Step 4:** Complete")
            st.progress(1.0, text="Completed")
        else:
            st.info("✅ **Step 4:** Complete")
            st.progress(0.0, text="Pending")
    
    with st.form("daily_checkin_form"):
        # Step 1: Basic Info
        st.subheader("📝 Step 1: Choose Your Check-in Mode")
        
        checkin_mode = st.radio(
            "What would you like to do?",
            ["📝 Just log my feelings", "🎯 Get help planning my day"],
            help="Select 'Just log' for quick mood tracking, or 'Get help' for smart task planning"
        )
        
        # Update progress when user selects mode
        if checkin_mode:
            st.session_state.checkin_steps_completed['basic_info'] = True
        
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
            
            # Update progress when user answers sleep question
            if sleep_quality:
                st.session_state.checkin_steps_completed['goals_energy'] = True
            
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
            
            # Update progress when user answers energy question
            if energy_level:
                st.session_state.checkin_steps_completed['feelings_progress'] = True
            
            # Morning wellness reminder
            if energy_level in ["Low", "Very low"]:
                st.warning("💡 **Tip:** Consider a short walk, stretching, or a healthy breakfast to boost your energy!")
            
            # Step 3: Additional Context
            st.subheader("💭 Step 3: Additional Context")
            
            # Optional notes field
            additional_notes = st.text_area(
                "📝 Any additional thoughts? (Optional)",
                placeholder="e.g., Feeling excited about today, Need to remember to call mom, Weather is affecting my mood",
                help="Share any context that might help with your check-in"
            )
            
            submitted = st.form_submit_button("💾 Save Morning Check-in")
            
            if submitted:
                # Mark check-in as complete
                st.session_state.checkin_steps_completed['complete'] = True
                
                checkin_data = {
                    "timestamp": datetime.now().isoformat(),
                    "time_period": "morning",
                    "sleep_quality": sleep_quality,
                    "focus_today": focus_today,
                    "energy_level": energy_level,
                    "additional_notes": additional_notes,
                    "day_of_week": day_of_week,
                    "checkin_hour": current_hour
                }
                # Save the check-in data to persistent storage
                save_checkin_data(checkin_data)
                st.success("✅ Morning check-in saved successfully!")
                
                # Completion celebration
                if st.session_state.checkin_steps_completed['complete']:
                    st.balloons()
                    st.success("🎉 **Check-in Complete!** You've successfully completed all steps!")
                    
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
                    
                    # Generate task plan using assistant
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
                
                st.balloons()
        
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
            
            # Update progress when user answers progress question
            if day_progress:
                st.session_state.checkin_steps_completed['goals_energy'] = True
            
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
            
            # Update progress when user answers break question
            if take_break:
                st.session_state.checkin_steps_completed['feelings_progress'] = True
            
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
                # Mark check-in as complete
                st.session_state.checkin_steps_completed['complete'] = True
                
                checkin_data = {
                    "timestamp": datetime.now().isoformat(),
                    "time_period": "afternoon",
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
                if st.session_state.checkin_steps_completed['complete']:
                    st.balloons()
                    st.success("🎉 **Check-in Complete!** You've successfully completed all steps!")
                    
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
                    
                    # Generate task plan using assistant
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
                
                st.balloons()
        
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
            
            # Update progress when user enters accomplishments
            if accomplishments:
                st.session_state.checkin_steps_completed['goals_energy'] = True
            
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
            
            # Update progress when user answers feeling question
            if current_feeling:
                st.session_state.checkin_steps_completed['feelings_progress'] = True
            
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
                # Mark check-in as complete
                st.session_state.checkin_steps_completed['complete'] = True
                
                checkin_data = {
                    "timestamp": datetime.now().isoformat(),
                    "time_period": "evening",
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
                if st.session_state.checkin_steps_completed['complete']:
                    st.balloons()
                    st.success("🎉 **Check-in Complete!** You've successfully completed all steps!")
                    
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
                    
                    # Generate task plan using assistant
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
                
                st.balloons()
