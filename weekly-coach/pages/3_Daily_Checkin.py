import streamlit as st
import os
import json
from coach import daily_checkin, save_daily_checkin_to_log, update_user_progress, update_task_completion_status, get_current_week_summary
from datetime import datetime, timedelta
from setup import load_user_profile

st.set_page_config(page_title="Daily Check-in", page_icon="🌤️")

def load_weekly_plans():
    log_path = "logs/weekly_plans.json"
    if not os.path.exists(log_path):
        return []
    try:
        with open(log_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def get_task_for_day(plan_text, day):
    """Get task for the day - improved to handle different formats"""
    patterns = [
        f"- **{day}:**",
        f"- {day}:",
        f"**{day}:**",
        f"{day}:",
        f"- {day}",
    ]
    
    lines = plan_text.splitlines()
    for line in lines:
        line = line.strip()
        for pattern in patterns:
            if line.startswith(pattern):
                task = line.replace(pattern, "").strip()
                task = task.replace("**", "").replace("*", "")
                return task if task else "Task found but no description"
    
    return "Not found"

def main():
    st.title("🌤️ Daily Check-in")
    st.markdown("Check in with your AI coach to stay on track")
    
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

    # Daily checkin
    st.markdown("### 🌤️ How are you doing today?")
    st.info("Take a moment to reflect on your progress and get personalized guidance.")
    
    # Get the most recent weekly plan
    logs = load_weekly_plans()
    if not logs:
        st.info("No weekly plan found. Please create a plan first.")
        if st.button("Create Weekly Plan"):
            st.switch_page("pages/2_Weekly_Plan.py")
    else:
        latest_plan = logs[-1]["plan"]
        
        today = datetime.now()
        day_str = today.strftime("%A")
        yesterday = (today - timedelta(days=1)).strftime("%A")

        # Show today's task
        today_task = get_task_for_day(latest_plan, day_str)
        if today_task != "Not found":
            st.markdown(f"**📋 Today's Task:** {today_task}")

        with st.form("daily_checkin_form"):
            mood = st.selectbox(
                "How are you feeling today?",
                ["Great", "Good", "Okay", "Tired", "Stressed", "Motivated", "Other"],
                help="Your mood helps us provide better guidance"
            )
            
            focus = st.text_input(
                "Is there any specific focus for today?", 
                placeholder="e.g. finishing a project, learning something new, taking care of myself",
                help="Optional - helps us tailor our advice"
            )

            yesterday_task = get_task_for_day(latest_plan, yesterday)
            yesterday_status = st.selectbox(
                f"Did you complete yesterday's task?",
                ["Yes", "Partially", "No", "Didn't try"],
                help="Be honest - this helps us understand your patterns"
            )

            if yesterday_task != "Not found":
                st.markdown(f"*Yesterday's task was: {yesterday_task}*")

            submitted = st.form_submit_button("🔍 Check In", type="primary")

        if submitted:
            with st.spinner("🤖 Getting your personalized check-in..."):
                try:
                    response = daily_checkin(
                        goal=profile["goal"],
                        motivation=profile.get("motivation", ""),
                        weekly_plan=latest_plan,
                        day=day_str,
                        yesterday_task=yesterday_task,
                        yesterday_status=yesterday_status,
                        mood=mood,
                        focus=focus,
                        today_task=today_task
                    )

                    # Save the checkin
                    save_daily_checkin_to_log(
                        inputs={
                            "day": day_str,
                            "mood": mood,
                            "focus": focus,
                            "yesterday_task": yesterday_task,
                            "yesterday_status": yesterday_status,
                            "today_task": today_task
                        },
                        response=response
                    )

                    # Update progress tracking
                    update_user_progress()
                    
                    # Update task completion status for yesterday
                    if yesterday_task != "Not found":
                        update_task_completion_status(yesterday, yesterday_status)

                    st.success("✅ Daily check-in saved and progress updated!")
                    
                    # Display the response
                    st.markdown("### 🤖 Your AI Coach Says:")
                    st.markdown(response)
                    
                    # Next steps
                    st.markdown("---")
                    st.markdown("### 🎯 Keep going!")
                    st.markdown("You're doing great! Here are some next steps:")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📋 View Weekly Plan"):
                            st.switch_page("pages/2_Weekly_Plan.py")
                    with col2:
                        if st.button("📊 Check Progress"):
                            st.switch_page("pages/5_Progress.py")
                    with col3:
                        if st.button("📝 Weekly Reflection"):
                            st.switch_page("pages/4_Reflection.py")
                            
                except Exception as e:
                    st.error(f"Sorry, there was an error during your check-in: {str(e)}")
                    st.info("Please try again or check your internet connection.")

    # Show current week progress
    st.markdown("---")
    week_summary = get_current_week_summary()
    if week_summary:
        st.markdown("### 📅 This Week's Progress")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📋 Total Tasks", week_summary["total_tasks"])
        with col2:
            st.metric("✅ Completed", f"{week_summary['completed_tasks']}/{week_summary['total_tasks']}")
        with col3:
            completion_rate = week_summary["completion_rate"]
            st.metric("📊 Progress", f"{completion_rate}%")
        
        # Progress bar
        st.progress(completion_rate / 100)
        
        # Show today's task prominently
        if today_task != "Not found":
            st.markdown(f"**🎯 Today's Focus:** {today_task}")

    # Tips for effective check-ins
    st.markdown("---")
    st.markdown("### 💡 Tips for Effective Check-ins")
    
    tips_col1, tips_col2 = st.columns(2)
    with tips_col1:
        st.markdown("**🎯 Be Honest**")
        st.markdown("- Your AI coach learns from your patterns")
        st.markdown("- Honest feedback leads to better guidance")
        
        st.markdown("**⏰ Check in Regularly**")
        st.markdown("- Daily check-ins build momentum")
        st.markdown("- Even quick check-ins are valuable")
    
    with tips_col2:
        st.markdown("**📝 Reflect Briefly**")
        st.markdown("- Take a moment to think about your day")
        st.markdown("- Note what worked and what didn't")
        
        st.markdown("**🎉 Celebrate Wins**")
        st.markdown("- Acknowledge your progress")
        st.markdown("- Small wins add up to big results")

if __name__ == "__main__":
    main() 