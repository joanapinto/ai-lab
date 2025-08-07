import streamlit as st
import os
import json
from datetime import datetime
from setup import load_user_profile

st.set_page_config(page_title="History", page_icon="📚")

def load_weekly_plans():
    log_path = "logs/weekly_plans.json"
    if not os.path.exists(log_path):
        return []
    try:
        with open(log_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def load_daily_checkins():
    log_path = "logs/daily_checkins.json"
    if not os.path.exists(log_path):
        return []
    try:
        with open(log_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def load_weekly_reflections():
    log_path = "logs/weekly_reflections.json"
    if not os.path.exists(log_path):
        return []
    try:
        with open(log_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def main():
    st.title("📚 History")
    st.markdown("View your past plans, check-ins, and reflections")
    
    # Add a back button
    if st.button("← Back to Dashboard"):
        st.switch_page("main.py")
    
    # Check for user profile
    profile = load_user_profile()
    if not profile:
        st.warning("Please complete setup first.")
        if st.button("Go to Setup"):
            st.switch_page("pages/1_Setup.py")
        return

    # Show main objective at the top
    if "goal" in profile:
        st.markdown(f"**🎯 Main Objective:** {profile['goal']}")

    # Navigation tabs
    tab1, tab2, tab3 = st.tabs(["📋 Weekly Plans", "🌤️ Daily Check-ins", "📝 Weekly Reflections"])
    
    with tab1:
        st.markdown("### 📋 Past Weekly Plans")
        
        weekly_plans = load_weekly_plans()
        if not weekly_plans:
            st.info("No weekly plans found. Create your first plan to see it here!")
            if st.button("Create Weekly Plan"):
                st.switch_page("pages/2_Weekly_Plan.py")
        else:
            # Show plans in reverse chronological order
            for i, entry in enumerate(reversed(weekly_plans)):
                with st.expander(f"📅 Week of {entry.get('date', 'Unknown')}", expanded=(i == 0)):
                    st.markdown(f"**🎯 Main Objective:** {entry.get('main_objective', 'Not set')}")
                    
                    # Show inputs
                    inputs = entry.get('inputs', {})
                    if inputs:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**😊 Mood:** {inputs.get('mood', 'Not specified')}")
                            st.markdown(f"**⏰ Availability:** {inputs.get('availability', 'Not specified')}")
                        with col2:
                            st.markdown(f"**🎯 Focus:** {inputs.get('focus', 'Not specified')}")
                    
                    # Show the plan
                    st.markdown("**📋 Weekly Plan:**")
                    st.markdown(entry.get('plan', 'No plan content'))
                    
                    # Show date
                    st.markdown(f"*Created: {entry.get('date', 'Unknown')}*")
    
    with tab2:
        st.markdown("### 🌤️ Past Daily Check-ins")
        
        daily_checkins = load_daily_checkins()
        if not daily_checkins:
            st.info("No daily check-ins found. Start checking in daily to see your history!")
            if st.button("Start Daily Check-in"):
                st.switch_page("pages/3_Daily_Checkin.py")
        else:
            # Show check-ins in reverse chronological order
            for i, entry in enumerate(reversed(daily_checkins)):
                with st.expander(f"🌤️ {entry.get('inputs', {}).get('day', 'Unknown Day')} - {entry.get('date', 'Unknown')}", expanded=(i < 3)):
                    inputs = entry.get('inputs', {})
                    
                    # Show check-in details
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**😊 Mood:** {inputs.get('mood', 'Not specified')}")
                        st.markdown(f"**🎯 Focus:** {inputs.get('focus', 'Not specified')}")
                    with col2:
                        st.markdown(f"**📋 Today's Task:** {inputs.get('today_task', 'Not specified')}")
                        st.markdown(f"**✅ Yesterday's Status:** {inputs.get('yesterday_status', 'Not specified')}")
                    
                    # Show AI response
                    st.markdown("**🤖 AI Coach Response:**")
                    st.markdown(entry.get('response', 'No response'))
                    
                    # Show date
                    st.markdown(f"*Check-in: {entry.get('date', 'Unknown')}*")
    
    with tab3:
        st.markdown("### 📝 Past Weekly Reflections")
        
        weekly_reflections = load_weekly_reflections()
        if not weekly_reflections:
            st.info("No weekly reflections found. Complete a weekly reflection to see your insights!")
            if st.button("Start Weekly Reflection"):
                st.switch_page("pages/4_Reflection.py")
        else:
            # Show reflections in reverse chronological order
            for i, entry in enumerate(reversed(weekly_reflections)):
                with st.expander(f"📝 Week Reflection - {entry.get('date', 'Unknown')}", expanded=(i == 0)):
                    inputs = entry.get('inputs', {})
                    
                    # Show reflection inputs
                    st.markdown("**📊 Reflection Summary:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**🎯 Achievements:** {inputs.get('achievements', 'Not specified')[:100]}...")
                        st.markdown(f"**⚠️ Challenges:** {inputs.get('challenges', 'Not specified')[:100]}...")
                    with col2:
                        st.markdown(f"**🧠 Learnings:** {inputs.get('learnings', 'Not specified')[:100]}...")
                        st.markdown(f"**📈 Next Week Focus:** {inputs.get('next_week_focus', 'Not specified')[:100]}...")
                    
                    # Show overall rating
                    rating = inputs.get('overall_rating', 0)
                    st.markdown(f"**⭐ Overall Rating:** {rating}/10")
                    
                    # Show AI analysis
                    st.markdown("**🤖 AI Coach Analysis:**")
                    st.markdown(entry.get('reflection', 'No analysis'))
                    
                    # Show date
                    st.markdown(f"*Reflection: {entry.get('date', 'Unknown')}*")

    # Statistics
    st.markdown("---")
    st.markdown("### 📊 History Statistics")
    
    weekly_plans = load_weekly_plans()
    daily_checkins = load_daily_checkins()
    weekly_reflections = load_weekly_reflections()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Total Plans", len(weekly_plans))
        if weekly_plans:
            latest_plan = weekly_plans[-1].get('date', 'Unknown')
            st.markdown(f"*Latest: {latest_plan}*")
    
    with col2:
        st.metric("🌤️ Total Check-ins", len(daily_checkins))
        if daily_checkins:
            latest_checkin = daily_checkins[-1].get('date', 'Unknown')
            st.markdown(f"*Latest: {latest_checkin}*")
    
    with col3:
        st.metric("📝 Total Reflections", len(weekly_reflections))
        if weekly_reflections:
            latest_reflection = weekly_reflections[-1].get('date', 'Unknown')
            st.markdown(f"*Latest: {latest_reflection}*")
    
    with col4:
        # Calculate average rating from reflections
        if weekly_reflections:
            ratings = [r.get('inputs', {}).get('overall_rating', 0) for r in weekly_reflections]
            avg_rating = sum(ratings) / len(ratings)
            st.metric("⭐ Avg Rating", f"{avg_rating:.1f}/10")
        else:
            st.metric("⭐ Avg Rating", "N/A")

    # Quick actions
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        if st.button("📋 Create Plan", use_container_width=True):
            st.switch_page("pages/2_Weekly_Plan.py")
    
    with action_col2:
        if st.button("🌤️ Daily Check-in", use_container_width=True):
            st.switch_page("pages/3_Daily_Checkin.py")
    
    with action_col3:
        if st.button("📝 Weekly Reflection", use_container_width=True):
            st.switch_page("pages/4_Reflection.py")
    
    with action_col4:
        if st.button("📊 View Progress", use_container_width=True):
            st.switch_page("pages/5_Progress.py")

if __name__ == "__main__":
    main() 