import streamlit as st
import os
import json
from coach import generate_weekly_reflection, save_weekly_reflection_to_log, update_reflection_history, get_reflection_summary
from datetime import datetime
from setup import load_user_profile

st.set_page_config(page_title="Weekly Reflection", page_icon="📝")

def load_weekly_plans():
    log_path = "logs/weekly_plans.json"
    if not os.path.exists(log_path):
        return []
    try:
        with open(log_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def main():
    st.title("📝 Weekly Reflection")
    st.markdown("Review your week and learn from your experiences")
    
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

    # Get the most recent weekly plan
    logs = load_weekly_plans()
    if not logs:
        st.info("No weekly plan found. Please create a plan first.")
        if st.button("Create Weekly Plan"):
            st.switch_page("pages/2_Weekly_Plan.py")
        return

    latest_plan = logs[-1]["plan"]
    
    st.markdown("### 🤔 How was your week?")
    st.info("Take some time to reflect on your achievements, challenges, and what you've learned.")
    
    with st.form("weekly_reflection_form"):
        achievements = st.text_area(
            "What did you accomplish this week?",
            placeholder="List your main achievements, big or small...",
            help="Celebrate your wins, no matter how small they seem"
        )
        
        challenges = st.text_area(
            "What challenges did you face?",
            placeholder="What was difficult or didn't go as planned?",
            help="Understanding challenges helps us improve future plans"
        )
        
        learnings = st.text_area(
            "What did you learn about yourself?",
            placeholder="Any insights about your work style, motivation, or habits?",
            help="Self-awareness is key to continuous improvement"
        )
        
        next_week_focus = st.text_area(
            "What would you like to focus on next week?",
            placeholder="Any specific areas you want to improve or focus on?",
            help="This helps us create better plans for next week"
        )
        
        overall_rating = st.slider(
            "How would you rate this week overall?",
            min_value=1,
            max_value=10,
            value=7,
            help="1 = Very challenging, 10 = Excellent week"
        )
        
        submitted = st.form_submit_button("📝 Generate Reflection", type="primary")

    if submitted:
        if not achievements.strip():
            st.error("Please share at least one achievement from this week.")
        else:
            with st.spinner("🤔 Analyzing your week and generating insights..."):
                try:
                    reflection = generate_weekly_reflection(
                        goal=profile["goal"],
                        weekly_plan=latest_plan,
                        achievements=achievements,
                        challenges=challenges,
                        learnings=learnings,
                        next_week_focus=next_week_focus,
                        overall_rating=overall_rating
                    )
                    
                    # Save to log
                    save_weekly_reflection_to_log(
                        inputs={
                            "achievements": achievements,
                            "challenges": challenges,
                            "learnings": learnings,
                            "next_week_focus": next_week_focus,
                            "overall_rating": overall_rating
                        },
                        reflection=reflection
                    )
                    
                    # Update reflection history
                    update_reflection_history()
                    
                    st.success("🎉 Your reflection has been saved!")
                    
                    # Display the reflection
                    st.markdown("### 🤖 Your AI Coach's Analysis:")
                    st.markdown(reflection)
                    
                    # Show reflection insights
                    reflection_summary = get_reflection_summary()
                    if reflection_summary:
                        st.markdown("---")
                        st.markdown("### 📊 Reflection Insights")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("📝 Total Reflections", reflection_summary["total_reflections"])
                        with col2:
                            st.metric("🎯 Success Patterns", len(reflection_summary["success_patterns"]))
                        with col3:
                            st.metric("⚠️ Common Challenges", len(reflection_summary["common_challenges"]))
                        
                        if reflection_summary["insights"]:
                            st.markdown("**💡 Key Insights:**")
                            for insight in reflection_summary["insights"][:3]:  # Show top 3
                                st.markdown(f"- {insight}")
                    
                    # Next steps
                    st.markdown("---")
                    st.markdown("### 🚀 What's next?")
                    st.markdown("Great job reflecting on your week! Here are some next steps:")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📋 Create Next Week's Plan"):
                            st.switch_page("pages/2_Weekly_Plan.py")
                    with col2:
                        if st.button("📊 View Progress"):
                            st.switch_page("pages/5_Progress.py")
                    with col3:
                        if st.button("🏠 Back to Dashboard"):
                            st.switch_page("main.py")
                            
                except Exception as e:
                    st.error(f"Sorry, there was an error generating your reflection: {str(e)}")
                    st.info("Please try again or check your internet connection.")

    # Show reflection tips
    st.markdown("---")
    st.markdown("### 💡 Tips for Effective Reflection")
    
    tips_col1, tips_col2 = st.columns(2)
    with tips_col1:
        st.markdown("**🎯 Be Honest**")
        st.markdown("- Honest reflection leads to real growth")
        st.markdown("- Don't judge yourself, just observe")
        
        st.markdown("**📝 Be Specific**")
        st.markdown("- Instead of 'worked hard', say 'completed 3 project milestones'")
        st.markdown("- Specific examples help identify patterns")
    
    with tips_col2:
        st.markdown("**🧠 Look for Patterns**")
        st.markdown("- Notice what works well for you")
        st.markdown("- Identify recurring challenges")
        
        st.markdown("**🎉 Celebrate Wins**")
        st.markdown("- Acknowledge all achievements")
        st.markdown("- Progress is progress, no matter how small")

if __name__ == "__main__":
    main() 