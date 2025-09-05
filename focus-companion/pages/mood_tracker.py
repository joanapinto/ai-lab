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
from auth import require_beta_access, get_user_email

st.set_page_config(page_title="Humsy - Mood Tracker", page_icon="😊", layout="wide")

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

# Require beta access
require_beta_access()

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
    
    # Quick Mood Log Section - Beautifully aligned above graphs
    st.write("---")
    
    # Create a beautiful mood logging form with better styling
    with st.container():
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; 
                    border-radius: 15px; 
                    color: white; 
                    margin-bottom: 20px;">
            <h3 style="color: white; margin-bottom: 15px;">📝 Quick Mood Log</h3>
            <p style="color: rgba(255,255,255,0.9); margin-bottom: 0;">How are you feeling right now? Take a moment to check in with yourself.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Form in columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Multiple mood selection
            mood_options = ["😊 Happy", "😌 Calm", "😤 Stressed", "😴 Tired", "😡 Angry", 
                           "😔 Sad", "😰 Anxious", "🤗 Excited", "😐 Neutral", "💪 Confident"]
            
            selected_moods = st.multiselect(
                "How are you feeling right now? (Select all that apply)",
                mood_options,
                help="You can select multiple moods if you're feeling mixed emotions"
            )
        
        with col2:
            st.write("")  # Spacer for alignment
            if st.button("💾 Log Mood", use_container_width=True, type="primary", help="Save your current mood"):
                if selected_moods:
                    new_mood = {
                        "timestamp": datetime.now().isoformat(),
                        "moods": selected_moods,  # Now stores multiple moods
                        "note": "",  # No note for simple mood logging
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "time": datetime.now().strftime("%H:%M")
                    }
                    # Save to persistent storage
                    save_mood_data(new_mood)
                    # Update session state
                    st.session_state.mood_data.append(new_mood)
                    st.success("🎉 Mood logged successfully! 📊")
                    st.rerun()
                else:
                    st.error("Please select at least one mood!")
            
            # Note about detailed logging
            if selected_moods:
                st.info("💡 **Tip**: Use 'Log Mood with Reasons' below for detailed tracking with reasons and notes!")
    
    # What made you feel that way section
    if selected_moods:
        st.write("---")
        st.subheader("💭 What made you feel that way?")
        
        # Define predefined options for each mood
        mood_reasons = {
            "😊 Happy": [
                "Time with friends/family", "A win or achievement", "Good weather", 
                "Laughter/fun", "Self-care", "Relaxed moment", "Gratitude", 
                "Feeling loved", "Productive day", "Other (free text)"
            ],
            "😌 Calm": [
                "Time in nature", "Yoga/meditation", "Unplugged from phone", 
                "Journaling", "Slow morning", "Reading or music", "Clean/organized space", 
                "Deep breath / pause", "No deadlines", "Other (free text)"
            ],
            "😤 Stressed": [
                "Too many tasks", "Work pressure", "Conflict or tension", 
                "Unclear expectations", "No time for rest", "Financial concerns", 
                "Tech overload", "Feeling behind", "Other (free text)"
            ],
            "😴 Tired": [
                "Poor sleep", "Overworking", "No breaks today", "Low energy day", 
                "Bad nutrition", "Social exhaustion", "Overthinking", 
                "Hormonal cycle", "Other (free text)"
            ],
            "😡 Angry": [
                "Argument or conflict", "Feeling misunderstood", "Unfair treatment", 
                "Traffic or delays", "Injustice", "Self-criticism", 
                "Expectations not met", "Other (free text)"
            ],
            "😔 Sad": [
                "Feeling alone", "Disappointment", "Loss or grief", "Unkind words", 
                "Low self-esteem", "Bad news", "Comparing myself", 
                "Feeling stuck", "Other (free text)"
            ],
            "😰 Anxious": [
                "Upcoming event", "Fear of failure", "Uncertainty", "Social pressure", 
                "Health worries", "Overthinking", "No control", 
                "Financial stress", "Other (free text)"
            ],
            "🤗 Excited": [
                "Upcoming plan/trip", "New idea", "Good news", "Doing what I love", 
                "Seeing someone I care about", "Feeling inspired", "Achievement unlocked", 
                "Creative flow", "Other (free text)"
            ],
            "😐 Neutral": [
                "Routine day", "No strong emotions", "Just okay", "Not much happening", 
                "Lack of stimulation", "Focused on tasks", "Zoned out", "Other (free text)"
            ],
            "💪 Confident": [
                "Spoke my mind", "Solved a problem", "Took care of myself", "Completed a task", 
                "Got recognition", "Learned something new", "Made a decision", 
                "Stuck to a boundary", "Other (free text)"
            ]
        }
        
        # Create columns for each selected mood
        cols = st.columns(len(selected_moods))
        
        for i, mood in enumerate(selected_moods):
            with cols[i]:
                st.write(f"**{mood}**")
                
                # Get predefined options for this mood
                reasons = mood_reasons.get(mood, ["Other (free text)"])
                
                # Create multiselect for reasons
                selected_reasons = st.multiselect(
                    "Reasons:",
                    reasons,
                    key=f"reasons_{mood}_{i}"
                )
                
                # Add custom reason input if "Other" is selected
                if "Other (free text)" in selected_reasons:
                    custom_reason = st.text_input(
                        "Custom reason:",
                        key=f"custom_{mood}_{i}",
                        placeholder="What else made you feel this way?"
                    )
                    if custom_reason.strip():
                        selected_reasons.remove("Other (free text)")
                        selected_reasons.append(custom_reason.strip())
                
                # Store reasons in session state for this mood
                if f"mood_reasons_{mood}_{i}" not in st.session_state:
                    st.session_state[f"mood_reasons_{mood}_{i}"] = []
                st.session_state[f"mood_reasons_{mood}_{i}"] = selected_reasons
        
        # Update the mood data with reasons when logging
        if st.button("💾 Log Mood with Reasons", use_container_width=True, type="secondary"):
            if selected_moods:
                # Collect all reasons for all selected moods
                all_reasons = {}
                for i, mood in enumerate(selected_moods):
                    mood_key = f"mood_reasons_{mood}_{i}"
                    if mood_key in st.session_state:
                        all_reasons[mood] = st.session_state[mood_key]
                
                new_mood = {
                    "timestamp": datetime.now().isoformat(),
                    "moods": selected_moods,
                    "reasons": all_reasons,  # Store reasons for each mood
                    "note": "",  # Note will be added if user fills it out
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": datetime.now().strftime("%H:%M")
                }
                
                # Save to persistent storage
                save_mood_data(new_mood)
                # Update session state
                st.session_state.mood_data.append(new_mood)
                st.success("🎉 Mood and reasons logged successfully! 📊")
                
                st.rerun()
    
    # Optional note field for detailed mood logging
    if selected_moods:
        st.write("")  # Spacer
        mood_note = st.text_area(
            "💭 Any additional thoughts or notes? (Optional)", 
            height=80,
            placeholder="How was your day? What influenced your mood? Any specific events?",
            help="Add context to help you understand your mood patterns better"
        )
        
        # Add note to the most recent mood entry if provided
        if mood_note.strip() and st.session_state.mood_data:
            if st.button("📝 Add Note to Last Entry", type="secondary"):
                # Update the most recent mood entry with the note
                latest_entry = st.session_state.mood_data[-1]
                latest_entry['note'] = mood_note.strip()
                # Update in persistent storage
                save_mood_data(latest_entry)
                st.info("📝 Note added to your latest mood entry!")
                st.rerun()
    
    st.write("---")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Mood History")
        
        if st.session_state.mood_data:
            # Process mood data to handle both old and new formats
            processed_data = []
            for entry in st.session_state.mood_data:
                # Handle both old format (single mood) and new format (multiple moods)
                if 'moods' in entry and entry['moods']:
                    # New format: multiple moods
                    for mood in entry['moods']:
                        processed_entry = entry.copy()
                        processed_entry['mood'] = mood
                        del processed_entry['moods']  # Remove the moods list
                        processed_data.append(processed_entry)
                elif 'mood' in entry:
                    # Old format: single mood
                    processed_data.append(entry)
                else:
                    # Fallback for malformed data
                    processed_entry = entry.copy()
                    processed_entry['mood'] = 'Unknown'
                    processed_data.append(processed_entry)
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(processed_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = pd.to_datetime(df['date'])
            df_expanded = df
            
            # Mood distribution
            mood_counts = df_expanded['mood'].value_counts()
            
            # Define beautiful colors for different moods
            mood_colors = {
                "😊 Happy": "#FFD700",      # Gold
                "😌 Calm": "#87CEEB",       # Sky Blue
                "😤 Stressed": "#FF6B6B",   # Coral Red
                "😴 Tired": "#9370DB",      # Medium Purple
                "😡 Angry": "#DC143C",      # Crimson
                "😔 Sad": "#4169E1",        # Royal Blue
                "😰 Anxious": "#FF8C00",    # Dark Orange
                "🤗 Excited": "#32CD32",    # Lime Green
                "😐 Neutral": "#808080",    # Gray
                "💪 Confident": "#FF1493"   # Deep Pink
            }
            
            # Create color list for the pie chart
            colors = [mood_colors.get(mood, "#CCCCCC") for mood in mood_counts.index]
            
            fig_dist = px.pie(
                values=mood_counts.values,
                names=mood_counts.index,
                title="📊 Your Mood Distribution",
                color_discrete_sequence=colors,
                hole=0.3  # Create a donut chart
            )
            
            # Improve styling
            fig_dist.update_layout(
                height=450,
                font=dict(size=12),
                title_font=dict(size=18, color="#2E86AB"),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.01
                ),
                margin=dict(l=20, r=20, t=50, b=20)
            )
            
            # Improve text formatting
            fig_dist.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont_size=11,
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )
            
            st.plotly_chart(fig_dist, use_container_width=True)
            
            # Mood frequency over time
            mood_time_data = df_expanded.groupby([df_expanded['date'].dt.date, 'mood']).size().reset_index(name='count')
            mood_time_data['date'] = pd.to_datetime(mood_time_data['date'])
            
            # Create the line chart with improved styling
            fig_trend = px.line(
                mood_time_data,
                x='date',
                y='count',
                color='mood',
                title="📈 Mood Frequency Over Time",
                labels={'count': 'Number of Times Felt', 'date': 'Date'},
                markers=True,
                color_discrete_map=mood_colors  # Use the same color scheme
            )
            
            # Improve styling
            fig_trend.update_layout(
                height=450,
                font=dict(size=12),
                title_font=dict(size=18, color="#2E86AB"),
                xaxis=dict(
                    title_font=dict(size=14, color="#2E86AB"),
                    tickfont=dict(size=11),
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True
                ),
                yaxis=dict(
                    title_font=dict(size=14, color="#2E86AB"),
                    tickfont=dict(size=11),
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True
                ),
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.01,
                    font=dict(size=10)
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=50, b=20)
            )
            
            # Improve line and marker styling
            fig_trend.update_traces(
                line=dict(width=3),
                marker=dict(size=8, line=dict(width=2, color='white')),
                hovertemplate='<b>%{fullData.name}</b><br>Date: %{x}<br>Count: %{y}<extra></extra>'
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
            
            # Reasons analysis if available
            if 'reasons' in df.columns and df['reasons'].notna().any():
                st.write("---")
                st.subheader("🔍 What's Making You Feel This Way?")
                
                # Collect all reasons across all entries
                all_reasons = []
                for entry in st.session_state.mood_data:
                    if 'reasons' in entry and entry['reasons']:
                        for mood, reasons in entry['reasons'].items():
                            if reasons:
                                all_reasons.extend(reasons)
                
                if all_reasons:
                    # Count reason frequency
                    reason_counts = pd.Series(all_reasons).value_counts().head(10)
                    
                    # Create a beautiful gradient color scheme for the bar chart
                    import numpy as np
                    colors = px.colors.qualitative.Set3[:len(reason_counts)]
                    
                    fig_reasons = px.bar(
                        x=reason_counts.values,
                        y=reason_counts.index,
                        orientation='h',
                        title="🔍 Top 10 Reasons for Your Moods",
                        labels={'x': 'Frequency', 'y': 'Reason'},
                        color=reason_counts.values,
                        color_continuous_scale='Viridis'
                    )
                    
                    # Improve styling
                    fig_reasons.update_layout(
                        height=450,
                        font=dict(size=12),
                        title_font=dict(size=18, color="#2E86AB"),
                        xaxis=dict(
                            title_font=dict(size=14, color="#2E86AB"),
                            tickfont=dict(size=11),
                            gridcolor='rgba(128,128,128,0.2)',
                            showgrid=True
                        ),
                        yaxis=dict(
                            title_font=dict(size=14, color="#2E86AB"),
                            tickfont=dict(size=11),
                            categoryorder='total ascending'
                        ),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=20, r=20, t=50, b=20),
                        showlegend=False
                    )
                    
                    # Improve bar styling
                    fig_reasons.update_traces(
                        hovertemplate='<b>%{y}</b><br>Frequency: %{x}<extra></extra>',
                        marker=dict(
                            line=dict(width=1, color='white'),
                            opacity=0.8
                        )
                    )
                    
                    st.plotly_chart(fig_reasons, use_container_width=True)
                    
                    # Show insights
                    st.write("**💡 Insights:**")
                    st.write(f"• Most common reason: **{reason_counts.index[0]}** ({reason_counts.iloc[0]} times)")
                    if len(reason_counts) > 1:
                        st.write(f"• Second most common: **{reason_counts.index[1]}** ({reason_counts.iloc[1]} times)")
                    
                    # Mood-reason correlation
                    st.write("**🎯 Mood-Reason Patterns:**")
                    mood_reason_pairs = []
                    for entry in st.session_state.mood_data:
                        if 'reasons' in entry and entry['reasons']:
                            for mood, reasons in entry['reasons'].items():
                                for reason in reasons:
                                    mood_reason_pairs.append((mood, reason))
                    
                    if mood_reason_pairs:
                        mood_reason_df = pd.DataFrame(mood_reason_pairs, columns=['mood', 'reason'])
                        mood_reason_counts = mood_reason_df.groupby(['mood', 'reason']).size().reset_index(name='count')
                        mood_reason_counts = mood_reason_counts.sort_values('count', ascending=False).head(5)
                        
                        for _, row in mood_reason_counts.iterrows():
                            st.write(f"• **{row['mood']}** often comes from: **{row['reason']}** ({row['count']} times)")
            
        else:
            st.info("No mood data yet. Start logging your moods above! 📝")
    
    with col2:
        st.header("📊 Quick Stats")
        
        if st.session_state.mood_data:
            df = pd.DataFrame(st.session_state.mood_data)
            
            # Handle multiple moods for stats
            if 'moods' in df.columns:
                # Drop the old 'mood' column if it exists to avoid conflicts
                if 'mood' in df.columns:
                    df = df.drop(columns=['mood'])
                df_expanded = df.explode('moods')
                df_expanded = df_expanded.rename(columns={'moods': 'mood'})
            else:
                df_expanded = df.copy()
                if 'mood' not in df_expanded.columns:
                    df_expanded['mood'] = 'Unknown'
            
            # Today's mood stats
            today = datetime.now().strftime("%Y-%m-%d")
            today_moods = df_expanded[df_expanded['date'] == today]
            
            if not today_moods.empty:
                total_moods_today = len(today_moods)
                st.metric("Moods Logged Today", total_moods_today)
                
                # Get the most common mood, ensuring we get a scalar value
                # First, clean the data by removing NaN values
                clean_moods = today_moods['mood'].dropna()
                if not clean_moods.empty:
                    # Get the most common mood
                    mode_result = clean_moods.mode()
                    if not mode_result.empty:
                        most_common_mood = mode_result.iloc[0]
                    else:
                        most_common_mood = "No data"
                else:
                    most_common_mood = "No data"
                st.metric("Most Common Mood Today", most_common_mood)
            else:
                st.metric("Moods Logged Today", "No data yet")
                st.metric("Most Common Mood Today", "No data yet")
            
            # Weekly stats
            week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            week_moods = df_expanded[df_expanded['date'] >= week_ago]
            
            if not week_moods.empty:
                total_weekly_moods = len(week_moods)
                st.metric("Moods This Week", total_weekly_moods)
            else:
                st.metric("Moods This Week", "No data yet")
        
        st.header("🎯 Mood Goals")
        st.write("Track your emotional wellness and identify patterns!")
        
        # Mood insights
        if st.session_state.mood_data and len(st.session_state.mood_data) > 5:
            st.success("💡 **Insight**: You've been tracking for a while! Keep it up!")
            if 'reasons' in st.session_state.mood_data[0]:
                st.info("💡 **New Feature**: You can now track what makes you feel each way!")
        elif st.session_state.mood_data:
            st.info("💡 **Tip**: Log your mood regularly to see patterns emerge!")
        else:
            st.warning("💡 **Start**: Begin by logging your first mood!")
    
    # Recent mood entries
    st.subheader("📝 Recent Entries")
    
    if st.session_state.mood_data:
        # Show last 10 entries
        recent_data = st.session_state.mood_data[-10:][::-1]  # Reverse to show newest first
        
        for entry in recent_data:
            # Handle both old format (single mood) and new format (multiple moods)
            if 'moods' in entry:
                mood_display = ", ".join(entry['moods'])
                title = f"{mood_display} - {entry['date']} {entry['time']}"
            else:
                mood_display = entry.get('mood', 'Unknown')
                title = f"{mood_display} - {entry['date']} {entry['time']}"
            
            with st.expander(title):
                # Show reasons if available
                if 'reasons' in entry and entry['reasons']:
                    st.write("**What made you feel this way:**")
                    for mood, reasons in entry['reasons'].items():
                        if reasons:
                            st.write(f"• {mood}: {', '.join(reasons)}")
                
                # Show note if available
                if entry.get('note'):
                    st.write(f"**Note:** {entry['note']}")
                
                # Add delete button
                if st.button(f"🗑️ Delete", key=f"delete_{entry['timestamp']}"):
                    # Remove from persistent storage
                    delete_mood_entry(entry['timestamp'])
                    # Remove from session state
                    st.session_state.mood_data.remove(entry)
                    st.rerun()
    else:
        st.info("No mood entries yet. Start logging above! 📝")
    
    # Export functionality
    if st.session_state.mood_data:
        st.subheader("📤 Export Data")
        
        if st.button("📊 Export Mood Data as JSON"):
            # Create export data
            export_data = {
                "export_date": datetime.now().isoformat(),
                "user_goal": user_profile.get('goal', 'Not set'),
                "mood_entries": st.session_state.mood_data,
                "export_note": "Data includes multiple moods per entry and reasons for each mood"
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