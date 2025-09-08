"""
Profile Page for Humsy
User profile management, goals, and feedback
"""

import streamlit as st
from auth import require_beta_access, get_user_email
from data.storage import load_user_profile, save_user_profile
from datetime import datetime

# Require beta access
require_beta_access()

# Set page config
st.set_page_config(
    page_title="Humsy - Profile",
    page_icon="👤",
    layout="wide"
)

# Hide Streamlit's default navigation
hide_streamlit_navigation = """
<style>
    /* Hide the automatic pages navigation */
    .stSidebar > div:first-child > div:first-child > div:nth-child(2) {
        display: none;
    }
    
    /* Hide the default page navigation */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Hide any remaining automatic navigation */
    .css-1544g2n {
        display: none;
    }
</style>
"""
st.markdown(hide_streamlit_navigation, unsafe_allow_html=True)

# Custom navigation sidebar
with st.sidebar:
    st.subheader("🧭 Navigation")
    
    # Main pages
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("👤 Profile", use_container_width=True):
        st.switch_page("pages/profile.py")
    
    if st.button("📝 Daily Check-in", use_container_width=True):
        st.switch_page("pages/daily_checkin.py")
    
    if st.button("😊 Mood Tracker", use_container_width=True):
        st.switch_page("pages/mood_tracker.py")
    
    if st.button("🌱 Weekly Reflection", use_container_width=True):
        st.switch_page("pages/reflection.py")
    
    if st.button("📊 Insights", use_container_width=True):
        st.switch_page("pages/history.py")
    
    st.write("---")
    
    # Admin insights access
    user_email = get_user_email()
    if user_email == "joanapnpinto@gmail.com":
        st.subheader("🔓 Admin Tools")
        if st.button("📊 Database Insights", use_container_width=True):
            st.switch_page("pages/insights.py")
    
    st.write("---")
    
    # Logout
    if st.button("🚪 Logout", use_container_width=True):
        from auth import logout
        logout()

