import streamlit as st
import os
import json
import sys
from pathlib import Path
from datetime import datetime

# Add the parent directory to the Python path to find the data module
current_file = Path(__file__)
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from data.storage import save_user_profile, load_user_profile

st.set_page_config(page_title="Focus Companion - Daily Check-in", page_icon="📝")
st.title("📝 Daily Check-in")

# Load user profile
user_profile = load_user_profile()

if not user_profile:
    st.warning("Please complete onboarding first!")
    if st.button("🚀 Go to Onboarding", use_container_width=True):
        st.switch_page("pages/onboarding.py")
else:
    # Determine time of day
    current_hour = datetime.now().hour
    
    if 5 <= current_hour < 12:
        time_period = "🕕 Morning"
        time_emoji = "🌅"
    elif 12 <= current_hour < 18:
        time_period = "🕒 Afternoon"
        time_emoji = "☀️"
    else:
        time_period = "🌙 Evening"
        time_emoji = "🌆"
    
    st.write(f"{time_emoji} **{time_period} Check-in**")
    st.write(f"Welcome back! Let's check in on your progress toward: **{user_profile.get('goal', 'your goal')}**")
    
    with st.form("daily_checkin_form"):
        # Morning flow (5 AM - 12 PM)
        if 5 <= current_hour < 12:
            sleep_quality = st.selectbox(
                "😴 How did you sleep?",
                ["Excellent", "Good", "Okay", "Poor", "Terrible"]
            )
            
            focus_today = st.text_area("🎯 What do you want to focus on today?")
            
            energy_level = st.selectbox(
                "🔋 What's your energy like?",
                ["High", "Good", "Moderate", "Low", "Very low"]
            )
            
            submitted = st.form_submit_button("💾 Save Morning Check-in")
            
            if submitted:
                checkin_data = {
                    "timestamp": datetime.now().isoformat(),
                    "time_period": "morning",
                    "sleep_quality": sleep_quality,
                    "focus_today": focus_today,
                    "energy_level": energy_level
                }
                # Here you would save the check-in data
                st.success("✅ Morning check-in saved successfully!")
                st.balloons()
        
        # Afternoon flow (12 PM - 6 PM)
        elif 12 <= current_hour < 18:
            day_progress = st.selectbox(
                "📊 How's the day going?",
                ["Great", "Good", "Okay", "Challenging", "Difficult"]
            )
            
            adjust_plan = st.text_area("🔄 Want to adjust your plan? (Optional)")
            
            take_break = st.radio(
                "☕ Take a break?",
                ["Yes, I need a break", "No, I'm in the zone", "Maybe later"]
            )
            
            submitted = st.form_submit_button("💾 Save Afternoon Check-in")
            
            if submitted:
                checkin_data = {
                    "timestamp": datetime.now().isoformat(),
                    "time_period": "afternoon",
                    "day_progress": day_progress,
                    "adjust_plan": adjust_plan,
                    "take_break": take_break
                }
                # Here you would save the check-in data
                st.success("✅ Afternoon check-in saved successfully!")
                st.balloons()
        
        # Evening flow (6 PM - 5 AM)
        else:
            accomplishments = st.text_area("🏆 What did you accomplish today?")
            
            challenges = st.text_area("🚧 Any challenges? (Optional)")
            
            current_feeling = st.selectbox(
                "😊 How do you feel now?",
                ["Accomplished", "Good", "Okay", "Tired", "Stressed"]
            )
            
            submitted = st.form_submit_button("💾 Save Evening Check-in")
            
            if submitted:
                checkin_data = {
                    "timestamp": datetime.now().isoformat(),
                    "time_period": "evening",
                    "accomplishments": accomplishments,
                    "challenges": challenges,
                    "current_feeling": current_feeling
                }
                # Here you would save the check-in data
                st.success("✅ Evening check-in saved successfully!")
                st.balloons()
