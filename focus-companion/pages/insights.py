"""
Database Insights Page for Focus Companion
Shows analytics and insights from user data
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.insights import DatabaseInsights
from auth import get_user_email

def main():
    st.set_page_config(
        page_title="Database Insights - Focus Companion",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Database Insights")
    st.write("Analytics and insights from your Focus Companion data")
    
    # Get user email
    user_email = get_user_email()
    if not user_email:
        st.error("Please log in to view insights")
        return
    
    # Restrict access to admin email only
    ADMIN_EMAIL = "joanapnpinto@gmail.com"
    if user_email != ADMIN_EMAIL:
        st.error("🔒 **Access Restricted**")
        st.write("Database insights are only available to administrators during beta testing.")
        st.write("If you need access to your personal data, please contact the development team.")
        return
    
    # Initialize insights
    insights = DatabaseInsights()
    
    # Sidebar for options
    st.sidebar.header("📊 Analysis Options")
    
    # Time period selection
    days = st.sidebar.selectbox(
        "Time Period",
        [7, 30, 90, 365],
        index=1,
        format_func=lambda x: f"Last {x} days"
    )
    
    # Analysis type
    analysis_type = st.sidebar.radio(
        "Analysis Type",
        ["Your Data", "Global Overview", "Cost Analysis", "Feature Adoption"]
    )
    
    # Main content
    if analysis_type == "Your Data":
        show_user_insights(insights, user_email, days)
    elif analysis_type == "Global Overview":
        show_global_insights(insights, days)
    elif analysis_type == "Cost Analysis":
        show_cost_analysis(insights, days)
    elif analysis_type == "Feature Adoption":
        show_feature_adoption(insights, days)

def show_user_insights(insights, user_email, days):
    """Show insights for a specific user"""
    st.header(f"👤 Your Insights ({days} days)")
    
    user_data = insights.get_user_activity_summary(user_email, days)
    
    # Engagement metrics
    col1, col2, col3, col4 = st.columns(4)
    
    engagement = user_data['engagement_metrics']
    with col1:
        st.metric("Total Activities", engagement['total_activities'])
    with col2:
        st.metric("Mood Entries", engagement['mood_entries'])
    with col3:
        st.metric("Check-ins", engagement['checkins'])
    with col4:
        st.metric("AI Calls", engagement['api_calls'])
    
    # Detailed insights
    col1, col2 = st.columns(2)
    
    with col1:
        if 'message' not in user_data['mood_insights']:
            st.subheader("😊 Mood Patterns")
            mood = user_data['mood_insights']
            st.write(f"**Average Intensity:** {mood['average_intensity']:.1f}")
            st.write(f"**Most Common Mood:** {mood['most_common_mood']}")
            st.write(f"**Highest Intensity:** {mood['highest_intensity_mood']}")
            
            # Mood distribution chart
            if mood['mood_distribution']:
                mood_df = pd.DataFrame(list(mood['mood_distribution'].items()), 
                                     columns=['Mood', 'Count'])
                st.bar_chart(mood_df.set_index('Mood'))
    
    with col2:
        if 'message' not in user_data['checkin_insights']:
            st.subheader("📋 Check-in Patterns")
            checkin = user_data['checkin_insights']
            st.write(f"**Most Common Period:** {checkin['most_common_period']}")
            st.write(f"**Most Common Energy:** {checkin['most_common_energy']}")
            
            # Time period distribution
            if checkin['time_period_distribution']:
                period_df = pd.DataFrame(list(checkin['time_period_distribution'].items()),
                                       columns=['Period', 'Count'])
                st.bar_chart(period_df.set_index('Period'))
    
    # AI Usage insights
    if 'message' not in user_data['usage_insights']:
        st.subheader("🤖 AI Usage")
        usage = user_data['usage_insights']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Calls", usage['total_api_calls'])
        with col2:
            st.metric("Total Cost", f"${usage['total_cost']:.4f}")
        with col3:
            st.metric("Avg Cost/Call", f"${usage['average_cost_per_call']:.6f}")
        
        # Feature usage breakdown
        if usage['feature_distribution']:
            st.write("**Feature Usage:**")
            for feature, count in usage['feature_distribution'].items():
                st.write(f"• {feature.title()}: {count} calls")

def show_global_insights(insights, days):
    """Show global insights across all users"""
    st.header(f"🌍 Global Overview ({days} days)")
    
    global_data = insights.get_user_activity_summary(days=days)
    
    # Overall metrics
    col1, col2, col3, col4 = st.columns(4)
    
    engagement = global_data['engagement_metrics']
    with col1:
        st.metric("Total Activities", engagement['total_activities'])
    with col2:
        st.metric("Mood Entries", engagement['mood_entries'])
    with col3:
        st.metric("Check-ins", engagement['checkins'])
    with col4:
        st.metric("AI Calls", engagement['api_calls'])
    
    # Detailed breakdowns
    col1, col2 = st.columns(2)
    
    with col1:
        if 'message' not in global_data['mood_insights']:
            st.subheader("😊 Global Mood Patterns")
            mood = global_data['mood_insights']
            st.write(f"**Total Entries:** {mood['total_entries']}")
            st.write(f"**Average Intensity:** {mood['average_intensity']:.1f}")
            st.write(f"**Most Common Mood:** {mood['most_common_mood']}")
            
            if 'active_users' in mood:
                st.write(f"**Active Users:** {mood['active_users']}")
    
    with col2:
        if 'message' not in global_data['usage_insights']:
            st.subheader("🤖 Global AI Usage")
            usage = global_data['usage_insights']
            st.write(f"**Total Calls:** {usage['total_api_calls']}")
            st.write(f"**Total Cost:** ${usage['total_cost']:.4f}")
            st.write(f"**Most Used Feature:** {usage['most_used_feature']}")
            
            if 'active_users' in usage:
                st.write(f"**Active Users:** {usage['active_users']}")

def show_cost_analysis(insights, days):
    """Show detailed cost analysis"""
    st.header(f"💰 Cost Analysis ({days} days)")
    
    costs = insights.get_cost_analysis(days)
    
    if 'message' in costs:
        st.info(costs['message'])
        return
    
    # Overall cost metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cost", f"${costs['total_cost']:.4f}")
    with col2:
        st.metric("Total Calls", costs['total_calls'])
    with col3:
        st.metric("Total Tokens", f"{costs['total_tokens']:,}")
    with col4:
        st.metric("Avg Cost/Call", f"${costs['average_cost_per_call']:.6f}")
    
    # Cost breakdowns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Cost by Feature")
        if costs['cost_per_feature']:
            feature_df = pd.DataFrame(list(costs['cost_per_feature'].items()),
                                    columns=['Feature', 'Cost'])
            st.bar_chart(feature_df.set_index('Feature'))
            
            st.write("**Top Features by Cost:**")
            for feature, cost in sorted(costs['cost_per_feature'].items(), 
                                      key=lambda x: x[1], reverse=True):
                st.write(f"• {feature.title()}: ${cost:.4f}")
    
    with col2:
        st.subheader("👤 Cost by User")
        if costs['cost_per_user']:
            user_df = pd.DataFrame(list(costs['cost_per_user'].items()),
                                 columns=['User', 'Cost'])
            st.bar_chart(user_df.set_index('User'))
            
            st.write("**Top Users by Cost:**")
            for user, cost in sorted(costs['cost_per_user'].items(), 
                                   key=lambda x: x[1], reverse=True):
                # Mask email for privacy
                masked_user = user.split('@')[0] + '@***'
                st.write(f"• {masked_user}: ${cost:.4f}")
    
    # Insights
    st.subheader("💡 Cost Insights")
    st.write(f"**Highest Cost User:** {costs['highest_cost_user']}")
    st.write(f"**Costliest Feature:** {costs['costliest_feature']}")

def show_feature_adoption(insights, days):
    """Show feature adoption analysis"""
    st.header(f"📊 Feature Adoption ({days} days)")
    
    adoption = insights.get_feature_adoption_analysis(days)
    
    if 'message' in adoption:
        st.info(adoption['message'])
        return
    
    # Overall metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Users", adoption['total_users'])
    with col2:
        if adoption['most_popular_feature']:
            st.metric("Most Popular Feature", adoption['most_popular_feature'].title())
    
    # Feature adoption breakdown
    st.subheader("📈 Adoption Rates")
    
    if adoption['feature_adoption']:
        # Create adoption chart
        features = []
        rates = []
        users = []
        
        for feature, data in adoption['feature_adoption'].items():
            features.append(feature.title())
            rates.append(data['adoption_rate'])
            users.append(data['users'])
        
        adoption_df = pd.DataFrame({
            'Feature': features,
            'Adoption Rate (%)': rates,
            'Users': users
        })
        
        st.bar_chart(adoption_df.set_index('Feature')['Adoption Rate (%)'])
        
        # Detailed breakdown
        st.write("**Detailed Adoption:**")
        for feature, data in adoption['feature_adoption'].items():
            st.write(f"• **{feature.title()}**: {data['adoption_rate']}% adoption "
                    f"({data['users']} users, {data['total_usage']} total uses)")

if __name__ == "__main__":
    main() 