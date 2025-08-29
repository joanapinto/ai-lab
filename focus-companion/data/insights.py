"""
Database Insights Tool for Focus Companion
Provides comprehensive analytics and reporting
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import DatabaseManager

class DatabaseInsights:
    """Provides insights and analytics from the Focus Companion database"""
    
    def __init__(self, db_path: str = "data/focus_companion.db"):
        self.db_path = db_path
        self.db = DatabaseManager(db_path)
    
    def get_user_activity_summary(self, user_email: str = None, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive activity summary for a user or all users"""
        with sqlite3.connect(self.db_path) as conn:
            # Convert to pandas for easier analysis
            if user_email:
                # User-specific queries
                mood_query = f"""
                    SELECT mood, intensity, created_at 
                    FROM mood_logs 
                    WHERE user_email = ? AND created_at >= date('now', '-{days} days')
                    ORDER BY created_at DESC
                """
                checkin_query = f"""
                    SELECT time_period, energy_level, sleep_quality, created_at
                    FROM checkins 
                    WHERE user_email = ? AND created_at >= date('now', '-{days} days')
                    ORDER BY created_at DESC
                """
                usage_query = f"""
                    SELECT feature, tokens_used, cost_usd, created_at
                    FROM api_usage 
                    WHERE user_email = ? AND created_at >= date('now', '-{days} days')
                    ORDER BY created_at DESC
                """
                
                mood_df = pd.read_sql_query(mood_query, conn, params=(user_email,))
                checkin_df = pd.read_sql_query(checkin_query, conn, params=(user_email,))
                usage_df = pd.read_sql_query(usage_query, conn, params=(user_email,))
            else:
                # Global queries
                mood_query = f"""
                    SELECT user_email, mood, intensity, created_at 
                    FROM mood_logs 
                    WHERE created_at >= date('now', '-{days} days')
                    ORDER BY created_at DESC
                """
                checkin_query = f"""
                    SELECT user_email, time_period, energy_level, sleep_quality, created_at
                    FROM checkins 
                    WHERE created_at >= date('now', '-{days} days')
                    ORDER BY created_at DESC
                """
                usage_query = f"""
                    SELECT user_email, feature, tokens_used, cost_usd, created_at
                    FROM api_usage 
                    WHERE created_at >= date('now', '-{days} days')
                    ORDER BY created_at DESC
                """
                
                mood_df = pd.read_sql_query(mood_query, conn)
                checkin_df = pd.read_sql_query(checkin_query, conn)
                usage_df = pd.read_sql_query(usage_query, conn)
            
            # Calculate insights
            insights = {
                "period": f"Last {days} days",
                "user_email": user_email or "All users",
                "mood_insights": self._analyze_mood_data(mood_df),
                "checkin_insights": self._analyze_checkin_data(checkin_df),
                "usage_insights": self._analyze_usage_data(usage_df),
                "engagement_metrics": self._calculate_engagement_metrics(mood_df, checkin_df, usage_df)
            }
            
            return insights
    
    def _analyze_mood_data(self, mood_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze mood data patterns"""
        if mood_df.empty:
            return {"message": "No mood data available"}
        
        insights = {
            "total_entries": len(mood_df),
            "average_intensity": mood_df['intensity'].mean(),
            "mood_distribution": mood_df['mood'].value_counts().to_dict(),
            "intensity_trend": mood_df.groupby('mood')['intensity'].mean().to_dict(),
            "most_common_mood": mood_df['mood'].mode().iloc[0] if not mood_df['mood'].mode().empty else None,
            "highest_intensity_mood": mood_df.loc[mood_df['intensity'].idxmax(), 'mood'] if not mood_df.empty else None
        }
        
        # Time-based analysis if we have multiple users
        if 'user_email' in mood_df.columns:
            insights["active_users"] = mood_df['user_email'].nunique()
            insights["entries_per_user"] = mood_df.groupby('user_email').size().to_dict()
        
        return insights
    
    def _analyze_checkin_data(self, checkin_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze check-in data patterns"""
        if checkin_df.empty:
            return {"message": "No check-in data available"}
        
        insights = {
            "total_checkins": len(checkin_df),
            "time_period_distribution": checkin_df['time_period'].value_counts().to_dict(),
            "energy_level_distribution": checkin_df['energy_level'].value_counts().to_dict(),
            "sleep_quality_distribution": checkin_df['sleep_quality'].value_counts().to_dict(),
            "most_common_period": checkin_df['time_period'].mode().iloc[0] if not checkin_df['time_period'].mode().empty else None,
            "most_common_energy": checkin_df['energy_level'].mode().iloc[0] if not checkin_df['energy_level'].mode().empty else None
        }
        
        # Time-based analysis if we have multiple users
        if 'user_email' in checkin_df.columns:
            insights["active_users"] = checkin_df['user_email'].nunique()
            insights["checkins_per_user"] = checkin_df.groupby('user_email').size().to_dict()
        
        return insights
    
    def _analyze_usage_data(self, usage_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze API usage data"""
        if usage_df.empty:
            return {"message": "No API usage data available"}
        
        insights = {
            "total_api_calls": len(usage_df),
            "total_tokens": usage_df['tokens_used'].sum(),
            "total_cost": usage_df['cost_usd'].sum(),
            "feature_distribution": usage_df['feature'].value_counts().to_dict(),
            "average_tokens_per_call": usage_df['tokens_used'].mean(),
            "average_cost_per_call": usage_df['cost_usd'].mean(),
            "most_used_feature": usage_df['feature'].mode().iloc[0] if not usage_df['feature'].mode().empty else None,
            "costliest_feature": usage_df.groupby('feature')['cost_usd'].sum().idxmax() if not usage_df.empty else None
        }
        
        # Time-based analysis if we have multiple users
        if 'user_email' in usage_df.columns:
            insights["active_users"] = usage_df['user_email'].nunique()
            insights["calls_per_user"] = usage_df.groupby('user_email').size().to_dict()
            insights["cost_per_user"] = usage_df.groupby('user_email')['cost_usd'].sum().to_dict()
        
        return insights
    
    def _calculate_engagement_metrics(self, mood_df: pd.DataFrame, checkin_df: pd.DataFrame, usage_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate user engagement metrics"""
        metrics = {
            "total_activities": len(mood_df) + len(checkin_df) + len(usage_df),
            "mood_entries": len(mood_df),
            "checkins": len(checkin_df),
            "api_calls": len(usage_df)
        }
        
        # Calculate activity frequency
        if not mood_df.empty:
            metrics["avg_mood_entries_per_day"] = len(mood_df) / 30  # Assuming 30 days
        
        if not checkin_df.empty:
            metrics["avg_checkins_per_day"] = len(checkin_df) / 30
        
        if not usage_df.empty:
            metrics["avg_api_calls_per_day"] = len(usage_df) / 30
        
        return metrics
    
    def get_feature_adoption_analysis(self, days: int = 30) -> Dict[str, Any]:
        """Analyze feature adoption across users"""
        with sqlite3.connect(self.db_path) as conn:
            # Get all users
            users_df = pd.read_sql_query("SELECT DISTINCT user_email FROM user_profiles", conn)
            
            if users_df.empty:
                return {"message": "No users found"}
            
            # Get feature usage per user
            usage_query = f"""
                SELECT user_email, feature, COUNT(*) as usage_count
                FROM api_usage 
                WHERE created_at >= date('now', '-{days} days')
                GROUP BY user_email, feature
            """
            usage_df = pd.read_sql_query(usage_query, conn)
            
            # Calculate adoption rates
            total_users = len(users_df)
            feature_adoption = {}
            
            if not usage_df.empty:
                for feature in usage_df['feature'].unique():
                    users_with_feature = usage_df[usage_df['feature'] == feature]['user_email'].nunique()
                    adoption_rate = (users_with_feature / total_users) * 100
                    feature_adoption[feature] = {
                        "users": users_with_feature,
                        "adoption_rate": round(adoption_rate, 1),
                        "total_usage": usage_df[usage_df['feature'] == feature]['usage_count'].sum()
                    }
            
            return {
                "total_users": total_users,
                "feature_adoption": feature_adoption,
                "most_popular_feature": max(feature_adoption.items(), key=lambda x: x[1]['adoption_rate'])[0] if feature_adoption else None
            }
    
    def get_cost_analysis(self, days: int = 30) -> Dict[str, Any]:
        """Analyze costs and usage patterns"""
        with sqlite3.connect(self.db_path) as conn:
            usage_query = f"""
                SELECT 
                    user_email,
                    feature,
                    SUM(tokens_used) as total_tokens,
                    SUM(cost_usd) as total_cost,
                    COUNT(*) as call_count
                FROM api_usage 
                WHERE created_at >= date('now', '-{days} days')
                GROUP BY user_email, feature
                ORDER BY total_cost DESC
            """
            usage_df = pd.read_sql_query(usage_query, conn)
            
            if usage_df.empty:
                return {"message": "No usage data available"}
            
            # Calculate cost insights
            total_cost = usage_df['total_cost'].sum()
            total_tokens = usage_df['total_tokens'].sum()
            total_calls = usage_df['call_count'].sum()
            
            # Cost per user
            cost_per_user = usage_df.groupby('user_email')['total_cost'].sum().to_dict()
            
            # Cost per feature
            cost_per_feature = usage_df.groupby('feature')['total_cost'].sum().to_dict()
            
            return {
                "total_cost": total_cost,
                "total_tokens": total_tokens,
                "total_calls": total_calls,
                "average_cost_per_call": total_cost / total_calls if total_calls > 0 else 0,
                "cost_per_user": cost_per_user,
                "cost_per_feature": cost_per_feature,
                "highest_cost_user": max(cost_per_user.items(), key=lambda x: x[1])[0] if cost_per_user else None,
                "costliest_feature": max(cost_per_feature.items(), key=lambda x: x[1])[0] if cost_per_feature else None
            }
    
    def export_user_data(self, user_email: str, format: str = "json") -> str:
        """Export all data for a specific user"""
        with sqlite3.connect(self.db_path) as conn:
            # Get all user data
            profile = self.db.get_user_profile(user_email)
            mood_logs = self.db.get_mood_logs(user_email, days=365)
            checkins = self.db.get_checkins(user_email, days=365)
            usage_stats = self.db.get_user_api_usage(user_email, days=365)
            
            user_data = {
                "user_email": user_email,
                "export_date": datetime.now().isoformat(),
                "profile": profile,
                "mood_logs": mood_logs,
                "checkins": checkins,
                "api_usage": usage_stats
            }
            
            if format == "json":
                import json
                filename = f"data/user_export_{user_email.replace('@', '_at_')}_{datetime.now().strftime('%Y%m%d')}.json"
                with open(filename, 'w') as f:
                    json.dump(user_data, f, indent=2, default=str)
                return filename
            
            return "Export format not supported"

def print_insights(insights: Dict[str, Any]):
    """Pretty print insights data"""
    print("🔍 Focus Companion Database Insights")
    print("=" * 60)
    print(f"📊 Period: {insights['period']}")
    print(f"👤 User: {insights['user_email']}")
    print()
    
    # Engagement Metrics
    print("📈 Engagement Metrics:")
    engagement = insights['engagement_metrics']
    print(f"   • Total Activities: {engagement['total_activities']}")
    print(f"   • Mood Entries: {engagement['mood_entries']}")
    print(f"   • Check-ins: {engagement['checkins']}")
    print(f"   • API Calls: {engagement['api_calls']}")
    print()
    
    # Mood Insights
    if 'message' not in insights['mood_insights']:
        print("😊 Mood Insights:")
        mood = insights['mood_insights']
        print(f"   • Total Entries: {mood['total_entries']}")
        print(f"   • Average Intensity: {mood['average_intensity']:.1f}")
        print(f"   • Most Common Mood: {mood['most_common_mood']}")
        print(f"   • Highest Intensity Mood: {mood['highest_intensity_mood']}")
        print()
    
    # Check-in Insights
    if 'message' not in insights['checkin_insights']:
        print("📋 Check-in Insights:")
        checkin = insights['checkin_insights']
        print(f"   • Total Check-ins: {checkin['total_checkins']}")
        print(f"   • Most Common Period: {checkin['most_common_period']}")
        print(f"   • Most Common Energy Level: {checkin['most_common_energy']}")
        print()
    
    # Usage Insights
    if 'message' not in insights['usage_insights']:
        print("🤖 AI Usage Insights:")
        usage = insights['usage_insights']
        print(f"   • Total API Calls: {usage['total_api_calls']}")
        print(f"   • Total Cost: ${usage['total_cost']:.4f}")
        print(f"   • Most Used Feature: {usage['most_used_feature']}")
        print(f"   • Average Cost per Call: ${usage['average_cost_per_call']:.6f}")
        print()

if __name__ == "__main__":
    # Example usage
    insights = DatabaseInsights()
    
    # Get global insights
    print("🌍 Global Insights:")
    global_insights = insights.get_user_activity_summary(days=30)
    print_insights(global_insights)
    
    # Get feature adoption
    print("📊 Feature Adoption Analysis:")
    adoption = insights.get_feature_adoption_analysis()
    if 'message' not in adoption:
        print(f"   Total Users: {adoption['total_users']}")
        for feature, data in adoption['feature_adoption'].items():
            print(f"   • {feature}: {data['adoption_rate']}% adoption ({data['users']} users)")
    else:
        print(f"   {adoption['message']}")
    
    # Get cost analysis
    print("\n💰 Cost Analysis:")
    costs = insights.get_cost_analysis()
    if 'message' not in costs:
        print(f"   Total Cost: ${costs['total_cost']:.4f}")
        print(f"   Total Calls: {costs['total_calls']}")
        print(f"   Average Cost per Call: ${costs['average_cost_per_call']:.6f}")
    else:
        print(f"   {costs['message']}") 