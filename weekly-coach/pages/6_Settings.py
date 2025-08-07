import streamlit as st
import json
import os
from datetime import datetime
from setup import load_user_profile, save_user_profile

st.set_page_config(page_title="Settings", page_icon="🔧")

def main():
    st.title("🔧 Settings")
    st.markdown("Manage your preferences and account settings")
    
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

    # Settings sections
    st.markdown("### ⚙️ Account Settings")
    
    with st.expander("🎯 Goal & Motivation", expanded=True):
        with st.form("goal_settings_form"):
            new_goal = st.text_area(
                "Update your main goal",
                value=profile.get("goal", ""),
                help="Your primary objective"
            )
            
            new_motivation = st.text_area(
                "Update your motivation",
                value=profile.get("motivation", ""),
                help="Why this goal is important to you"
            )
            
            new_deadline = st.date_input(
                "Update your deadline",
                value=None,
                help="Optional - when you want to achieve your goal"
            )
            
            goal_submitted = st.form_submit_button("💾 Save Goal Changes")
            
        if goal_submitted:
            profile["goal"] = new_goal.strip()
            profile["motivation"] = new_motivation.strip()
            if new_deadline:
                profile["deadline"] = new_deadline.strftime("%d-%m-%Y")
            else:
                profile["deadline"] = None
            
            save_user_profile(profile)
            st.success("✅ Goal settings updated!")

    with st.expander("⚙️ Preferences"):
        preferences = profile.get("preferences", {})
        
        with st.form("preferences_form"):
            coaching_style = st.selectbox(
                "Coaching Style",
                ["Motivational", "Strict", "Gentle", "Technical", "Balanced"],
                index=["Motivational", "Strict", "Gentle", "Technical", "Balanced"].index(
                    preferences.get("coaching_style", "Balanced")
                ),
                help="How your AI coach should communicate with you"
            )
            
            focus_areas = st.multiselect(
                "Focus Areas",
                ["AI/ML", "Programming", "Learning", "Career", "Health", "Relationships", "Finance", "Other"],
                default=preferences.get("focus_areas", ["AI/ML", "Learning"]),
                help="Areas most relevant to your goals"
            )
            
            st.markdown("**Working Hours:**")
            work_col1, work_col2 = st.columns(2)
            with work_col1:
                work_start = st.time_input(
                    "Start Time",
                    value=datetime.strptime(preferences.get("working_hours", {}).get("start", "09:00"), "%H:%M").time(),
                    help="When you typically start working"
                )
            with work_col2:
                work_end = st.time_input(
                    "End Time",
                    value=datetime.strptime(preferences.get("working_hours", {}).get("end", "17:00"), "%H:%M").time(),
                    help="When you typically finish working"
                )
            
            notification_frequency = st.selectbox(
                "Reminder Frequency",
                ["Daily", "Every other day", "Weekly", "Only when I check in"],
                index=["Daily", "Every other day", "Weekly", "Only when I check in"].index(
                    preferences.get("notification_frequency", "Daily")
                ),
                help="How often you want to be reminded"
            )
            
            prefs_submitted = st.form_submit_button("💾 Save Preferences")
            
        if prefs_submitted:
            if "preferences" not in profile:
                profile["preferences"] = {}
            
            profile["preferences"]["coaching_style"] = coaching_style
            profile["preferences"]["focus_areas"] = focus_areas
            profile["preferences"]["working_hours"] = {
                "start": work_start.strftime("%H:%M"),
                "end": work_end.strftime("%H:%M")
            }
            profile["preferences"]["notification_frequency"] = notification_frequency
            
            save_user_profile(profile)
            st.success("✅ Preferences updated!")

    with st.expander("📊 Data & Privacy"):
        st.markdown("**Your Data:**")
        st.markdown("- All your data is stored locally on your device")
        st.markdown("- No data is sent to external servers except for AI processing")
        st.markdown("- Your personal information is kept private")
        
        st.markdown("**Data Storage:**")
        st.markdown("- User profile: `user_profile.json`")
        st.markdown("- Weekly plans: `logs/weekly_plans.json`")
        st.markdown("- Daily check-ins: `logs/daily_checkins.json`")
        st.markdown("- Weekly reflections: `logs/weekly_reflections.json`")
        
        # Export data option
        if st.button("📤 Export My Data"):
            try:
                # Create a backup of all data
                backup_data = {
                    "profile": profile,
                    "export_date": datetime.now().isoformat(),
                    "version": "1.0"
                }
                
                # Add logs if they exist
                log_files = ["weekly_plans.json", "daily_checkins.json", "weekly_reflections.json"]
                for log_file in log_files:
                    log_path = f"logs/{log_file}"
                    if os.path.exists(log_path):
                        with open(log_path, "r") as f:
                            backup_data[log_file.replace(".json", "")] = json.load(f)
                
                # Create download
                st.download_button(
                    label="📥 Download Backup",
                    data=json.dumps(backup_data, indent=2),
                    file_name=f"weekly_coach_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"Error creating backup: {str(e)}")

    with st.expander("🗑️ Reset & Delete"):
        st.warning("⚠️ **Danger Zone** - These actions cannot be undone!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Reset Progress", type="secondary"):
                if "progress" in profile:
                    profile["progress"] = {
                        "total_weeks": 0,
                        "total_checkins": 0,
                        "completion_rate": 0.0,
                        "streak_days": 0,
                        "last_checkin_date": None,
                        "achievements": [],
                        "weekly_completion_rates": []
                    }
                    save_user_profile(profile)
                    st.success("✅ Progress reset! Your goal and preferences are kept.")
        
        with col2:
            if st.button("🗑️ Delete All Data", type="secondary"):
                # Delete all log files
                log_files = ["weekly_plans.json", "daily_checkins.json", "weekly_reflections.json"]
                for log_file in log_files:
                    log_path = f"logs/{log_file}"
                    if os.path.exists(log_path):
                        os.remove(log_path)
                
                # Delete user profile
                if os.path.exists("user_profile.json"):
                    os.remove("user_profile.json")
                
                st.success("✅ All data deleted! You'll need to set up again.")
                st.rerun()

    # Account info
    st.markdown("---")
    st.markdown("### 📋 Account Information")
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown("**📅 Account Created:**")
        st.write(profile.get("start_date", "Unknown"))
        
        st.markdown("**🎯 Current Goal:**")
        st.write(profile.get("goal", "Not set"))
        
        st.markdown("**📊 Total Check-ins:**")
        progress = profile.get("progress", {})
        st.write(progress.get("total_checkins", 0))
    
    with info_col2:
        st.markdown("**📅 Last Check-in:**")
        last_checkin = progress.get("last_checkin_date")
        st.write(last_checkin if last_checkin else "Never")
        
        st.markdown("**📈 Completion Rate:**")
        completion_rate = progress.get("completion_rate", 0)
        st.write(f"{completion_rate}%")
        
        st.markdown("**🔥 Current Streak:**")
        st.write(f"{progress.get('streak_days', 0)} days")

    # Quick actions
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("📋 Create Plan", use_container_width=True):
            st.switch_page("pages/2_Weekly_Plan.py")
    
    with action_col2:
        if st.button("🌤️ Daily Check-in", use_container_width=True):
            st.switch_page("pages/3_Daily_Checkin.py")
    
    with action_col3:
        if st.button("📊 View Progress", use_container_width=True):
            st.switch_page("pages/5_Progress.py")

if __name__ == "__main__":
    main() 