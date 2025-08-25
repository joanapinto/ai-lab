import streamlit as st
import os
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add the parent directory to the Python path to find the data module
current_file = Path(__file__)
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from data.storage import save_user_profile, load_user_profile, save_mood_data, load_mood_data, save_all_mood_data, delete_mood_entry

st.set_page_config(page_title="Focus Companion - Mood Tracker", page_icon="😊", layout="wide")
st.title("😊 Mood Tracker")

# Load user profile
user_profile = load_user_profile()

if not user_profile:
    st.warning("Please complete onboarding first!")
    if st.button("🚀 Go to Onboarding", use_container_width=True):
        st.switch_page("pages/onboarding.py")
else:
    # Load existing mood data from persistent storage
    mood_data = load_mood_data()
    
    # Initialize session state for mood data
    if 'mood_data' not in st.session_state:
        st.session_state.mood_data = mood_data
    else:
        # Sync session state with persistent data
        st.session_state.mood_data = mood_data
    
    # Sidebar for quick mood logging
    with st.sidebar:
        st.header("📝 Quick Mood Log")
        
        current_mood = st.selectbox(
            "How are you feeling right now?",
            ["😊 Happy", "😌 Calm", "😤 Stressed", "😴 Tired", "😡 Angry", 
             "😔 Sad", "😰 Anxious", "🤗 Excited", "😐 Neutral", "😎 Confident"]
        )
        
        mood_intensity = st.slider("Intensity (1-10)", 1, 10, 5)
        
        mood_note = st.text_area("Any notes? (Optional)", height=100)
        
        if st.button("💾 Log Mood", use_container_width=True):
            new_mood = {
                "timestamp": datetime.now().isoformat(),
                "mood": current_mood,
                "intensity": mood_intensity,
                "note": mood_note,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": datetime.now().strftime("%H:%M")
            }
            # Save to persistent storage
            save_mood_data(new_mood)
            # Update session state
            st.session_state.mood_data.append(new_mood)
            st.success("Mood logged! 📊")
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📈 Mood History")
        
        if st.session_state.mood_data:
            # Convert to DataFrame for analysis
            df = pd.DataFrame(st.session_state.mood_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = pd.to_datetime(df['date'])
            
            # Mood trend over time
            fig_trend = px.line(
                df, 
                x='timestamp', 
                y='intensity',
                title="Mood Intensity Over Time",
                labels={'intensity': 'Mood Intensity', 'timestamp': 'Time'},
                markers=True
            )
            fig_trend.update_layout(height=400)
            st.plotly_chart(fig_trend, use_container_width=True)
            
            # Mood distribution
            mood_counts = df['mood'].value_counts()
            fig_dist = px.pie(
                values=mood_counts.values,
                names=mood_counts.index,
                title="Mood Distribution"
            )
            fig_dist.update_layout(height=400)
            st.plotly_chart(fig_dist, use_container_width=True)
            
        else:
            st.info("No mood data yet. Start logging your moods in the sidebar! 📝")
    
    with col2:
        st.header("📊 Quick Stats")
        
        if st.session_state.mood_data:
            df = pd.DataFrame(st.session_state.mood_data)
            
            # Today's average mood
            today = datetime.now().strftime("%Y-%m-%d")
            today_moods = df[df['date'] == today]
            
            if not today_moods.empty:
                avg_intensity = today_moods['intensity'].mean()
                st.metric("Today's Average Mood", f"{avg_intensity:.1f}/10")
                
                most_common_mood = today_moods['mood'].mode().iloc[0] if not today_moods['mood'].mode().empty else "No data"
                st.metric("Most Common Mood Today", most_common_mood)
            else:
                st.metric("Today's Average Mood", "No data yet")
                st.metric("Most Common Mood Today", "No data yet")
            
            # Weekly average
            week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            week_moods = df[df['date'] >= week_ago]
            
            if not week_moods.empty:
                weekly_avg = week_moods['intensity'].mean()
                st.metric("Weekly Average", f"{weekly_avg:.1f}/10")
            else:
                st.metric("Weekly Average", "No data yet")
        
        st.header("🎯 Mood Goals")
        st.write("Track your emotional wellness and identify patterns!")
        
        # Mood insights
        if st.session_state.mood_data and len(st.session_state.mood_data) > 5:
            st.success("💡 **Insight**: You've been tracking for a while! Keep it up!")
        elif st.session_state.mood_data:
            st.info("💡 **Tip**: Log your mood regularly to see patterns emerge!")
        else:
            st.warning("💡 **Start**: Begin by logging your first mood!")
    
    # Recent mood entries
    st.header("📝 Recent Entries")
    
    if st.session_state.mood_data:
        # Show last 10 entries
        recent_data = st.session_state.mood_data[-10:][::-1]  # Reverse to show newest first
        
        for entry in recent_data:
            with st.expander(f"{entry['mood']} - {entry['date']} {entry['time']} (Intensity: {entry['intensity']}/10)"):
                if entry['note']:
                    st.write(f"**Note:** {entry['note']}")
                else:
                    st.write("*No notes added*")
                
                # Add delete button
                if st.button(f"🗑️ Delete", key=f"delete_{entry['timestamp']}"):
                    # Remove from persistent storage
                    delete_mood_entry(entry['timestamp'])
                    # Remove from session state
                    st.session_state.mood_data.remove(entry)
                    st.rerun()
    else:
        st.info("No mood entries yet. Start logging in the sidebar! 📝")
    
    # Export functionality
    if st.session_state.mood_data:
        st.header("📤 Export Data")
        
        if st.button("📊 Export Mood Data as JSON"):
            # Create export data
            export_data = {
                "export_date": datetime.now().isoformat(),
                "user_goal": user_profile.get('goal', 'Not set'),
                "mood_entries": st.session_state.mood_data
            }
            
            # Convert to JSON string
            json_str = json.dumps(export_data, indent=2)
            
            # Create download button
            st.download_button(
                label="💾 Download JSON",
                data=json_str,
                file_name=f"mood_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            ) 