"""
Usage Limiter for Focus Companion
Controls OpenAI API usage to manage costs and prevent abuse
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import DatabaseManager

class UsageLimiter:
    """Manages API usage limits and tracking"""
    
    def __init__(self, usage_file: str = "data/usage_tracking.json"):
        self.usage_file = usage_file
        self.daily_limit = 100  # API calls per day (5 users × 20 calls)
        self.monthly_limit = 2000  # API calls per month (5 users × 400 calls)
        self.user_daily_limit = 20  # API calls per user per day
        self.user_monthly_limit = 400  # API calls per user per month
        
        # Initialize database manager
        self.db = DatabaseManager()
        
    def _load_usage_data(self) -> Dict:
        """Load usage tracking data from file"""
        try:
            if os.path.exists(self.usage_file):
                with open(self.usage_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {
            "daily_usage": {},
            "monthly_usage": {},
            "user_usage": {},
            "last_reset": {
                "daily": datetime.now().strftime("%Y-%m-%d"),
                "monthly": datetime.now().strftime("%Y-%m")
            }
        }
    
    def _save_usage_data(self, data: Dict):
        """Save usage tracking data to file"""
        try:
            os.makedirs(os.path.dirname(self.usage_file), exist_ok=True)
            with open(self.usage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass  # Silently fail if we can't save
    
    def _reset_daily_usage(self, data: Dict):
        """Reset daily usage counters"""
        today = datetime.now().strftime("%Y-%m-%d")
        if data["last_reset"]["daily"] != today:
            data["daily_usage"] = {}
            data["user_usage"] = {}
            data["last_reset"]["daily"] = today
            return True
        return False
    
    def _reset_monthly_usage(self, data: Dict):
        """Reset monthly usage counters"""
        this_month = datetime.now().strftime("%Y-%m")
        if data["last_reset"]["monthly"] != this_month:
            data["monthly_usage"] = {}
            data["last_reset"]["monthly"] = this_month
            return True
        return False
    
    def can_make_api_call(self, user_email: str = None) -> tuple[bool, str]:
        """
        Check if an API call can be made
        Returns (allowed, reason)
        """
        # Get usage from database
        global_usage = self.db.get_global_api_usage(days=1)  # Today
        global_monthly = self.db.get_global_api_usage(days=30)  # This month
        
        # Check global daily limit
        today_usage = sum(global_usage["daily_usage"].values())
        if today_usage >= self.daily_limit:
            return False, f"Daily API limit reached ({self.daily_limit} calls)"
        
        # Check global monthly limit
        monthly_usage = sum(global_monthly["monthly_usage"].values())
        if monthly_usage >= self.monthly_limit:
            return False, f"Monthly API limit reached ({self.monthly_limit} calls)"
        
        # Check user-specific limits
        if user_email:
            user_usage = self.db.get_user_api_usage(user_email, days=1)
            user_monthly = self.db.get_user_api_usage(user_email, days=30)
            
            user_daily = sum(user_usage["daily_usage"].values())
            if user_daily >= self.user_daily_limit:
                return False, f"Your daily limit reached ({self.user_daily_limit} calls)"
            
            user_monthly_total = sum(user_monthly["monthly_usage"].values())
            if user_monthly_total >= self.user_monthly_limit:
                return False, f"Your monthly limit reached ({self.user_monthly_limit} calls)"
        
        return True, "API call allowed"
    
    def record_api_call(self, user_email: str = None, feature: str = "unknown", 
                       tokens_used: int = None, cost_usd: float = None):
        """Record that an API call was made"""
        if user_email:
            self.db.record_api_usage(
                user_email=user_email,
                feature=feature,
                tokens_used=tokens_used,
                cost_usd=cost_usd,
                success=True
            )
    
    def get_usage_stats(self, user_email: str = None) -> Dict:
        """Get current usage statistics"""
        # Get global stats
        global_usage = self.db.get_global_api_usage(days=1)
        global_monthly = self.db.get_global_api_usage(days=30)
        
        stats = {
            "global": {
                "daily_used": sum(global_usage["daily_usage"].values()),
                "daily_limit": self.daily_limit,
                "monthly_used": sum(global_monthly["monthly_usage"].values()),
                "monthly_limit": self.monthly_limit,
                "total_cost": global_monthly["total_cost"]
            }
        }
        
        if user_email:
            user_usage = self.db.get_user_api_usage(user_email, days=1)
            user_monthly = self.db.get_user_api_usage(user_email, days=30)
            
            stats["user"] = {
                "daily_used": sum(user_usage["daily_usage"].values()),
                "daily_limit": self.user_daily_limit,
                "monthly_used": sum(user_monthly["monthly_usage"].values()),
                "monthly_limit": self.user_monthly_limit,
                "total_cost": user_monthly["total_cost"],
                "feature_usage": user_monthly["feature_usage"]
            }
        
        return stats
    
    def is_feature_enabled(self, feature: str, user_email: str = None) -> bool:
        """
        Check if a specific AI feature is enabled
        Can be used to disable certain features for cost control
        """
        # Define which features are enabled for beta testing
        enabled_features = {
                                "greeting": True,
                    "encouragement": True,
                    "productivity_tip": True,
                    "weekly_summary": True,  # Enable weekly summaries
                    "mood_analysis": False,  # Disable expensive features
                    "focus_optimization": False,
                    "stress_management": False
        }
        
        return enabled_features.get(feature, False) 