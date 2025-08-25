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

st.set_page_config(page_title="Focus Companion - Reflection", page_icon="🤔")
st.title("🤔 Weekly Reflection")

# Load user profile
user_profile = load_user_profile()

if not user_profile:
    st.warning("Please complete onboarding first!")
    if st.button("🚀 Go to Onboarding", use_container_width=True):
        st.switch_page("pages/onboarding.py")
else:
    st.write("Take some time to reflect on your week and progress toward your goals.")
    
    with st.form("reflection_form"):
        wins = st.text_area("🏆 What were your biggest wins this week?")
        
        challenges = st.text_area("🚧 What challenges did you face?")
        
        lessons = st.text_area("📚 What did you learn?")
        
        next_week = st.text_area("🎯 What do you want to focus on next week?")
        
        submitted = st.form_submit_button("💾 Save Reflection")
        
        if submitted:
            st.success("✅ Reflection saved successfully!")
            st.balloons()
