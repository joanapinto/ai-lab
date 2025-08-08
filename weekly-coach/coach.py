import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from datetime import datetime, timedelta
import re

# Load API key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client only if API key is available
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None

# Load the user profile from file
def load_user_profile():
    path = "user_profile.json"
    if not os.path.exists(path):
        raise FileNotFoundError("User profile not found. Please run setup first.")
    with open(path, "r") as f:
        return json.load(f)

# Load the prompt from file
def load_prompt_template(file_path):
    with open(file_path, "r") as file:
        return file.read()

# Load the last reflection
def load_last_reflection():
    try:
        with open("logs/weekly_plans.json", "r") as f:
            data = json.load(f)
        for entry in reversed(data):
            if "reflection" in entry:
                return entry["main_objective"], entry["reflection"]
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return None, None

# Extract the main objective from the plan
def extract_main_objective(plan_text):
    match = re.search(r"🎯 This week's main objective:\s*(.+?)(?:\n|$)", plan_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return "Not specified"

# Generate the weekly plan
def generate_weekly_plan(mood, availability, focus="None"):
    # Load user goal profile
    profile = load_user_profile()
    goal = profile["goal"]
    motivation = profile.get("motivation", "")
    deadline = profile.get("deadline", "None")
    last_objective, reflection = load_last_reflection()

    # Format last week summary if available
    if reflection:
        reflection_summary = (
            f"\nLast week’s goal was: {last_objective}\n"
            f"- Achieved: {'Yes' if reflection['achieved'] else 'No'}\n"
            f"- Notes: {reflection.get('notes', 'None')}\n"
        )
    else:
        reflection_summary = ""

    # Load and format prompt
    template = load_prompt_template("prompts/weekly_plan.txt")
    prompt = template.format(
        goal=goal,
        motivation=motivation,
        deadline=deadline,
        mood=mood,
        availability=availability,
        focus=focus or "None"
    )

    # Final prompt includes reflection
    final_prompt = reflection_summary + prompt

    # GPT call
    if not client:
        raise ValueError("OpenAI API key not set. Please add your API key to the .env file.")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a helpful, supportive career coach."},
            {"role": "user", "content": final_prompt}
        ]
    )
    
    plan = response.choices[0].message.content.strip()
    main_objective = extract_main_objective(plan)

    return plan, main_objective


# Save the plan to the logs
def save_weekly_plan_to_log(inputs, plan, main_objective):
    log_path = "logs/weekly_plans.json"
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "inputs": inputs,
        "plan": plan,
        "main_objective": main_objective
    }

    # Load existing logs
    try:
        with open(log_path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(entry)

    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)

# Generate the weekly reflection
def generate_weekly_reflection(goal, motivation, deadline, last_week_plan, objective_achieved, notes):
    template = load_prompt_template("prompts/weekly_reflection.txt")

    prompt = template.format(
        goal=goal,
        motivation=motivation,
        deadline=deadline,
        last_week_plan=last_week_plan,
        objective_achieved=objective_achieved,
        notes=notes
    )

    if not client:
        raise ValueError("OpenAI API key not set. Please add your API key to the .env file.")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a supportive career coach."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

# Save the reflection to the logs
def save_weekly_reflection_to_log(inputs, reflection):
    log_path = "logs/weekly_reflections.json"
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "inputs": inputs,
        "reflection": reflection
    }

    # Load existing logs
    try:
        with open(log_path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(entry)

    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)

def regenerate_weekly_plan(goal, motivation, deadline, last_plan, objective_achieved, notes):
    template = load_prompt_template("prompts/regen_plan.txt")

    prompt = template.format(
        goal=goal,
        motivation=motivation,
        deadline=deadline,
        last_plan=last_plan,
        objective_achieved=objective_achieved,
        notes=notes
    )

    if not client:
        raise ValueError("OpenAI API key not set. Please add your API key to the .env file.")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful coach adapting a weekly plan."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

def daily_checkin(goal, motivation, weekly_plan, day, yesterday_task, yesterday_status, mood, focus, today_task):
    template = load_prompt_template("prompts/daily_checkin.txt")

    prompt = template.format(
        goal=goal,
        motivation=motivation,
        weekly_plan=weekly_plan,
        day=day,
        yesterday_task=yesterday_task,
        yesterday_status=yesterday_status,
        mood=mood,
        focus=focus or "None",
        today_task=today_task
    )

    if not client:
        raise ValueError("OpenAI API key not set. Please add your API key to the .env file.")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a positive daily assistant helping someone stay on track."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

# Save daily checkin to logs
def save_daily_checkin_to_log(inputs, response):
    log_path = "logs/daily_checkins.json"
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "inputs": inputs,
        "response": response
    }

    # Load existing logs
    try:
        with open(log_path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(entry)

    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)

