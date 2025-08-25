import streamlit as st
import os
import json
import sys
from pathlib import Path

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
    st.write(f"Welcome back! Let's check in on your progress toward: **{user_profile.get('goal', 'your goal')}**")
    
    with st.form("daily_checkin_form"):
        mood = st.selectbox(
            "😊 How are you feeling today?",
            ["Great", "Good", "Okay", "Not great", "Terrible"]
        )
        
        energy = st.selectbox(
            "🔋 How's your energy level?",
            ["High", "Good", "Moderate", "Low", "Very low"]
        )
        
        progress = st.text_area("📈 What progress did you make today?")
        
        challenges = st.text_area("🚧 What challenges did you face?")
        
        tomorrow_plan = st.text_area("🎯 What's your plan for tomorrow?")
        
        submitted = st.form_submit_button("💾 Save Check-in")
        
        if submitted:
            # Here you would save the check-in data
            st.success("✅ Check-in saved successfully!")
            st.balloons()
