"""
AI Cache Manager for Focus Companion
Smart caching system to optimize API calls and reduce costs
"""

import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import streamlit as st

class AICache:
    """Smart caching system for AI responses"""
    
    def __init__(self, cache_file: str = "data/ai_cache.json", max_cache_age_hours: int = 24):
        self.cache_file = cache_file
        self.max_cache_age_hours = max_cache_age_hours
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict[str, Any]:
        """Load cache from file"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                    # Clean expired entries
                    return self._clean_expired_entries(cache_data)
        except Exception:
            pass
        return {}
    
    def _save_cache(self):
        """Save cache to file"""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception:
            pass  # Silently fail if we can't save cache
    
    def _clean_expired_entries(self, cache_data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove expired cache entries"""
        current_time = datetime.now()
        cleaned_cache = {}
        
        for key, entry in cache_data.items():
            try:
                cache_time = datetime.fromisoformat(entry['timestamp'])
                if current_time - cache_time < timedelta(hours=self.max_cache_age_hours):
                    cleaned_cache[key] = entry
            except Exception:
                continue  # Skip invalid entries
        
        return cleaned_cache
    
    def _generate_cache_key(self, feature: str, user_email: str, input_data: Dict[str, Any]) -> str:
        """Generate a unique cache key for the input"""
        # Create a normalized version of input data for consistent hashing
        normalized_data = {
            'feature': feature,
            'user_email': user_email,
            'input_hash': self._hash_input(input_data)
        }
        
        # Create hash of normalized data
        cache_key_data = json.dumps(normalized_data, sort_keys=True)
        return hashlib.md5(cache_key_data.encode()).hexdigest()
    
    def _hash_input(self, input_data: Dict[str, Any]) -> str:
        """Create a hash of input data, excluding timestamps and other volatile fields"""
        # Create a copy and remove volatile fields
        clean_data = input_data.copy()
        
        # Remove timestamp fields that change frequently
        volatile_fields = ['timestamp', 'created_at', 'updated_at', 'id']
        for field in volatile_fields:
            if field in clean_data:
                del clean_data[field]
        
        # For nested data, clean recursively
        def clean_nested_data(data):
            if isinstance(data, dict):
                cleaned = {}
                for key, value in data.items():
                    if key not in volatile_fields:
                        cleaned[key] = clean_nested_data(value)
                return cleaned
            elif isinstance(data, list):
                return [clean_nested_data(item) for item in data]
            else:
                return data
        
        cleaned_data = clean_nested_data(clean_data)
        
        # Create hash of cleaned data
        return hashlib.md5(json.dumps(cleaned_data, sort_keys=True).encode()).hexdigest()
    
    def get_cached_response(self, feature: str, user_email: str, input_data: Dict[str, Any]) -> Optional[str]:
        """Get cached response if available and not expired"""
        cache_key = self._generate_cache_key(feature, user_email, input_data)
        
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            cache_time = datetime.fromisoformat(entry['timestamp'])
            
            # Check if cache is still valid
            if datetime.now() - cache_time < timedelta(hours=self.max_cache_age_hours):
                return entry['response']
            else:
                # Remove expired entry
                del self.cache[cache_key]
                self._save_cache()
        
        return None
    
    def cache_response(self, feature: str, user_email: str, input_data: Dict[str, Any], response: str):
        """Cache a response"""
        cache_key = self._generate_cache_key(feature, user_email, input_data)
        
        self.cache[cache_key] = {
            'feature': feature,
            'user_email': user_email,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'input_hash': self._hash_input(input_data)
        }
        
        self._save_cache()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_entries = len(self.cache)
        features = {}
        
        for entry in self.cache.values():
            feature = entry.get('feature', 'unknown')
            features[feature] = features.get(feature, 0) + 1
        
        return {
            'total_entries': total_entries,
            'features': features,
            'cache_size_mb': self._get_cache_size_mb()
        }
    
    def _get_cache_size_mb(self) -> float:
        """Get cache file size in MB"""
        try:
            if os.path.exists(self.cache_file):
                return os.path.getsize(self.cache_file) / (1024 * 1024)
        except Exception:
            pass
        return 0.0
    
    def clear_cache(self, user_email: str = None):
        """Clear cache for specific user or all cache"""
        if user_email:
            # Clear cache for specific user
            keys_to_remove = []
            for key, entry in self.cache.items():
                if entry.get('user_email') == user_email:
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                del self.cache[key]
        else:
            # Clear all cache
            self.cache = {}
        
        self._save_cache()
    
    def get_cache_hit_rate(self, user_email: str = None) -> Dict[str, float]:
        """Calculate cache hit rate (requires tracking hits/misses)"""
        # This would require additional tracking in the AI service
        # For now, return basic stats
        return {
            'total_entries': len(self.cache),
            'estimated_savings': len(self.cache) * 0.1  # Rough estimate of API calls saved
        }