# Progress tracking functions
def update_user_progress():
    """Update user progress based on daily checkins and weekly plans"""
    profile = load_user_profile()
    if not profile:
        return
    
    # Load daily checkins
    try:
        with open("logs/daily_checkins.json", "r") as f:
            checkins = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        checkins = []
    
    # Load weekly plans
    try:
        with open("logs/weekly_plans.json", "r") as f:
            plans = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        plans = []
    
    # Calculate progress metrics
    total_checkins = len(checkins)
    total_weeks = len(plans)
    
    # Calculate completion rate from recent checkins
    recent_checkins = checkins[-7:] if len(checkins) >= 7 else checkins
    completed_tasks = sum(1 for c in recent_checkins if c['inputs'].get('yesterday_status') in ['Yes', 'Partially'])
    completion_rate = (completed_tasks / len(recent_checkins)) * 100 if recent_checkins else 0
    
    # Calculate streak
    streak_days = 0
    last_checkin_date = None
    if checkins:
        last_checkin = checkins[-1]
        last_checkin_date = last_checkin['timestamp']
        
        # Count consecutive days with checkins
        current_date = datetime.now()
        for i in range(len(checkins) - 1, -1, -1):
            checkin_date = datetime.fromisoformat(checkins[i]['timestamp'])
            days_diff = (current_date - checkin_date).days
            
            if days_diff == streak_days:
                streak_days += 1
            else:
                break
    
    # Update profile
    if "progress" not in profile:
        profile["progress"] = {}
    
    profile["progress"].update({
        "total_weeks": total_weeks,
        "total_checkins": total_checkins,
        "completion_rate": round(completion_rate, 1),
        "streak_days": streak_days,
        "last_checkin_date": last_checkin_date
    })
    
    # Save updated profile
    with open("user_profile.json", "w") as f:
        json.dump(profile, f, indent=2)

def get_user_achievements(profile):
    """Get user achievements based on progress"""
    achievements = []
    progress = profile.get("progress", {})
    
    # Check for various achievements
    if progress.get("total_checkins", 0) >= 7:
        achievements.append({
            "badge": "🎯",
            "title": "Week Warrior",
            "description": "Completed 7 daily check-ins",
            "date": datetime.now().strftime("%Y-%m-%d")
        })
    
    if progress.get("streak_days", 0) >= 5:
        achievements.append({
            "badge": "🔥",
            "title": "Streak Master",
            "description": "5+ day check-in streak",
            "date": datetime.now().strftime("%Y-%m-%d")
        })
    
    if progress.get("completion_rate", 0) >= 80:
        achievements.append({
            "badge": "✅",
            "title": "High Achiever",
            "description": "80%+ task completion rate",
            "date": datetime.now().strftime("%Y-%m-%d")
        })
    
    if progress.get("total_weeks", 0) >= 4:
        achievements.append({
            "badge": "📅",
            "title": "Monthly Planner",
            "description": "Completed 4 weeks of planning",
            "date": datetime.now().strftime("%Y-%m-%d")
        })
    
    return achievements

# Weekly plan context management
def update_current_week_context(plan_text, main_objective):
    """Update the current week context in user profile"""
    profile = load_user_profile()
    if not profile:
        return
    
    # Extract daily tasks from plan
    daily_tasks = {}
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for day in days:
        task = extract_task_for_day(plan_text, day)
        if task and task != "Not found":
            daily_tasks[day] = task
    
    # Get current week start (Monday)
    today = datetime.now()
    days_since_monday = today.weekday()
    week_start = today - timedelta(days=days_since_monday)
    
    # Update current week context
    if "current_week" not in profile:
        profile["current_week"] = {}
    
    profile["current_week"].update({
        "week_start": week_start.strftime("%Y-%m-%d"),
        "main_objective": main_objective,
        "daily_tasks": daily_tasks,
        "completion_status": {},
        "last_updated": datetime.now().isoformat()
    })
    
    # Save updated profile
    with open("user_profile.json", "w") as f:
        json.dump(profile, f, indent=2)

def extract_task_for_day(plan_text, day):
    """Extract task for a specific day from plan text"""
    patterns = [
        f"- **{day}:**",
        f"- {day}:",
        f"**{day}:**",
        f"{day}:",
        f"- {day}",
    ]
    
    lines = plan_text.splitlines()
    for i, line in enumerate(lines):
        line = line.strip()
        for pattern in patterns:
            if line.startswith(pattern):
                # Get the task from the current line
                task = line.replace(pattern, "").strip()
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

def update_task_completion_status(day, status):
    """Update completion status for a specific day"""
    profile = load_user_profile()
    if not profile or "current_week" not in profile:
        return
    
    if "completion_status" not in profile["current_week"]:
        profile["current_week"]["completion_status"] = {}
    
    profile["current_week"]["completion_status"][day] = {
        "status": status,
        "completed_at": datetime.now().isoformat()
    }
    
    # Save updated profile
    with open("user_profile.json", "w") as f:
        json.dump(profile, f, indent=2)

