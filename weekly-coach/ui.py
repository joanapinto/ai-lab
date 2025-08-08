import streamlit as st
import os
import json
from coach import generate_weekly_plan, save_weekly_plan_to_log, generate_weekly_reflection, save_weekly_reflection_to_log, regenerate_weekly_plan, daily_checkin, save_daily_checkin_to_log, update_user_progress, get_user_achievements, update_current_week_context, update_task_completion_status, get_current_week_summary, update_reflection_history, get_reflection_summary
from datetime import datetime, timedelta
from setup import load_user_profile

st.set_page_config(page_title="Weekly Coach GPT", page_icon="🧠")

st.title("🧠 Weekly Coach GPT")
st.subheader("Let’s build a weekly plan together")

# Check for user profile
profile = load_user_profile()
if not profile:
    st.warning("Please set up your main objective first.")
    st.info("Go to the setup page to enter your main objective, motivation, and deadline.")
    st.stop()

# Show main objective at the top
if "goal" in profile:
    st.markdown(f"**🎯 Main Objective:** {profile['goal']}")

# Progress Dashboard
if "progress" in profile:
    progress = profile["progress"]
    
    # Update progress first
    update_user_progress()
    
    # Reload profile to get updated progress
    profile = load_user_profile()
    progress = profile.get("progress", {})
    
    # Display progress metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Check-ins", progress.get("total_checkins", 0))
    
    with col2:
        st.metric("📅 Total Weeks", progress.get("total_weeks", 0))
    
    with col3:
        completion_rate = progress.get("completion_rate", 0)
        st.metric("✅ Completion Rate", f"{completion_rate}%")
    
    with col4:
        st.metric("🔥 Streak Days", progress.get("streak_days", 0))
    
    # Show achievements
    achievements = get_user_achievements(profile)
    if achievements:
        st.markdown("**🏆 Achievements:**")
        for achievement in achievements:
            st.markdown(f"- {achievement}")
    
    st.markdown("---")

# Current Week Summary
week_summary = get_current_week_summary()
if week_summary:
    st.markdown("### 📅 Current Week Summary")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Main Objective", week_summary["main_objective"] or "Not set")
    with col2:
        st.metric("📋 Total Tasks", week_summary["total_tasks"])
    with col3:
        st.metric("✅ Completed", f"{week_summary['completed_tasks']}/{week_summary['total_tasks']}")
    
    # Show completion rate
    completion_rate = week_summary["completion_rate"]
    st.progress(completion_rate / 100)
    st.markdown(f"**Progress:** {completion_rate}% complete")
    
    # Show daily tasks with status
    if week_summary["daily_tasks"]:
        st.markdown("**📝 Daily Tasks:**")
        for day, task in week_summary["daily_tasks"].items():
            status = week_summary["completion_status"].get(day, {}).get("status", "Not started")
            status_emoji = {"Yes": "✅", "Partially": "🟡", "No": "❌", "Not started": "⏳"}
            
            st.markdown(f"{status_emoji.get(status, '⏳')} **{day}:** {task}")
            if status != "Not started":
                st.markdown(f"   *Status: {status}*")
    
    st.markdown("---")

# Reflection Insights
reflection_summary = get_reflection_summary()
if reflection_summary and reflection_summary["total_reflections"] > 0:
    st.markdown("### 🧠 Reflection Insights")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📝 Total Reflections", reflection_summary["total_reflections"])
        if reflection_summary["last_reflection_date"]:
            last_reflection = datetime.fromisoformat(reflection_summary["last_reflection_date"])
            st.metric("🕒 Last Reflection", last_reflection.strftime("%d %b"))
    
    with col2:
        st.metric("🎯 Success Patterns", len(reflection_summary["success_patterns"]))
        st.metric("💡 Challenges", len(reflection_summary["common_challenges"]))
    
    # Show insights
    if reflection_summary["insights"]:
        st.markdown("**💡 Key Insights:**")
        for insight in reflection_summary["insights"]:
            st.markdown(f"- {insight}")
    
    st.markdown("---")

