"""
Usage Limiter for Focus Companion
Controls OpenAI API usage to manage costs and prevent abuse
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import streamlit as st

class UsageLimiter:
    """Manages API usage limits and tracking"""
    
    def __init__(self, usage_file: str = "data/usage_tracking.json"):
        self.usage_file = usage_file
        self.daily_limit = 100  # API calls per day (5 users × 20 calls)
        self.monthly_limit = 2000  # API calls per month (5 users × 400 calls)
        self.user_daily_limit = 20  # API calls per user per day
        self.user_monthly_limit = 400  # API calls per user per month
        
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
        data = self._load_usage_data()
        
        # Reset counters if needed
        self._reset_daily_usage(data)
        self._reset_monthly_usage(data)
        
        today = datetime.now().strftime("%Y-%m-%d")
        this_month = datetime.now().strftime("%Y-%m")
        
        # Check global daily limit
        daily_total = sum(data["daily_usage"].values())
        if daily_total >= self.daily_limit:
            return False, f"Daily API limit reached ({self.daily_limit} calls)"
        
        # Check global monthly limit
        monthly_total = sum(data["monthly_usage"].values())
        if monthly_total >= self.monthly_limit:
            return False, f"Monthly API limit reached ({self.monthly_limit} calls)"
        
        # Check user-specific limits
        if user_email:
            user_daily = data["user_usage"].get(user_email, {}).get(today, 0)
            if user_daily >= self.user_daily_limit:
                return False, f"Your daily limit reached ({self.user_daily_limit} calls)"
            
            user_monthly = data["user_usage"].get(user_email, {}).get(this_month, 0)
            if user_monthly >= self.user_monthly_limit:
                return False, f"Your monthly limit reached ({self.user_monthly_limit} calls)"
        
        return True, "API call allowed"
    
    def record_api_call(self, user_email: str = None):
        """Record that an API call was made"""
        data = self._load_usage_data()
        
        # Reset counters if needed
        self._reset_daily_usage(data)
        self._reset_monthly_usage(data)
        
        today = datetime.now().strftime("%Y-%m-%d")
        this_month = datetime.now().strftime("%Y-%m")
        
        # Update global daily usage
        data["daily_usage"][today] = data["daily_usage"].get(today, 0) + 1
        
        # Update global monthly usage
        data["monthly_usage"][this_month] = data["monthly_usage"].get(this_month, 0) + 1
        
        # Update user-specific usage
        if user_email:
            if user_email not in data["user_usage"]:
                data["user_usage"][user_email] = {}
            
            data["user_usage"][user_email][today] = data["user_usage"][user_email].get(today, 0) + 1
            data["user_usage"][user_email][this_month] = data["user_usage"][user_email].get(this_month, 0) + 1
        
        self._save_usage_data(data)
    
    def get_usage_stats(self, user_email: str = None) -> Dict:
        """Get current usage statistics"""
        data = self._load_usage_data()
        
        today = datetime.now().strftime("%Y-%m-%d")
        this_month = datetime.now().strftime("%Y-%m")
        
        stats = {
            "global": {
                "daily_used": sum(data["daily_usage"].values()),
                "daily_limit": self.daily_limit,
                "monthly_used": sum(data["monthly_usage"].values()),
                "monthly_limit": self.monthly_limit
            }
        }
        
        if user_email:
            user_daily = data["user_usage"].get(user_email, {}).get(today, 0)
            user_monthly = data["user_usage"].get(user_email, {}).get(this_month, 0)
            
            stats["user"] = {
                "daily_used": user_daily,
                "daily_limit": self.user_daily_limit,
                "monthly_used": user_monthly,
                "monthly_limit": self.user_monthly_limit
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
            "mood_analysis": False,  # Disable expensive features
            "focus_optimization": False,
            "stress_management": False
        }
        
        return enabled_features.get(feature, False) 