class PromptOptimizer:
    """Optimize prompts for better token efficiency"""
    
    @staticmethod
    def optimize_weekly_summary_prompt(user_profile: Dict, week_analysis: Dict) -> str:
        """Create an optimized prompt for weekly summaries"""
        
        # Extract only essential data
        essential_data = {
            'checkins': week_analysis['total_checkins'],
            'moods': week_analysis['total_mood_entries'],
            'active_days': len(set(week_analysis['checkin_days'])),
            'goal': user_profile.get('goal', 'Improve focus and productivity'),
            'tone': user_profile.get('tone', 'Friendly')
        }
        
        # Find key patterns efficiently
        if week_analysis['energy_patterns']:
            energy_days = list(week_analysis['energy_patterns'].keys())
            essential_data['energy_days'] = energy_days[:3]  # Top 3 days
        
        if week_analysis['mood_patterns']:
            all_moods = []
            for day_data in week_analysis['mood_patterns'].values():
                all_moods.extend(day_data['moods'])
            if all_moods:
                essential_data['top_mood'] = max(set(all_moods), key=all_moods.count)
        
        # Create concise prompt
        prompt = f"""
Analyze weekly wellness data and provide encouraging insights.

User: {essential_data['goal']} | Tone: {essential_data['tone']}
Data: {essential_data['checkins']} check-ins, {essential_data['moods']} moods, {essential_data['active_days']} active days
Patterns: Energy peaks on {essential_data.get('energy_days', ['N/A'])} | Top mood: {essential_data.get('top_mood', 'N/A')}

Write 2-3 encouraging paragraphs celebrating progress and suggesting improvements.
"""
        
        return prompt
    
    @staticmethod
    def optimize_greeting_prompt(user_profile: Dict, recent_data: Dict) -> str:
        """Create an optimized prompt for greetings"""
        
        # Extract only essential context
        essential_context = {
            'time': recent_data.get('time_context', 'day'),
            'goal': user_profile.get('goal', 'Improve focus and productivity'),
            'tone': user_profile.get('tone', 'Friendly')
        }
        
        # Add mood summary if available
        if recent_data.get('mood_summary'):
            essential_context['mood'] = recent_data['mood_summary']
        
        prompt = f"""
Create a warm {essential_context['tone'].lower()} greeting for someone working on: {essential_context['goal']}
Time: {essential_context['time']} | Mood: {essential_context.get('mood', 'Good')}
Keep it personal and encouraging (1-2 sentences).
"""
        
        return prompt
    
    @staticmethod
    def optimize_encouragement_prompt(user_profile: Dict, recent_data: Dict) -> str:
        """Create an optimized prompt for daily encouragement"""
        
        essential_context = {
            'goal': user_profile.get('goal', 'Improve focus and productivity'),
            'tone': user_profile.get('tone', 'Friendly'),
            'energy': recent_data.get('checkin_summary', 'Good energy')
        }
        
        prompt = f"""
Provide {essential_context['tone'].lower()} encouragement for someone with {essential_context['energy']} working on: {essential_context['goal']}
Write 1-2 motivating sentences.
"""
        
        return prompt

# Global cache instance
ai_cache = AICache() 