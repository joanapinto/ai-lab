import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path
from datetime import datetime, timedelta
import calendar

# Add the parent directory to the Python path to find the data module
current_file = Path(__file__)
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from data.storage import load_user_profile, load_mood_data, load_checkin_data
from assistant.logic import FocusAssistant
from assistant.fallback import FallbackAssistant

st.set_page_config(page_title="Focus Companion - History & Analytics", page_icon="📊", layout="wide")
st.title("📊 Your History & Analytics")

# Load user profile and data
user_profile = load_user_profile()
mood_data = load_mood_data()
checkin_data = load_checkin_data()

if not user_profile:
    st.warning("Please complete onboarding first!")
    if st.button("🚀 Go to Onboarding", use_container_width=True):
        st.switch_page("pages/onboarding.py")
else:
    # Initialize assistants
    assistant = FocusAssistant(user_profile, mood_data, checkin_data)
    fallback_assistant = FallbackAssistant(user_profile, mood_data, checkin_data)
    
    # Sidebar for navigation and filters
    st.sidebar.title("🎛️ Analytics Dashboard")
    
    # Time period filter
    time_period = st.sidebar.selectbox(
        "📅 Time Period",
        ["Last 7 days", "Last 30 days", "Last 90 days", "All time"],
        index=0
    )
    
    # Data type filter
    data_type = st.sidebar.multiselect(
        "📊 Data Types",
        ["Mood Tracking", "Daily Check-ins", "Sleep Quality", "Energy Levels", "Focus Goals"],
        default=["Mood Tracking", "Daily Check-ins"]
    )
    
    # Quick stats in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 Quick Stats")
    
    if mood_data:
        total_mood_entries = len(mood_data)
        st.sidebar.metric("Mood Entries", total_mood_entries)
        
        if mood_data:
            avg_intensity = sum(entry.get('intensity', 0) for entry in mood_data) / len(mood_data)
            st.sidebar.metric("Avg Mood Intensity", f"{avg_intensity:.1f}/10")
    
    if checkin_data:
        total_checkins = len(checkin_data)
        st.sidebar.metric("Check-ins", total_checkins)
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "😊 Mood Analytics", "📝 Check-in History", "🎯 Insights"])
    
    with tab1:
        st.header("📊 Overview Dashboard")
        
        # User profile summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("👤 Your Profile")
            st.write(f"**Goal:** {user_profile.get('goal', 'Not set')}")
            st.write(f"**Availability:** {user_profile.get('availability', 'Not set')}")
            st.write(f"**Energy Level:** {user_profile.get('energy', 'Not set')}")
            st.write(f"**Situation:** {user_profile.get('situation', 'Not set')}")
            
            # Display joy sources
            joy_sources = user_profile.get('joy_sources', [])
            if joy_sources:
                st.write(f"**Joy Sources:** {', '.join(joy_sources)}")
            
            # Display energy drainers
            energy_drainers = user_profile.get('energy_drainers', [])
            if energy_drainers:
                st.write(f"**Energy Drainers:** {', '.join(energy_drainers)}")
            
            # Display small habit if applicable
            small_habit = user_profile.get('small_habit', '')
            if small_habit:
                st.write(f"**Small Habit Goal:** {small_habit}")
        
        with col2:
            st.subheader("📈 Activity Summary")
            st.write(f"**Total Mood Entries:** {len(mood_data)}")
            st.write(f"**Total Check-ins:** {len(checkin_data)}")
            
            # Calculate unique days more accurately
            mood_dates = set(entry.get('date', '') for entry in mood_data)
            checkin_dates = set()
            for entry in checkin_data:
                try:
                    checkin_date = datetime.fromisoformat(entry.get('timestamp', '')).date()
                    checkin_dates.add(str(checkin_date))
                except:
                    pass
            all_dates = mood_dates.union(checkin_dates)
            st.write(f"**Days Active:** {len(all_dates)}")
        
        with col3:
            st.subheader("🎯 Current Status")
            if mood_data:
                latest_mood = mood_data[-1] if mood_data else None
                if latest_mood:
                    st.write(f"**Latest Mood:** {latest_mood.get('mood', 'N/A')}")
                    st.write(f"**Intensity:** {latest_mood.get('intensity', 'N/A')}/10")
                    st.write(f"**Date:** {latest_mood.get('date', 'N/A')}")
        
        # Recent activity timeline
        st.subheader("⏰ Recent Activity Timeline")
        
        if mood_data or checkin_data:
            # Combine and sort recent activity
            all_activity = []
            
            for entry in mood_data:
                all_activity.append({
                    'timestamp': entry.get('timestamp', ''),
                    'type': 'Mood',
                    'title': f"{entry.get('mood', 'Mood')} ({entry.get('intensity', 0)}/10)",
                    'description': entry.get('note', ''),
                    'date': entry.get('date', ''),
                    'time': entry.get('time', '')
                })
            
            for entry in checkin_data:
                try:
                    timestamp = datetime.fromisoformat(entry.get('timestamp', ''))
                    all_activity.append({
                        'timestamp': entry.get('timestamp', ''),
                        'type': 'Check-in',
                        'title': f"{entry.get('time_period', 'Check-in').title()} Check-in",
                        'description': entry.get('focus_today', entry.get('accomplishments', '')),
                        'date': timestamp.strftime('%Y-%m-%d'),
                        'time': timestamp.strftime('%H:%M')
                    })
                except:
                    pass
            
            # Sort by timestamp
            all_activity.sort(key=lambda x: x['timestamp'], reverse=True)
            
            # Display recent activity
            for activity in all_activity[:10]:  # Show last 10 activities
                with st.expander(f"{activity['type']} - {activity['title']} ({activity['date']} {activity['time']})"):
                    st.write(f"**Description:** {activity['description']}")
                    if activity['type'] == 'Mood':
                        st.write(f"**Mood:** {activity['title']}")
                    else:
                        st.write(f"**Type:** {activity['title']}")
        else:
            st.info("No activity data available yet. Start tracking your mood and check-ins to see your history here!")
    
    with tab2:
        st.header("😊 Mood Analytics")
        
        if mood_data:
            # Convert to DataFrame for analysis
            df = pd.DataFrame(mood_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = pd.to_datetime(df['date'])
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.day_name()
            df['month'] = df['timestamp'].dt.month_name()
            
            # Filter by time period
            if time_period == "Last 7 days":
                cutoff_date = datetime.now() - timedelta(days=7)
                df = df[df['timestamp'] >= cutoff_date]
            elif time_period == "Last 30 days":
                cutoff_date = datetime.now() - timedelta(days=30)
                df = df[df['timestamp'] >= cutoff_date]
            elif time_period == "Last 90 days":
                cutoff_date = datetime.now() - timedelta(days=90)
                df = df[df['timestamp'] >= cutoff_date]
            
            # Mood trend over time
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Mood Trend Over Time")
                if not df.empty:
                    fig = px.line(df, x='timestamp', y='intensity', 
                                title='Mood Intensity Over Time',
                                labels={'intensity': 'Mood Intensity', 'timestamp': 'Date'})
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No mood data available for the selected time period.")
            
            with col2:
                st.subheader("😊 Mood Distribution")
                if not df.empty:
                    mood_counts = df['mood'].value_counts()
                    fig = px.pie(values=mood_counts.values, names=mood_counts.index,
                               title='Mood Distribution')
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No mood data available for the selected time period.")
            
            # Mood patterns analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📅 Mood by Day of Week")
                if not df.empty:
                    day_avg = df.groupby('day_of_week')['intensity'].mean().reindex([
                        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
                    ])
                    fig = px.bar(x=day_avg.index, y=day_avg.values,
                               title='Average Mood by Day of Week',
                               labels={'x': 'Day of Week', 'y': 'Average Mood Intensity'})
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No mood data available for the selected time period.")
            
            with col2:
                st.subheader("🕐 Mood by Time of Day")
                if not df.empty:
                    hour_avg = df.groupby('hour')['intensity'].mean()
                    fig = px.bar(x=hour_avg.index, y=hour_avg.values,
                               title='Average Mood by Hour of Day',
                               labels={'x': 'Hour of Day', 'y': 'Average Mood Intensity'})
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No mood data available for the selected time period.")
            
            # Mood insights
            st.subheader("🧠 Mood Insights")
            
            if not df.empty:
                # Calculate insights
                avg_mood = df['intensity'].mean()
                best_day = df.groupby('day_of_week')['intensity'].mean().idxmax()
                worst_day = df.groupby('day_of_week')['intensity'].mean().idxmin()
                best_hour = df.groupby('hour')['intensity'].mean().idxmax()
                worst_hour = df.groupby('hour')['intensity'].mean().idxmin()
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Average Mood", f"{avg_mood:.1f}/10")
                
                with col2:
                    st.metric("Best Day", best_day)
                
                with col3:
                    st.metric("Worst Day", worst_day)
                
                with col4:
                    st.metric("Peak Hour", f"{best_hour}:00")
                
                # Mood recommendations
                st.subheader("💡 Mood Recommendations")
                
                if avg_mood < 5:
                    st.info("Your average mood is on the lower side. Consider activities that boost your mood!")
                elif avg_mood > 7:
                    st.success("Great job maintaining a positive mood! Keep up the good work!")
                else:
                    st.info("Your mood is in a good range. Focus on maintaining this balance!")
                
                # Get AI insights
                mood_analysis = assistant.analyze_mood_patterns()
                if mood_analysis.get('insights'):
                    st.subheader("🤖 AI Mood Insights")
                    for insight in mood_analysis['insights']:
                        st.write(f"• {insight}")
        else:
            st.info("No mood data available yet. Start tracking your mood to see analytics here!")
    
    with tab3:
        st.header("📝 Check-in History")
        
        if checkin_data:
            # Convert to DataFrame
            df_checkins = pd.DataFrame(checkin_data)
            df_checkins['timestamp'] = pd.to_datetime(df_checkins['timestamp'])
            df_checkins['date'] = df_checkins['timestamp'].dt.date
            
            # Filter by time period
            if time_period == "Last 7 days":
                cutoff_date = datetime.now().date() - timedelta(days=7)
                df_checkins = df_checkins[df_checkins['date'] >= cutoff_date]
            elif time_period == "Last 30 days":
                cutoff_date = datetime.now().date() - timedelta(days=30)
                df_checkins = df_checkins[df_checkins['date'] >= cutoff_date]
            elif time_period == "Last 90 days":
                cutoff_date = datetime.now().date() - timedelta(days=90)
                df_checkins = df_checkins[df_checkins['date'] >= cutoff_date]
            
            # Check-in patterns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Check-in Frequency")
                if not df_checkins.empty:
                    daily_checkins = df_checkins.groupby('date').size()
                    fig = px.bar(x=daily_checkins.index, y=daily_checkins.values,
                               title='Daily Check-ins',
                               labels={'x': 'Date', 'y': 'Number of Check-ins'})
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No check-in data available for the selected time period.")
            
            with col2:
                st.subheader("⏰ Check-in Times")
                if not df_checkins.empty:
                    time_period_counts = df_checkins['time_period'].value_counts()
                    fig = px.pie(values=time_period_counts.values, names=time_period_counts.index,
                               title='Check-ins by Time Period')
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No check-in data available for the selected time period.")
            
            # Sleep and energy analysis
            if 'sleep_quality' in df_checkins.columns or 'energy_level' in df_checkins.columns:
                st.subheader("😴 Sleep & Energy Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'sleep_quality' in df_checkins.columns:
                        sleep_data = df_checkins[df_checkins['sleep_quality'].notna()]
                        if not sleep_data.empty:
                            sleep_counts = sleep_data['sleep_quality'].value_counts()
                            fig = px.bar(x=sleep_counts.index, y=sleep_counts.values,
                                       title='Sleep Quality Distribution',
                                       labels={'x': 'Sleep Quality', 'y': 'Count'})
                            fig.update_layout(height=300)
                            st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    if 'energy_level' in df_checkins.columns:
                        energy_data = df_checkins[df_checkins['energy_level'].notna()]
                        if not energy_data.empty:
                            energy_counts = energy_data['energy_level'].value_counts()
                            fig = px.bar(x=energy_counts.index, y=energy_counts.values,
                                       title='Energy Level Distribution',
                                       labels={'x': 'Energy Level', 'y': 'Count'})
                            fig.update_layout(height=300)
                            st.plotly_chart(fig, use_container_width=True)
            
            # Recent check-ins table
            st.subheader("📋 Recent Check-ins")
            
            if not df_checkins.empty:
                # Get available columns dynamically
                available_columns = ['timestamp', 'time_period']
                
                # Add optional columns if they exist
                optional_columns = ['focus_today', 'energy_level', 'sleep_quality', 'day_progress', 'accomplishments', 'current_feeling']
                for col in optional_columns:
                    if col in df_checkins.columns:
                        available_columns.append(col)
                
                # Prepare data for display
                display_data = df_checkins[available_columns].copy()
                display_data['timestamp'] = display_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
                display_data = display_data.fillna('N/A')
                
                st.dataframe(display_data, use_container_width=True)
            else:
                st.info("No check-in data available for the selected time period.")
        else:
            st.info("No check-in data available yet. Start your daily check-ins to see history here!")
    
    with tab4:
        st.header("🎯 AI-Powered Insights")
        
        # Get comprehensive insights
        if mood_data or checkin_data:
            st.subheader("🧠 Your Personal Insights")
            
            # Weekly summary
            weekly_summary = assistant.get_weekly_summary()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Mood Entries", weekly_summary.get('mood_entries', 0))
                st.metric("Check-in Entries", weekly_summary.get('checkin_entries', 0))
            
            with col2:
                st.metric("Mood Trend", weekly_summary.get('mood_trend', 'N/A'))
                st.metric("Best Day", weekly_summary.get('best_day', 'N/A'))
            
            # AI insights
            if weekly_summary.get('insights'):
                st.subheader("💡 AI Insights")
                for insight in weekly_summary['insights']:
                    st.write(f"• {insight}")
            
            if weekly_summary.get('recommendations'):
                st.subheader("🎯 Recommendations")
                for rec in weekly_summary['recommendations']:
                    st.write(f"• {rec}")
            
            # Personalized greeting and tips
            st.subheader("🌟 Daily Motivation")
            st.write(fallback_assistant.get_personalized_greeting())
            st.write(fallback_assistant.get_daily_encouragement())
            
            # Goal progress
            st.subheader("🎯 Goal Progress")
            st.write(f"**Your Goal:** {user_profile.get('goal', 'Not set')}")
            st.write(fallback_assistant.get_goal_reminder())
            
            # Productivity tips
            st.subheader("⚡ Productivity Tips")
            st.write(fallback_assistant.get_productivity_tip())
            
            # Wellness reminder
            st.subheader("💚 Wellness Reminder")
            st.write(fallback_assistant.get_wellness_reminder())
        else:
            st.info("Complete your first mood entry or check-in to receive personalized insights!")
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Daily Check-in", use_container_width=True):
            st.switch_page("pages/daily_checkin.py")
    
    with col2:
        if st.button("😊 Mood Tracker", use_container_width=True):
            st.switch_page("pages/mood_tracker.py")
    
    with col3:
        if st.button("🤔 Reflection", use_container_width=True):
            st.switch_page("pages/reflection.py") 