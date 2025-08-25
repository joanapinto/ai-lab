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

st.set_page_config(page_title="Focus Companion - History", page_icon="📊")
st.title("📊 Your History")

# Load user profile
user_profile = load_user_profile()

if not user_profile:
    st.warning("Please complete onboarding first!")
    if st.button("🚀 Go to Onboarding", use_container_width=True):
        st.switch_page("pages/onboarding.py")
else:
    st.write("View your progress and history over time.")
    
    # Display user profile
    st.subheader("👤 Your Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Goal:** {user_profile.get('goal', 'Not set')}")
        st.write(f"**Availability:** {user_profile.get('availability', 'Not set')}")
        st.write(f"**Energy Level:** {user_profile.get('energy', 'Not set')}")
    
    with col2:
        st.write(f"**Check-ins:** {user_profile.get('check_ins', 'Not set')}")
        st.write(f"**Tone Preference:** {user_profile.get('tone', 'Not set')}")
        st.write(f"**Situation:** {user_profile.get('situation', 'Not set')}")
    
    st.info("📈 Check-in and reflection history will be displayed here as you use the app more.")
