import streamlit as st
import os
import json
from coach import generate_weekly_plan, save_weekly_plan_to_log, update_user_progress, update_current_week_context
from datetime import datetime, timedelta
from setup import load_user_profile

st.set_page_config(page_title="Weekly Plan", page_icon="📋")

def main():
    st.title("📋 Create Weekly Plan")
    st.markdown("Generate a personalized plan for this week")
    
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

    # Current Week Summary
    from coach import get_current_week_summary
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
        
        st.markdown("---")

    # Weekly plan form
    st.markdown("### 🚀 Create New Weekly Plan")
    st.info("Tell us about your week ahead and we'll create a personalized plan for you.")
    
    with st.form("weekly_plan_form"):
        mood = st.text_input("How are you feeling this week?", placeholder="e.g. motivated, tired, excited, stressed", help="Your mood helps us adjust the plan's tone and intensity")
        availability = st.text_input("How much time do you have each day?", placeholder="e.g. 2 hours, 4 hours, flexible", help="This helps us plan realistic tasks")
        focus = st.text_input("Any particular focus for this week?", placeholder="e.g. learning Python, building a project, improving health", help="Optional - helps us prioritize specific areas")

        submitted = st.form_submit_button("🔮 Generate Plan", type="primary")

    if submitted:
        if not mood.strip() or not availability.strip():
            st.error("Please fill in your mood and availability.")
        else:
            with st.spinner("🤔 Creating your personalized weekly plan..."):
                try:
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
                    
                    st.success("🎉 Your weekly plan is ready!")
                    
                    # Display the plan
                    st.markdown("### 📋 Your Weekly Plan")
                    st.markdown(plan)
                    
                    # Next steps
                    st.markdown("---")
                    st.markdown("### 🎯 What's next?")
                    st.markdown("1. **Start your daily check-ins** - Track your progress each day")
                    st.markdown("2. **Review your plan** - Check off tasks as you complete them")
                    st.markdown("3. **Stay motivated** - Your AI coach will help you stay on track")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🌤️ Start Daily Check-in"):
                            st.switch_page("pages/3_Daily_Checkin.py")
                    with col2:
                        if st.button("📊 View Progress"):
                            st.switch_page("pages/5_Progress.py")
                            
                except Exception as e:
                    st.error(f"Sorry, there was an error generating your plan: {str(e)}")
                    st.info("Please try again or check your internet connection.")

    # Show tips for better planning
    st.markdown("---")
    st.markdown("### 💡 Tips for Better Planning")
    
    tips_col1, tips_col2 = st.columns(2)
    with tips_col1:
        st.markdown("**🎯 Be Specific**")
        st.markdown("- Instead of 'work on project', try 'build the login feature'")
        st.markdown("- Break large goals into smaller, actionable tasks")
        
        st.markdown("**⏰ Be Realistic**")
        st.markdown("- Consider your actual available time")
        st.markdown("- Account for meetings, breaks, and unexpected events")
    
    with tips_col2:
        st.markdown("**📝 Track Progress**")
        st.markdown("- Use daily check-ins to stay accountable")
        st.markdown("- Celebrate small wins along the way")
        
        st.markdown("**🔄 Stay Flexible**")
        st.markdown("- Plans can be adjusted as needed")
        st.markdown("- Focus on progress, not perfection")

if __name__ == "__main__":
    main() 