def main():
    st.title("👤 Your Profile")
    
    # Get user email and profile
    user_email = get_user_email()
    user_profile = load_user_profile()
    
    if not user_profile:
        st.warning("No profile found. Please complete onboarding first.")
        if st.button("🚀 Go to Onboarding"):
            st.switch_page("pages/onboarding.py")
        return
    
    # Profile Overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Profile Information")
        st.write(f"**Email:** {user_email}")
        
        # Member since date
        member_since = user_profile.get('created_at', user_profile.get('member_since'))
        if member_since:
            try:
                # Try to parse the date if it's a string
                if isinstance(member_since, str):
                    from datetime import datetime
                    parsed_date = datetime.fromisoformat(member_since.replace('Z', '+00:00'))
                    formatted_date = parsed_date.strftime("%B %d, %Y")
                else:
                    formatted_date = str(member_since)
                st.write(f"**Member since:** {formatted_date}")
            except:
                st.write(f"**Member since:** {member_since}")
        else:
            st.write("**Member since:** Unknown")
        
        # Current situation
        st.write("---")
        st.subheader("🎯 Current Situation")
        situation = user_profile.get('situation', 'Not specified')
        situation_other = user_profile.get('situation_other', '')
        
        if situation == "Other" and situation_other:
            current_situation = situation_other
        else:
            current_situation = situation
            
        st.write(f"**How would you describe your current situation?**")
        st.info(current_situation)
    
    with col2:
        st.subheader("📊 Quick Stats")
        # Add some quick stats here if available
        st.info("Profile statistics coming soon!")
    
    # Editable Goal Section
    st.write("---")
    st.subheader("🎯 Your Goal")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        current_goal = user_profile.get('goal', 'Not set')
        st.write(f"**Current Goal:** {current_goal}")
    
    with col2:
        if st.button("✏️ Edit Goal", use_container_width=True):
            st.session_state.editing_goal = True
    
    # Goal editing form
    if st.session_state.get('editing_goal', False):
        with st.form("goal_edit_form"):
            new_goal = st.text_area(
                "What's your main goal?",
                value=current_goal if current_goal != 'Not set' else "",
                placeholder="e.g., Improve focus and productivity, Better work-life balance, Reduce stress...",
                height=100
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Save Goal", use_container_width=True):
                    if new_goal.strip():
                        user_profile['goal'] = new_goal.strip()
                        save_user_profile(user_profile)
                        st.success("✅ Goal updated successfully!")
                        st.session_state.editing_goal = False
                        st.rerun()
                    else:
                        st.error("Please enter a goal")
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.editing_goal = False
                    st.rerun()
    
    # Onboarding Answers (Editable)
    st.write("---")
    st.subheader("📝 Your Onboarding Answers")
    
    # Energy drainers
    st.write("**What drains your energy?**")
    energy_drainers = user_profile.get('energy_drainers', [])
    energy_drainer_other = user_profile.get('energy_drainer_other', '')
    
    if energy_drainers:
        for drainer in energy_drainers:
            st.write(f"• {drainer}")
        if energy_drainer_other:
            st.write(f"• {energy_drainer_other}")
    else:
        st.info("No energy drainers specified")
    
    # Energy boosters (joy sources)
    st.write("**What gives you energy?**")
    joy_sources = user_profile.get('joy_sources', [])
    joy_other = user_profile.get('joy_other', '')
    
    if joy_sources:
        for source in joy_sources:
            st.write(f"• {source}")
        if joy_other:
            st.write(f"• {joy_other}")
    else:
        st.info("No energy sources specified")
    
    # Stress triggers (using energy drainers as stress indicators)
    st.write("**What stresses you out?**")
    if energy_drainers:
        for drainer in energy_drainers:
            st.write(f"• {drainer}")
        if energy_drainer_other:
            st.write(f"• {energy_drainer_other}")
    else:
        st.info("No stress triggers specified")
    
    # Edit onboarding answers button
    if st.button("✏️ Edit Onboarding Answers", use_container_width=True):
        st.switch_page("pages/onboarding.py")
    
    # Feedback Section
    st.write("---")
    st.subheader("💬 Help Us Improve Humsy")
    st.write("Your feedback is invaluable for making Humsy better! 🚀")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Give Feedback", use_container_width=True):
            st.markdown("""
            ### 📝 We'd love your feedback!
            
            Please take a moment to share your thoughts about Humsy:
            
            **[📋 Open Feedback Form](https://tally.so/r/mBr11Q)**
            
            Your feedback helps us make the app better for everyone! 🚀
            """)
    
    with col2:
        if st.button("🐛 Report Bug", use_container_width=True):
            st.markdown("**[🐛 Open Bug Report Form](https://tally.so/r/waR7Eq)**")
            st.info("🐛 **Bug Report**\n\nPlease detail step by step how to reproduce the bug. Include:\n- What you were trying to do\n- What happened instead\n- Steps to reproduce")
    
    with col3:
        if st.button("💡 Suggest Feature", use_container_width=True):
            st.info("💡 **Feature Request**\n\nGreat idea! Please use the feedback form above and describe:\n- What feature you'd like\n- Why it would be helpful\n- How you'd use it")
    
    # Beta Tester Guide
    st.write("---")
    st.subheader("📋 Beta Tester Guide")
    if st.button("📋 View Beta Guide", use_container_width=True):
        st.markdown("""
        ### 🚀 **Beta Tester Guide**
        
        **🎯 Quick Start:**
        1. **Complete your onboarding** - Set your goals and preferences first!
        2. **Start with a time-aware check-in** - Morning, afternoon, or evening based on current time
        3. **Track your mood** - Build patterns and insights
        4. **Try the AI features** - Personalized analysis and tips
        5. **Explore weekly reflections** - Learn from your patterns
        
        **💡 Pro Tips:**
        - **Be consistent** - Daily check-ins build the most valuable insights
        - **Use the AI features** - They get smarter with your data
        - **Don't worry about perfection** - Just log how you're feeling
        - **Try different times** - Morning, afternoon, and evening check-ins
        
        **🤖 AI Features:**
        - **Personalized greetings** - AI that knows your patterns
        - **Smart task planning** - Based on your energy and goals
        - **Usage limits** - 20 AI calls per day, 400 per month
        - **Graceful fallback** - Works perfectly even without AI
        
        **⚠️ Beta Expectations:**
        - This is a **beta version** - some things might change
        - **AI features** have usage limits to control costs
        - **Data is saved locally** - your privacy is protected
        - **Updates** will add new features based on your feedback
        
        **🎁 Beta Perks:**
        - **Early access** to new features
        - **Direct influence** on development
        - **Priority support** for issues
        - **Exclusive insights** into the development process
        """)

if __name__ == "__main__":
    main()
