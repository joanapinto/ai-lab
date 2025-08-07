import streamlit as st
import json
import os
from datetime import datetime
from setup import load_user_profile, save_user_profile

st.set_page_config(page_title="Setup Your Coach", page_icon="🎯")

def main():
    st.title("🎯 Setup Your Weekly Coach")
    st.markdown("Let's get to know you and your goals better")
    
    # Add a back button
    if st.button("← Back to Home"):
        st.switch_page("main.py")
    
    existing_profile = load_user_profile()

    if existing_profile:
        st.success("✅ You've already completed setup.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🎯 Main Goal:**")
            st.write(existing_profile.get("goal"))
            st.markdown("**📅 Deadline:**")
            st.write(existing_profile.get("deadline", "None"))
            st.markdown("**💭 Motivation:**")
            st.write(existing_profile.get("motivation", "None"))
        
        with col2:
            if "preferences" in existing_profile:
                prefs = existing_profile["preferences"]
                st.markdown("**⚙️ Preferences:**")
                st.write(f"**Coaching Style:** {prefs.get('coaching_style', 'Not set')}")
                st.write(f"**Focus Areas:** {', '.join(prefs.get('focus_areas', []))}")
                st.write(f"**Working Hours:** {prefs.get('working_hours', {}).get('start', 'Not set')} - {prefs.get('working_hours', {}).get('end', 'Not set')}")
                st.write(f"**Reminders:** {prefs.get('notification_frequency', 'Not set')}")
        
        # Show progress if it exists
        if "progress" in existing_profile:
            progress = existing_profile["progress"]
            st.markdown("**📊 Progress:**")
            st.write(f"**Total Check-ins:** {progress.get('total_checkins', 0)}")
            st.write(f"**Total Weeks:** {progress.get('total_weeks', 0)}")
            st.write(f"**Completion Rate:** {progress.get('completion_rate', 0)}%")
            st.write(f"**Streak Days:** {progress.get('streak_days', 0)}")
        
        # Show current week if it exists
        if "current_week" in existing_profile:
            current_week = existing_profile["current_week"]
            if current_week.get("main_objective"):
                st.markdown("**📅 Current Week:**")
                st.write(f"**Main Objective:** {current_week.get('main_objective')}")
                st.write(f"**Week Start:** {current_week.get('week_start')}")
                st.write(f"**Tasks:** {len(current_week.get('daily_tasks', {}))} daily tasks")
        
        # Show reflection insights if they exist
        if "reflections" in existing_profile:
            reflections = existing_profile["reflections"]
            if reflections.get("total_reflections", 0) > 0:
                st.markdown("**🧠 Reflection Insights:**")
                st.write(f"**Total Reflections:** {reflections.get('total_reflections', 0)}")
                st.write(f"**Success Patterns:** {len(reflections.get('success_patterns', []))}")
                st.write(f"**Common Challenges:** {len(reflections.get('common_challenges', []))}")
                if reflections.get("insights"):
                    st.write(f"**Key Insights:** {len(reflections.get('insights', []))} insights generated")
        
        if st.button("Reset and start over"):
            os.remove("user_profile.json")
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🚀 Ready to continue?")
        if st.button("Go to Dashboard", type="primary"):
            st.switch_page("main.py")
        return

    # Setup form for new users
    st.markdown("### 🎯 Tell us about your goals")
    st.info("This information helps us create personalized weekly plans and coaching for you.")
    
    with st.form("goal_setup_form"):
        st.markdown("#### 🎯 Your Goal")
        goal = st.text_area("What's your long-term goal?", placeholder="e.g. Build 3 AI tools by December", help="Be specific about what you want to achieve")
        motivation = st.text_area("Why is this important to you?", placeholder="Optional...", help="Understanding your motivation helps us keep you motivated")
        deadline = st.date_input("Do you have a deadline?", value=None, help="Optional - helps with planning and urgency")
        
        st.markdown("#### ⚙️ Your Preferences")
        coaching_style = st.selectbox(
            "What coaching style works best for you?",
            ["Motivational", "Strict", "Gentle", "Technical", "Balanced"],
            help="Choose the style that motivates you most"
        )
        
        focus_areas = st.multiselect(
            "What are your main focus areas?",
            ["AI/ML", "Programming", "Learning", "Career", "Health", "Relationships", "Finance", "Other"],
            default=["AI/ML", "Learning"],
            help="Select areas that are most relevant to your goals"
        )
        
        st.markdown("#### ⏰ Your Schedule")
        working_hours = st.columns(2)
        with working_hours[0]:
            work_start = st.time_input("When do you typically start working?", value=datetime.strptime("09:00", "%H:%M").time(), help="This helps us plan tasks around your schedule")
        with working_hours[1]:
            work_end = st.time_input("When do you typically finish working?", value=datetime.strptime("17:00", "%H:%M").time(), help="This helps us plan tasks around your schedule")
        
        notification_frequency = st.selectbox(
            "How often would you like to be reminded?",
            ["Daily", "Every other day", "Weekly", "Only when I check in"],
            help="Choose how often you want to be reminded to check in"
        )
        
        submitted = st.form_submit_button("🚀 Save Goal & Preferences", type="primary")

    if submitted:
        if not goal.strip():
            st.error("Please enter your goal.")
        else:
            profile = {
                "goal": goal.strip(),
                "motivation": motivation.strip(),
                "deadline": deadline.strftime("%d-%m-%Y") if deadline else None,
                "start_date": datetime.now().strftime("%d-%m-%Y"),
                "history": [],
                "preferences": {
                    "coaching_style": coaching_style,
                    "focus_areas": focus_areas,
                    "working_hours": {
                        "start": work_start.strftime("%H:%M"),
                        "end": work_end.strftime("%H:%M")
                    },
                    "notification_frequency": notification_frequency
                },
                "progress": {
                    "total_weeks": 0,
                    "total_checkins": 0,
                    "completion_rate": 0.0,
                    "streak_days": 0,
                    "last_checkin_date": None,
                    "achievements": [],
                    "weekly_completion_rates": []
                },
                "current_week": {
                    "week_start": None,
                    "main_objective": None,
                    "daily_tasks": {},
                    "completion_status": {},
                    "last_updated": None
                },
                "reflections": {
                    "total_reflections": 0,
                    "last_reflection_date": None,
                    "common_challenges": [],
                    "success_patterns": [],
                    "goal_evolution": [],
                    "insights": []
                }
            }
            save_user_profile(profile)
            st.success("🎉 Goal and preferences saved! You're all set to begin.")
            
            st.markdown("### 🚀 What's next?")
            st.markdown("Now you can:")
            st.markdown("1. **Create your first weekly plan** - Get a personalized plan for this week")
            st.markdown("2. **Start daily check-ins** - Track your progress daily")
            st.markdown("3. **View your dashboard** - See your progress and insights")
            
            if st.button("Go to Dashboard", type="primary"):
                st.switch_page("main.py")

if __name__ == "__main__":
    main() 