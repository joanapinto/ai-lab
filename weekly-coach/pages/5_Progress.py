import streamlit as st
import os
import json
from coach import get_user_achievements, get_current_week_summary, get_reflection_summary
from setup import load_user_profile

st.set_page_config(page_title="Progress Dashboard", page_icon="📊")

def main():
    st.title("📊 Progress Dashboard")
    st.markdown("Track your journey and celebrate your achievements")
    
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

    # Progress Overview
    if "progress" in profile:
        progress = profile["progress"]
        
        st.markdown("### 📈 Overall Progress")
        
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
        
        # Progress bar for completion rate
        st.progress(completion_rate / 100)
        
        # Weekly completion rates chart
        if progress.get("weekly_completion_rates"):
            st.markdown("**📊 Weekly Completion Trends:**")
            rates = progress["weekly_completion_rates"]
            if len(rates) > 1:
                st.line_chart(rates)
            else:
                st.info("Complete more weeks to see trends")

    # Current Week Summary
    week_summary = get_current_week_summary()
    if week_summary:
        st.markdown("---")
        st.markdown("### 📅 Current Week Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎯 Main Objective", week_summary["main_objective"] or "Not set")
        with col2:
            st.metric("📋 Total Tasks", week_summary["total_tasks"])
        with col3:
            st.metric("✅ Completed", f"{week_summary['completed_tasks']}/{week_summary['total_tasks']}")
        
        # Progress bar for current week
        completion_rate = week_summary["completion_rate"]
        st.progress(completion_rate / 100)
        st.markdown(f"**Progress:** {completion_rate}% complete")
        
        # Daily task status
        if week_summary.get("daily_status"):
            st.markdown("**📋 Daily Task Status:**")
            for day, status in week_summary["daily_status"].items():
                if status == "completed":
                    st.markdown(f"✅ {day}: Completed")
                elif status == "partial":
                    st.markdown(f"🟡 {day}: Partially completed")
                elif status == "not_started":
                    st.markdown(f"⚪ {day}: Not started")
                else:
                    st.markdown(f"❓ {day}: {status}")

    # Achievements
    achievements = get_user_achievements(profile)
    if achievements:
        st.markdown("---")
        st.markdown("### 🏆 Achievements")
        
        achievement_cols = st.columns(3)
        for i, achievement in enumerate(achievements):
            with achievement_cols[i % 3]:
                st.markdown(f"**{achievement['badge']} {achievement['title']}**")
                st.markdown(f"*{achievement['description']}*")
                st.markdown(f"*Unlocked: {achievement['date']}*")
    else:
        st.markdown("---")
        st.markdown("### 🏆 Achievements")
        st.info("Complete more check-ins and plans to unlock achievements!")

    # Reflection Insights
    reflection_summary = get_reflection_summary()
    if reflection_summary and reflection_summary.get("total_reflections", 0) > 0:
        st.markdown("---")
        st.markdown("### 🧠 Reflection Insights")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📝 Total Reflections", reflection_summary["total_reflections"])
        with col2:
            st.metric("🎯 Success Patterns", len(reflection_summary["success_patterns"]))
        with col3:
            st.metric("⚠️ Common Challenges", len(reflection_summary["common_challenges"]))
        
        # Show success patterns
        if reflection_summary.get("success_patterns"):
            st.markdown("**✅ Success Patterns:**")
            for pattern in reflection_summary["success_patterns"][:3]:  # Show top 3
                st.markdown(f"- {pattern}")
        
        # Show common challenges
        if reflection_summary.get("common_challenges"):
            st.markdown("**⚠️ Common Challenges:**")
            for challenge in reflection_summary["common_challenges"][:3]:  # Show top 3
                st.markdown(f"- {challenge}")
        
        # Show key insights
        if reflection_summary.get("insights"):
            st.markdown("**💡 Key Insights:**")
            for insight in reflection_summary["insights"][:3]:  # Show top 3
                st.markdown(f"- {insight}")

    # Quick Actions
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
        if st.button("📚 View History", use_container_width=True):
            st.switch_page("pages/7_History.py")

    # Progress Tips
    st.markdown("---")
    st.markdown("### 💡 Progress Tips")
    
    tips_col1, tips_col2 = st.columns(2)
    with tips_col1:
        st.markdown("**📈 Boost Your Progress**")
        st.markdown("- Check in daily to build momentum")
        st.markdown("- Celebrate small wins")
        st.markdown("- Focus on consistency over perfection")
        
        st.markdown("**🎯 Stay Motivated**")
        st.markdown("- Review your main goal regularly")
        st.markdown("- Track your achievements")
        st.markdown("- Learn from setbacks")
    
    with tips_col2:
        st.markdown("**📊 Understanding Metrics**")
        st.markdown("- **Completion Rate:** Percentage of tasks completed")
        st.markdown("- **Streak Days:** Consecutive days of check-ins")
        st.markdown("- **Total Weeks:** Number of weekly plans created")
        
        st.markdown("**🏆 Achievement System**")
        st.markdown("- Unlock badges for milestones")
        st.markdown("- Each achievement represents progress")
        st.markdown("- Keep checking in to unlock more!")

if __name__ == "__main__":
    main() 