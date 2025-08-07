import streamlit as st
from setup import load_user_profile

st.set_page_config(
    page_title="Weekly Coach GPT",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🧠 Weekly Coach GPT")
    st.markdown("Your AI-powered personal coach for goal achievement and productivity")
    
    # Check if user has completed setup
    profile = load_user_profile()
    
    if not profile:
        st.warning("👋 Welcome! Let's get you started.")
        st.info("You need to complete the setup first to use the Weekly Coach.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🎯 What is Weekly Coach GPT?")
            st.markdown("""
            - **AI-powered coaching** for your personal and professional goals
            - **Weekly planning** with personalized task breakdowns
            - **Daily check-ins** to stay on track
            - **Progress tracking** with insights and achievements
            - **Reflection tools** to learn from your experiences
            """)
        
        with col2:
            st.markdown("### 🚀 How it works")
            st.markdown("""
            1. **Setup** - Define your main goal and preferences
            2. **Plan** - Generate weekly plans tailored to you
            3. **Check-in** - Daily progress updates and motivation
            4. **Reflect** - Weekly reviews and insights
            5. **Grow** - Track progress and celebrate achievements
            """)
        
        st.markdown("---")
        st.markdown("### 🎬 Ready to start?")
        if st.button("🚀 Begin Setup", type="primary", use_container_width=True):
            st.switch_page("pages/1_Setup.py")
        
        st.markdown("---")
        st.markdown("### 📚 Quick Demo")
        st.markdown("Want to see how it works? Check out the demo features:")
        
        demo_col1, demo_col2, demo_col3 = st.columns(3)
        with demo_col1:
            if st.button("📋 Sample Weekly Plan", use_container_width=True):
                st.switch_page("pages/2_Sample_Plan.py")
        
        with demo_col2:
            if st.button("🌤️ Sample Check-in", use_container_width=True):
                st.switch_page("pages/3_Sample_Checkin.py")
        
        with demo_col3:
            if st.button("📝 Sample Reflection", use_container_width=True):
                st.switch_page("pages/4_Sample_Reflection.py")
    
    else:
        # User has completed setup - show main dashboard
        st.success("✅ Welcome back! You're all set up.")
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🎯 Main Goal", profile.get("goal", "Not set")[:30] + "..." if len(profile.get("goal", "")) > 30 else profile.get("goal", "Not set"))
        
        with col2:
            progress = profile.get("progress", {})
            st.metric("📊 Check-ins", progress.get("total_checkins", 0))
        
        with col3:
            st.metric("📅 Weeks", progress.get("total_weeks", 0))
        
        with col4:
            completion_rate = progress.get("completion_rate", 0)
            st.metric("✅ Progress", f"{completion_rate}%")
        
        st.markdown("---")
        
        # Main navigation
        st.markdown("### 🧭 What would you like to do today?")
        
        nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
        
        with nav_col1:
            if st.button("📋 Create Weekly Plan", use_container_width=True, type="primary"):
                st.switch_page("pages/2_Weekly_Plan.py")
        
        with nav_col2:
            if st.button("🌤️ Daily Check-in", use_container_width=True):
                st.switch_page("pages/3_Daily_Checkin.py")
        
        with nav_col3:
            if st.button("📝 Weekly Reflection", use_container_width=True):
                st.switch_page("pages/4_Reflection.py")
        
        with nav_col4:
            if st.button("📊 View Progress", use_container_width=True):
                st.switch_page("pages/5_Progress.py")
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        quick_col1, quick_col2, quick_col3 = st.columns(3)
        
        with quick_col1:
            if st.button("🔧 Settings", use_container_width=True):
                st.switch_page("pages/6_Settings.py")
        
        with quick_col2:
            if st.button("📚 View History", use_container_width=True):
                st.switch_page("pages/7_History.py")
        
        with quick_col3:
            if st.button("❓ Help & Tips", use_container_width=True):
                st.switch_page("pages/8_Help.py")

if __name__ == "__main__":
    main() 