def get_current_week_summary():
    """Get a summary of the current week's progress"""
    profile = load_user_profile()
    if not profile or "current_week" not in profile:
        return None
    
    current_week = profile["current_week"]
    completion_status = current_week.get("completion_status", {})
    
    # Calculate completion stats
    total_tasks = len(current_week.get("daily_tasks", {}))
    completed_tasks = sum(1 for status in completion_status.values() 
                         if status.get("status") in ["Yes", "Partially"])
    
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    return {
        "main_objective": current_week.get("main_objective"),
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": round(completion_rate, 1),
        "daily_tasks": current_week.get("daily_tasks", {}),
        "completion_status": completion_status
    }

# Reflection history analysis
def update_reflection_history(reflection_data):
    """Update reflection history with new reflection data"""
    profile = load_user_profile()
    if not profile:
        return
    
    # Load past reflections
    try:
        with open("logs/weekly_reflections.json", "r") as f:
            reflections = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        reflections = []
    
    # Update reflection stats
    if "reflections" not in profile:
        profile["reflections"] = {}
    
    profile["reflections"].update({
        "total_reflections": len(reflections),
        "last_reflection_date": datetime.now().isoformat()
    })
    
    # Analyze patterns if we have enough reflections
    if len(reflections) >= 2:
        analyze_reflection_patterns(profile, reflections)
    
    # Save updated profile
    with open("user_profile.json", "w") as f:
        json.dump(profile, f, indent=2)

def analyze_reflection_patterns(profile, reflections):
    """Analyze reflection patterns and extract insights"""
    challenges = []
    successes = []
    goals = []
    
    # Extract patterns from recent reflections (last 5)
    recent_reflections = reflections[-5:] if len(reflections) >= 5 else reflections
    
    for reflection in recent_reflections:
        inputs = reflection.get("inputs", {})
        reflection_text = reflection.get("reflection", "")
        
        # Track goal achievement patterns
        objective_achieved = inputs.get("objective_achieved", "")
        if objective_achieved in ["No", "Partially"]:
            challenges.append({
                "type": "goal_achievement",
                "frequency": 1,
                "notes": inputs.get("notes", "")
            })
        elif objective_achieved == "Yes":
            successes.append({
                "type": "goal_achievement",
                "frequency": 1,
                "notes": inputs.get("notes", "")
            })
    
    # Update profile with insights
    profile["reflections"].update({
        "common_challenges": challenges[-3:],  # Keep last 3 challenges
        "success_patterns": successes[-3:],    # Keep last 3 successes
        "goal_evolution": goals[-3:]           # Keep last 3 goal changes
    })
    
    # Generate insights
    insights = generate_insights(profile, reflections)
    profile["reflections"]["insights"] = insights

def generate_insights(profile, reflections):
    """Generate insights based on reflection history"""
    insights = []
    
    if len(reflections) < 2:
        return insights
    
    # Analyze completion patterns
    recent_reflections = reflections[-3:]  # Last 3 reflections
    completion_rates = []
    
    for reflection in recent_reflections:
        inputs = reflection.get("inputs", {})
        objective_achieved = inputs.get("objective_achieved", "")
        
        if objective_achieved == "Yes":
            completion_rates.append(100)
        elif objective_achieved == "Partially":
            completion_rates.append(50)
        else:
            completion_rates.append(0)
    
    avg_completion = sum(completion_rates) / len(completion_rates)
    
    # Generate insights based on patterns
    if avg_completion >= 80:
        insights.append("🎯 You're consistently achieving your goals! Keep up the great work.")
    elif avg_completion >= 50:
        insights.append("📈 You're making steady progress. Consider breaking down larger goals into smaller tasks.")
    else:
        insights.append("💡 You might benefit from setting more achievable goals or adjusting your approach.")
    
    # Check for consistency
    if len(reflections) >= 4:
        insights.append("📅 You're building a great habit of weekly reflection!")
    
    # Check for recent improvements
    if len(completion_rates) >= 2:
        if completion_rates[-1] > completion_rates[-2]:
            insights.append("🚀 You're improving! Your recent performance is better than before.")
    
    return insights

def get_reflection_summary():
    """Get a summary of reflection history and insights"""
    profile = load_user_profile()
    if not profile or "reflections" not in profile:
        return None
    
    reflections = profile["reflections"]
    
    return {
        "total_reflections": reflections.get("total_reflections", 0),
        "last_reflection_date": reflections.get("last_reflection_date"),
        "common_challenges": reflections.get("common_challenges", []),
        "success_patterns": reflections.get("success_patterns", []),
        "insights": reflections.get("insights", [])
    }
