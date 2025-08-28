import streamlit as st
import os
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
from io import StringIO

# Add the parent directory to the Python path to find the data module
current_file = Path(__file__)
project_root = current_file.parent.parent
sys.path.insert(0, str(project_root))

from data.storage import save_user_profile, load_user_profile, load_mood_data, load_checkin_data
from auth import require_beta_access

st.set_page_config(page_title="Focus Companion - Mood Journal", page_icon="📖", layout="wide")

# Require beta access
require_beta_access()

st.title("📖 Mood Journal")

# Load user profile
user_profile = load_user_profile()

if not user_profile:
    st.warning("Please complete onboarding first!")
    if st.button("🚀 Go to Onboarding", use_container_width=True):
        st.switch_page("pages/onboarding.py")
else:
    # Load all data
    mood_data = load_mood_data()
    checkin_data = load_checkin_data()
    
    # Combine and process data
    all_entries = []
    
    # Add mood entries
    for entry in mood_data:
        entry['type'] = 'mood'
        entry['display_date'] = datetime.fromisoformat(entry['timestamp']).strftime("%B %d, %Y")
        entry['display_time'] = datetime.fromisoformat(entry['timestamp']).strftime("%I:%M %p")
        all_entries.append(entry)
    
    # Add check-in entries
    for entry in checkin_data:
        entry['type'] = 'checkin'
        entry['display_date'] = datetime.fromisoformat(entry['timestamp']).strftime("%B %d, %Y")
        entry['display_time'] = datetime.fromisoformat(entry['timestamp']).strftime("%I:%M %p")
        all_entries.append(entry)
    
    # Sort by timestamp (newest first)
    all_entries.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Sidebar for filtering
    with st.sidebar:
        st.header("🔍 Filters")
        
        # Date range filter
        st.subheader("📅 Date Range")
        if all_entries:
            dates = [datetime.fromisoformat(entry['timestamp']).date() for entry in all_entries]
            min_date = min(dates)
            max_date = max(dates)
            
            date_range = st.date_input(
                "Select date range",
                value=(max_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
        else:
            date_range = None
        
        # Entry type filter
        st.subheader("📝 Entry Type")
        entry_types = st.multiselect(
            "Filter by type",
            options=['mood', 'checkin'],
            default=['mood', 'checkin']
        )
        
        # Mood filter (for mood entries)
        st.subheader("😊 Mood Filter")
        if mood_data:
            mood_options = list(set([entry['mood'] for entry in mood_data]))
            selected_moods = st.multiselect(
                "Filter by mood",
                options=mood_options,
                default=mood_options
            )
        else:
            selected_moods = []
        
        # Time period filter
        st.subheader("⏰ Time Period")
        time_period = st.selectbox(
            "Filter by time period",
            options=['All time', 'Last 7 days', 'Last 30 days', 'Last 90 days'],
            index=0
        )
        
        # Clear filters button
        if st.button("🗑️ Clear All Filters", use_container_width=True):
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("📚 Your Journal Entries")
        
        if not all_entries:
            st.info("📝 No journal entries yet. Start by logging your mood or completing daily check-ins!")
        else:
            # Apply filters
            filtered_entries = all_entries.copy()
            
            # Date range filter
            if date_range and len(date_range) == 2:
                start_date, end_date = date_range
                filtered_entries = [
                    entry for entry in filtered_entries
                    if start_date <= datetime.fromisoformat(entry['timestamp']).date() <= end_date
                ]
            
            # Entry type filter
            filtered_entries = [entry for entry in filtered_entries if entry['type'] in entry_types]
            
            # Mood filter
            if selected_moods:
                filtered_entries = [
                    entry for entry in filtered_entries
                    if entry['type'] != 'mood' or entry['mood'] in selected_moods
                ]
            
            # Time period filter
            if time_period != 'All time':
                days_map = {
                    'Last 7 days': 7,
                    'Last 30 days': 30,
                    'Last 90 days': 90
                }
                days = days_map[time_period]
                cutoff_date = datetime.now() - timedelta(days=days)
                filtered_entries = [
                    entry for entry in filtered_entries
                    if datetime.fromisoformat(entry['timestamp']) >= cutoff_date
                ]
            
            # Display entries
            if not filtered_entries:
                st.info("🔍 No entries match your current filters. Try adjusting your filter settings.")
            else:
                st.write(f"📊 Showing {len(filtered_entries)} of {len(all_entries)} total entries")
                
                # Group entries by date
                entries_by_date = {}
                for entry in filtered_entries:
                    date_key = entry['display_date']
                    if date_key not in entries_by_date:
                        entries_by_date[date_key] = []
                    entries_by_date[date_key].append(entry)
                
                # Display entries grouped by date
                for date, day_entries in entries_by_date.items():
                    with st.expander(f"📅 {date} ({len(day_entries)} entries)", expanded=True):
                        for entry in day_entries:
                            with st.container():
                                col1, col2, col3 = st.columns([1, 3, 1])
                                
                                with col1:
                                    if entry['type'] == 'mood':
                                        st.write(f"😊 **{entry['mood']}**")
                                        st.write(f"Intensity: {entry['intensity']}/10")
                                    else:
                                        st.write(f"📝 **{entry['time_period'].title()} Check-in**")
                                
                                with col2:
                                    if entry['type'] == 'mood':
                                        if entry.get('note'):
                                            st.write(f"*{entry['note']}*")
                                        else:
                                            st.write("*No notes added*")
                                    else:
                                        # Display check-in details
                                        if entry['time_period'] == 'morning':
                                            st.write(f"Sleep: {entry.get('sleep_quality', 'N/A')}")
                                            st.write(f"Focus: {entry.get('focus_today', 'N/A')}")
                                            st.write(f"Energy: {entry.get('energy_level', 'N/A')}")
                                        elif entry['time_period'] == 'afternoon':
                                            st.write(f"Progress: {entry.get('day_progress', 'N/A')}")
                                            if entry.get('adjust_plan'):
                                                st.write(f"Plan adjustment: {entry['adjust_plan']}")
                                            st.write(f"Break: {entry.get('take_break', 'N/A')}")
                                        else:  # evening
                                            if entry.get('accomplishments'):
                                                st.write(f"Accomplishments: {entry['accomplishments']}")
                                            if entry.get('challenges'):
                                                st.write(f"Challenges: {entry['challenges']}")
                                            st.write(f"Feeling: {entry.get('current_feeling', 'N/A')}")
                                
                                with col3:
                                    st.write(f"🕐 {entry['display_time']}")
                                    st.write(f"📋 {entry['type'].title()}")
                                
                                st.divider()
    
    with col2:
        st.header("📊 Quick Stats")
        
        if all_entries:
            # Calculate stats
            total_entries = len(all_entries)
            mood_entries = len([e for e in all_entries if e['type'] == 'mood'])
            checkin_entries = len([e for e in all_entries if e['type'] == 'checkin'])
            
            # Date range
            dates = [datetime.fromisoformat(entry['timestamp']).date() for entry in all_entries]
            date_range_days = (max(dates) - min(dates)).days + 1
            
            # Average entries per day
            avg_per_day = total_entries / date_range_days if date_range_days > 0 else 0
            
            # Display stats
            st.metric("Total Entries", total_entries)
            st.metric("Mood Entries", mood_entries)
            st.metric("Check-in Entries", checkin_entries)
            st.metric("Avg Entries/Day", f"{avg_per_day:.1f}")
            
            # Most common mood
            if mood_data:
                mood_counts = {}
                for entry in mood_data:
                    mood = entry['mood']
                    mood_counts[mood] = mood_counts.get(mood, 0) + 1
                
                if mood_counts:
                    most_common_mood = max(mood_counts, key=mood_counts.get)
                    st.metric("Most Common Mood", most_common_mood)
            
            # Recent activity
            recent_entries = [e for e in all_entries 
                            if datetime.fromisoformat(e['timestamp']) > datetime.now() - timedelta(days=7)]
            st.metric("Last 7 Days", len(recent_entries))
        
        st.header("📤 Export Options")
        
        if all_entries:
            # Export as JSON
            if st.button("📄 Export as JSON", use_container_width=True):
                export_data = {
                    "export_date": datetime.now().isoformat(),
                    "user_goal": user_profile.get('goal', 'Not set'),
                    "total_entries": len(all_entries),
                    "entries": all_entries
                }
                
                json_str = json.dumps(export_data, indent=2)
                
                st.download_button(
                    label="💾 Download JSON",
                    data=json_str,
                    file_name=f"mood_journal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            # Export as CSV
            if st.button("📊 Export as CSV", use_container_width=True):
                # Convert to DataFrame for CSV export
                df_data = []
                for entry in all_entries:
                    row = {
                        'Date': entry['display_date'],
                        'Time': entry['display_time'],
                        'Type': entry['type'].title(),
                        'Timestamp': entry['timestamp']
                    }
                    
                    if entry['type'] == 'mood':
                        row.update({
                            'Mood': entry['mood'],
                            'Intensity': entry['intensity'],
                            'Note': entry.get('note', '')
                        })
                    else:
                        row.update({
                            'Time Period': entry['time_period'],
                            'Details': json.dumps(entry, indent=2)
                        })
                    
                    df_data.append(row)
                
                df = pd.DataFrame(df_data)
                csv = df.to_csv(index=False)
                
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name=f"mood_journal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        st.header("💡 Tips")
        st.info("""
        **Journal Tips:**
        - Review your patterns regularly
        - Look for mood and productivity correlations
        - Celebrate your consistency
        - Share insights with your therapist or coach
        """) 