import streamlit as st
import os
import json
import sys
from pathlib import Path

# Add the parent directory to the Python path to find the data module
current_file = Path(__file__)
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from data.storage import save_user_profile, load_user_profile, reset_user_profile

st.set_page_config(page_title="Focus Companion - Onboarding", page_icon="🧠")
st.title("🧠 Welcome to Your Focus Companion")

# Load existing profile if available
existing_profile = load_user_profile()
is_returning_user = bool(existing_profile)

if is_returning_user:
    st.success("👋 Welcome back! You can update your profile or reset it below.")
else:
    st.info("👋 First time here? Let’s tailor your assistant!")

# Prefill or fallback values
goal = existing_profile.get("goal", "")
availability = existing_profile.get("availability", "1–2 hours")
energy = existing_profile.get("energy", "Decent")
check_ins = existing_profile.get("check_ins", "Yes")
tone = existing_profile.get("tone", "Gentle & supportive")
situation = existing_profile.get("situation", "Freelancer")

with st.form("onboarding_form"):
    goal = st.text_area("🎯 What’s one area in your life you’d like help managing better?", value=goal)

    availability = st.selectbox(
        "⏱️ On average, how much time do you have available on weekdays?",
        ["< 1 hour", "1–2 hours", "2–4 hours", "4+ hours"],
        index=["< 1 hour", "1–2 hours", "2–4 hours", "4+ hours"].index(availability)
    )

    energy = st.selectbox(
        "🔋 How would you describe your general energy lately?",
        ["Very low", "Low", "Decent", "Good", "High"],
        index=["Very low", "Low", "Decent", "Good", "High"].index(energy)
    )

    check_ins = st.radio(
        "🔔 Do you want to receive nudges or follow-up check-ins?",
        ["Yes", "No"],
        index=["Yes", "No"].index(check_ins)
    )

    tone = st.selectbox(
        "🗣️ What tone do you prefer from your assistant?",
        ["Gentle & supportive", "Direct & motivating", "Neutral"],
        index=["Gentle & supportive", "Direct & motivating", "Neutral"].index(tone)
    )

    situation = st.selectbox(
        "💼 What best describes your current situation?",
        ["New parent", "PhD student", "Freelancer", "Full-time job", "Unemployed", "Other"],
        index=["New parent", "PhD student", "Freelancer", "Full-time job", "Unemployed", "Other"].index(situation)
    )

    submitted = st.form_submit_button("💾 Save & Continue")

if submitted:
    user_profile = {
        "goal": goal,
        "availability": availability,
        "energy": energy,
        "check_ins": check_ins,
        "tone": tone,
        "situation": situation
    }

    save_user_profile(user_profile)
    st.success("✅ Profile saved successfully!")
    st.switch_page("pages/daily_checkin.py")

# 🚨 Reset Button with Confirmation
st.markdown("---")
st.subheader("⚠️ Reset your profile")

confirm_reset = st.checkbox("I understand this will delete all my saved profile data.")

if confirm_reset:
    if st.button("❌ Reset My Profile"):
        reset_user_profile()
        st.success("✅ Profile reset successfully. Redirecting...")
        st.experimental_rerun()
else:
    st.warning("Tick the box above to enable the reset button.")
