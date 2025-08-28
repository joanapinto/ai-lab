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

# Prefill or fallback values
goal = existing_profile.get("goal", "")
joy_sources = existing_profile.get("joy_sources", [])
joy_other = existing_profile.get("joy_other", "")
energy_drainers = existing_profile.get("energy_drainers", [])
energy_drainer_other = existing_profile.get("energy_drainer_other", "")
therapy_coaching = existing_profile.get("therapy_coaching", "No")

# Handle availability value conversion for backward compatibility
old_availability = existing_profile.get("availability", "1–2 hours")
availability_options = ["< 1 hour", "1–2 hours", "2–4 hours", "4+ hours"]
if old_availability == "2-4 hours":  # Convert old format to new format
    availability = "2–4 hours"
elif old_availability in availability_options:
    availability = old_availability
else:
    availability = "1–2 hours"

energy = existing_profile.get("energy", "Okay")
emotional_patterns = existing_profile.get("emotional_patterns", "Not sure yet")
small_habit = existing_profile.get("small_habit", "")
reminders = existing_profile.get("reminders", "Yes")
tone = existing_profile.get("tone", "Gentle & Supportive")
situation = existing_profile.get("situation", "Freelancer")
situation_other = existing_profile.get("situation_other", "")

if is_returning_user:
    st.success("👋 Welcome back! You can update your profile or reset it below.")
else:
    st.info("👋 First time here? Let's get to know you better!")

st.subheader("🎯 Let's understand your needs")

# Question 1: Main area of support
goal = st.text_area(
    "🎯 What's one area of your life you'd like more support with right now?",
    value=goal,
    placeholder="e.g., staying focused, managing emotions, building routines…",
    help="This helps us tailor your experience"
)

st.subheader("❤️ Understanding what energizes you")

# Question 2: Joy sources
joy_options = ["Friends", "Movement", "Creating", "Helping others", "Nature", "Rest", "Learning", "Other"]
joy_sources = st.multiselect(
    "❤️ What brings you joy or gives you energy lately?",
    options=joy_options,
    default=joy_sources
)

# Conditional "Other" specification for joy sources
if "Other" in joy_sources:
    st.info("💬 Tell us more about what brings you joy!")
    joy_other = st.text_area(
        "Do you want to specify what?",
        value=joy_other,
        placeholder="Write what brings you joy…"
    )

st.subheader("🌧️ Understanding what drains you")

# Question 3: Energy drainers
drainer_options = ["Overwhelm", "Lack of sleep", "Isolation", "Criticism", "Deadlines", "Other"]
energy_drainers = st.multiselect(
    "🌧️ What tends to bring you down or drain your energy?",
    options=drainer_options,
    default=energy_drainers
)

# Conditional "Other" specification for energy drainers
if "Other" in energy_drainers:
    st.info("💬 Tell us more about what drains your energy!")
    energy_drainer_other = st.text_area(
        "Do you want to specify what?",
        value=energy_drainer_other,
        placeholder="Write what brings you down or drains your energy…"
    )

st.subheader("💬 Professional support")

# Question 4: Therapy/coaching
therapy_coaching = st.selectbox(
    "💬 Are you currently working with a therapist, coach, or mentor?",
    options=["No", "Yes", "I'd like to find one"],
    index=["No", "Yes", "I'd like to find one"].index(therapy_coaching)
)

st.subheader("⏱️ Time and energy assessment")

# Question 5: Time availability
availability = st.selectbox(
    "⏱️ On most weekdays, how much time do you feel you can dedicate to yourself or your goals?",
    options=["< 1 hour", "1–2 hours", "2–4 hours", "4+ hours"],
    index=["< 1 hour", "1–2 hours", "2–4 hours", "4+ hours"].index(availability)
)

# Question 6: Current energy levels
energy = st.selectbox(
    "🔋 How would you describe your current energy levels?",
    options=["Very low", "Low", "Okay", "Good", "High"],
    index=["Very low", "Low", "Okay", "Good", "High"].index(energy)
)

# Conditional questions for low energy
if energy in ["Low", "Very low"]:
    st.info("💡 Since your energy is low, let's see how we can help!")
    
    # Question 6.1: Emotional patterns help
    emotional_patterns = st.selectbox(
        "🧠 Do you want help understanding emotional patterns over time?",
        options=["Yes", "No", "Not sure yet"],
        index=["Yes", "No", "Not sure yet"].index(emotional_patterns)
    )
    
    # Question 6.2: Small habit building
    small_habit = st.text_area(
        "🌱 What's one small habit you'd love to build right now?",
        value=small_habit,
        placeholder="e.g., journaling, moving more, taking breaks…"
    )

st.subheader("🔔 Assistant preferences")

# Question 7: Reminders
reminders = st.selectbox(
    "🔔 Would you like gentle reminders or check-in nudges from your assistant?",
    options=["Yes", "No"],
    index=["Yes", "No"].index(reminders)
)

# Question 8: Communication tone
tone = st.selectbox(
    "🗣️ How would you like your assistant to speak to you?",
    options=["Direct & Motivating", "Gentle & Supportive", "Neutral & Balanced"],
    index=["Direct & Motivating", "Gentle & Supportive", "Neutral & Balanced"].index(tone)
)

st.subheader("💼 Your situation")

# Question 9: Current situation
situation = st.selectbox(
    "💼 Which of these best describes your current situation?",
    options=["Freelancer", "New parent", "PhD student", "Full-time job", "Unemployed", "Other"],
    index=["Freelancer", "New parent", "PhD student", "Full-time job", "Unemployed", "Other"].index(situation)
)

# Conditional "Other" specification for situation
if situation == "Other":
    st.info("💬 Tell us more about your situation!")
    situation_other = st.text_area(
        "Do you want to specify what?",
        value=situation_other,
        placeholder="Describe your current situation in a few words…"
    )

# Save button
submitted = st.button("💾 Save & Continue", type="primary", use_container_width=True)

if submitted:
    user_profile = {
        "goal": goal,
        "joy_sources": joy_sources,
        "joy_other": joy_other if "Other" in joy_sources else "",
        "energy_drainers": energy_drainers,
        "energy_drainer_other": energy_drainer_other if "Other" in energy_drainers else "",
        "therapy_coaching": therapy_coaching,
        "availability": availability,
        "energy": energy,
        "emotional_patterns": emotional_patterns if energy in ["Low", "Very low"] else "Not applicable",
        "small_habit": small_habit if energy in ["Low", "Very low"] else "",
        "reminders": reminders,
        "tone": tone,
        "situation": situation,
        "situation_other": situation_other if situation == "Other" else ""
    }

    save_user_profile(user_profile)
    st.success("✅ Profile saved successfully!")
    st.balloons()
    st.switch_page("pages/daily_checkin.py")

# 🚨 Reset Button with Confirmation
st.markdown("---")
st.subheader("⚠️ Reset your profile")

confirm_reset = st.checkbox("I understand this will delete all my saved profile data.")

if confirm_reset:
    if st.button("❌ Reset My Profile"):
        reset_user_profile()
        st.success("✅ Profile reset successfully. Redirecting...")
        st.rerun()
else:
    st.warning("Tick the box above to enable the reset button.")