# Load weekly plans function
def load_weekly_plans():
    log_path = "logs/weekly_plans.json"
    if not os.path.exists(log_path):
        return []
    try:
        with open(log_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

# Weekly plan form
with st.form("weekly_plan_form"):
    mood = st.text_input("How are you feeling this week?")
    availability = st.text_input("How much time do you have each day?")
    focus = st.text_input("Any particular focus? (optional)")

    submitted = st.form_submit_button("Generate Plan")

if submitted:
    with st.spinner("Thinking..."):
        plan, main_objective = generate_weekly_plan(
            mood=mood,
            availability=availability,
            focus=focus,
        )
        # Save to log
        save_weekly_plan_to_log(
            inputs={
                "mood": mood,
                "availability": availability,
                "focus": focus
            },
            plan=plan,
            main_objective=main_objective
        )
        
        # Update progress tracking
        update_user_progress()
        
        # Update current week context
        update_current_week_context(plan, main_objective)
        
    st.success("Here's your plan!")
    st.markdown(plan)

# Get task for the day - improved to handle different formats
def get_task_for_day(plan_text, day):
    # Try different patterns for finding the day's task
    patterns = [
        f"- **{day}:**",  # Bold format
        f"- {day}:",      # Regular format
        f"**{day}:**",    # Just bold
        f"{day}:",        # Just colon
        f"- {day}",       # Just dash
    ]
    
    lines = plan_text.splitlines()
    for i, line in enumerate(lines):
        line = line.strip()
        for pattern in patterns:
            if line.startswith(pattern):
                # Remove the pattern and clean up
                task = line.replace(pattern, "").strip()
                # Remove any remaining markdown formatting
                task = task.replace("**", "").replace("*", "")
                
                # If the task is empty, check the next lines for content
                if not task:
                    task_lines = []
                    j = i + 1
                    while j < len(lines):
                        next_line = lines[j].strip()
                        # Stop if we hit another day or section
                        if (next_line.startswith("- **") or 
                            next_line.startswith("###") or 
                            next_line.startswith("---") or
                            not next_line):
                            break
                        # Add non-empty lines to the task
                        if next_line:
                            task_lines.append(next_line.replace("**", "").replace("*", ""))
                        j += 1
                    
                    if task_lines:
                        task = " ".join(task_lines)
                
                return task if task else f"No specific task for {day}"
    
    return "Not found"


# Daily checkin
with st.expander("🌤️ Daily Check-In"):
    st.markdown("Check in with your assistant to stay on track!")

    today = datetime.now()
    day_str = today.strftime("%A")
    yesterday = (today - timedelta(days=1)).strftime("%A")

    mood = st.selectbox("How are you feeling today?", ["Great", "Okay", "Tired", "Stressed", "Motivated", "Other"])
    focus = st.text_input("Is there any specific focus for today?", "")

    # Get the most recent weekly plan
    logs = load_weekly_plans()
    if not logs:
        st.info("No weekly plan found. Please generate a plan first.")
        st.stop()
    
    latest_plan = logs[-1]["plan"]
    
    # Show today's task
    today_task = get_task_for_day(latest_plan, day_str)
    if today_task != "Not found":
        st.markdown(f"**📋 Today's Task:** {today_task}")
    
    yesterday_task = get_task_for_day(latest_plan, yesterday)

    yesterday_status = st.selectbox(
        f"Did you complete yesterday’s task ({yesterday_task})?",
        ["Yes", "Partially", "No", "Didn't try"]
    )

    if st.button("🔍 Check In"):
            with st.spinner("Getting your personalized check-in..."):
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

                st.markdown("### 🤖 Your Assistant Says:")
                st.markdown(response)
                st.success("✅ Daily check-in saved and progress updated!")

# Progress tracking
def calculate_weekly_progress(latest_plan):
    """Calculate completion rate for the current week"""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    completed = 0
    total = 0
    
    # Load daily checkins for this week
    try:
        with open("logs/daily_checkins.json", "r") as f:
            checkins = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        checkins = []
    
    # Get this week's checkins (last 7 days)
    week_start = datetime.now() - timedelta(days=7)
    this_week_checkins = [
        c for c in checkins 
        if datetime.fromisoformat(c['timestamp']) >= week_start
    ]
    
    # Count completed tasks
    for checkin in this_week_checkins:
        status = checkin['inputs'].get('yesterday_status', '')
        if status in ['Yes', 'Partially']:
            completed += 1
        total += 1
    
    return completed, total

# Show progress if we have a plan and checkins
if 'latest_plan' in locals():
    completed, total = calculate_weekly_progress(latest_plan)
    if total > 0:
        progress_rate = (completed / total) * 100
        st.markdown(f"**📊 This Week's Progress:** {completed}/{total} tasks completed ({progress_rate:.1f}%)")
        
        # Progress bar
        st.progress(progress_rate / 100)
    else:
        st.info("📊 Complete your first daily check-in to see progress tracking!")


# View past plans
st.markdown("---")
with st.expander("📚 View Past Weekly Plans"):
    logs = load_weekly_plans()

    if not logs:
        st.info("No plans saved yet.")
    else:
        # Extract available months from logs
        unique_months = sorted({
            datetime.fromisoformat(entry['timestamp']).strftime("%B %Y")
            for entry in logs
        }, reverse=True)

        selected_month = st.selectbox("Select a month", unique_months)

        # Filter logs by selected month
        filtered_logs = [
            entry for entry in logs
            if datetime.fromisoformat(entry['timestamp']).strftime("%B %Y") == selected_month
        ]

        # Optional: further filter by week (first day of the week)
        week_dates = sorted({
            datetime.fromisoformat(entry['timestamp']).strftime("%d-%m-%Y")
            for entry in filtered_logs
        }, reverse=True)

        selected_week = st.selectbox("Optional: Filter by week start date", ["All"] + week_dates)

        for entry in reversed(filtered_logs):
            timestamp = datetime.fromisoformat(entry['timestamp'])
            formatted_date = timestamp.strftime("%d-%m-%Y")

            # Apply week filter if selected
            if selected_week != "All" and formatted_date != selected_week:
                continue

            st.subheader(f"🗓️ {formatted_date}")
            inputs = entry['inputs']
            st.markdown(f"""
            - **Mood:** {inputs.get("mood", "")}  
            - **Availability:** {inputs.get("availability", "")}  
            {f"- **Focus:** {inputs.get('focus', '')}" if inputs.get("focus") else ""}
            """)
            if entry.get('plan') and entry['plan'].strip():
                st.markdown(entry['plan'])
            
            st.markdown("---")

# Reflect on last week
with st.expander("📝 Reflect on Last Week"):
    logs = load_weekly_plans()

    if not logs:
        st.info("No past plans available for reflection.")
    else:
        # Get last week’s plan
        last_log = logs[-1]
        last_week_plan = last_log["plan"]

        st.markdown("### How did last week go?")
        objective_achieved = st.radio("Did you achieve your main goal?", ["Yes", "Partially", "No"])
        notes = st.text_area("Add any reflections or notes about your week")

        if st.button("Generate Weekly Reflection"):
            with st.spinner("Thinking about your week..."):
                reflection = generate_weekly_reflection(
                    goal=profile["goal"],
                    motivation=profile.get("motivation", ""),
                    deadline=profile.get("deadline", ""),
                    last_week_plan=last_week_plan,
                    objective_achieved=objective_achieved,
                    notes=notes
                )

                st.markdown(reflection)
                
            save_weekly_reflection_to_log(
                inputs={
                    "objective_achieved": objective_achieved,
                    "notes": notes
                },
                reflection=reflection
            )
            
            # Update reflection history
            update_reflection_history({
                "objective_achieved": objective_achieved,
                "notes": notes,
                "reflection": reflection
            })

        # Optional: Offer to regenerate a new plan
        if objective_achieved in ["No", "Partially"]:
            if st.button("🔁 Rebuild this week’s plan based on last week"):
                with st.spinner("Creating an adjusted plan..."):
                    new_plan = regenerate_weekly_plan(
                        goal=profile["goal"],
                        motivation=profile.get("motivation", ""),
                        deadline=profile.get("deadline", ""),
                        last_plan=last_week_plan,
                        objective_achieved=objective_achieved,
                        notes=notes
                    )

                    st.markdown("### 📅 Your Adjusted Weekly Plan")
                    st.markdown(new_plan)

# View past reflections
with st.expander("📖 View Past Reflections"):
    import os
    import json

    reflections_path = "logs/weekly_reflections.json"
    if not os.path.exists(reflections_path):
        st.info("No past reflections found.")
    else:
        try:
            with open(reflections_path, "r") as f:
                reflections = json.load(f)
        except Exception:
            st.error("Could not load past reflections.")
            reflections = []

        if not reflections:
            st.info("No past reflections found.")
        else:
            for entry in reversed(reflections):
                timestamp = entry.get("timestamp", "")
                try:
                    from datetime import datetime
                    formatted_date = datetime.fromisoformat(timestamp).strftime("%A, %d %B %Y %H:%M")
                except Exception:
                    formatted_date = timestamp
                st.subheader(f"🗓️ {formatted_date}")
                inputs = entry.get("inputs", {})
                st.markdown(f"""
                - **Objective Achieved:** {inputs.get("objective_achieved", "")}  
                {f'- **Notes:** {inputs.get("notes", "")}' if inputs.get("notes") else ""}
                """)
                st.markdown(entry.get("reflection", ""))
                st.markdown("---")

# View past daily checkins
with st.expander("📅 View Past Daily Check-ins"):
    checkins_path = "logs/daily_checkins.json"
    if not os.path.exists(checkins_path):
        st.info("No past daily check-ins found.")
    else:
        try:
            with open(checkins_path, "r") as f:
                checkins = json.load(f)
        except Exception:
            st.error("Could not load past check-ins.")
            checkins = []

        if not checkins:
            st.info("No past daily check-ins found.")
        else:
            # Group by week
            for entry in reversed(checkins):
                timestamp = entry.get("timestamp", "")
                try:
                    formatted_date = datetime.fromisoformat(timestamp).strftime("%A, %d %B %Y %H:%M")
                except Exception:
                    formatted_date = timestamp
                
                st.subheader(f"🌤️ {formatted_date}")
                inputs = entry.get("inputs", {})
                
                # Display checkin details
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Mood:** {inputs.get('mood', '')}")
                    st.markdown(f"**Focus:** {inputs.get('focus', '')}")
                with col2:
                    st.markdown(f"**Yesterday's Status:** {inputs.get('yesterday_status', '')}")
                    st.markdown(f"**Today's Task:** {inputs.get('today_task', '')}")
                
                # Show assistant's response
                st.markdown("**🤖 Assistant's Response:**")
                st.markdown(entry.get("response", ""))
                st.markdown("---")

