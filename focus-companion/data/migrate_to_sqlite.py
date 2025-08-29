"""
Migration utility to move existing JSON data to SQLite database
"""

import json
import os
from datetime import datetime
from database import DatabaseManager

def migrate_json_to_sqlite():
    """Migrate all existing JSON data to SQLite database"""
    db = DatabaseManager()
    
    print("🔄 Starting migration from JSON to SQLite...")
    
    # Migrate user profiles
    migrate_user_profiles(db)
    
    # Migrate mood data
    migrate_mood_data(db)
    
    # Migrate check-in data
    migrate_checkin_data(db)
    
    # Migrate usage tracking (if exists)
    migrate_usage_tracking(db)
    
    print("✅ Migration completed successfully!")
    
    # Show database stats
    stats = db.get_database_stats()
    print(f"\n📊 Database Statistics:")
    print(f"   - User profiles: {stats['user_profiles_count']}")
    print(f"   - Mood logs: {stats['mood_logs_count']}")
    print(f"   - Check-ins: {stats['checkins_count']}")
    print(f"   - API usage records: {stats['api_usage_count']}")
    print(f"   - Unique users: {stats['unique_users']}")
    print(f"   - Total API cost: ${stats['total_api_cost']:.4f}")

def migrate_user_profiles(db):
    """Migrate user profile data"""
    profile_file = "data/user_profile.json"
    if os.path.exists(profile_file):
        print("📝 Migrating user profiles...")
        try:
            with open(profile_file, 'r') as f:
                profile_data = json.load(f)
            
            # Extract email from profile data or use a default
            user_email = profile_data.get('email', 'unknown@example.com')
            db.save_user_profile(user_email, profile_data)
            print(f"   ✅ Migrated profile for {user_email}")
            
        except Exception as e:
            print(f"   ❌ Error migrating user profile: {e}")

def migrate_mood_data(db):
    """Migrate mood tracking data"""
    mood_file = "data/mood_data.json"
    if os.path.exists(mood_file):
        print("😊 Migrating mood data...")
        try:
            with open(mood_file, 'r') as f:
                mood_entries = json.load(f)
            
            migrated_count = 0
            for entry in mood_entries:
                # Extract user email or use default
                user_email = entry.get('user_email', 'unknown@example.com')
                
                # Parse timestamp
                timestamp = entry.get('timestamp', datetime.now().isoformat())
                if isinstance(timestamp, str):
                    try:
                        # Convert to datetime if it's a string
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                db.save_mood_log(
                    user_email=user_email,
                    mood=entry.get('mood', 'unknown'),
                    intensity=entry.get('intensity', 5),
                    notes=entry.get('notes', '')
                )
                migrated_count += 1
            
            print(f"   ✅ Migrated {migrated_count} mood entries")
            
        except Exception as e:
            print(f"   ❌ Error migrating mood data: {e}")

def migrate_checkin_data(db):
    """Migrate check-in data"""
    checkin_file = "data/checkin_data.json"
    if os.path.exists(checkin_file):
        print("📋 Migrating check-in data...")
        try:
            with open(checkin_file, 'r') as f:
                checkin_entries = json.load(f)
            
            migrated_count = 0
            for entry in checkin_entries:
                # Extract user email or use default
                user_email = entry.get('user_email', 'unknown@example.com')
                
                # Prepare checkin data
                checkin_data = {
                    'time_period': entry.get('time_period', 'unknown'),
                    'sleep_quality': entry.get('sleep_quality'),
                    'energy_level': entry.get('energy_level'),
                    'focus_today': entry.get('focus_today'),
                    'current_feeling': entry.get('current_feeling'),
                    'day_progress': entry.get('day_progress'),
                    'accomplishments': entry.get('accomplishments'),
                    'challenges': entry.get('challenges'),
                    'task_plan': entry.get('task_plan', {}),
                    'task_completion': entry.get('task_completion', {})
                }
                
                db.save_checkin(user_email, checkin_data)
                migrated_count += 1
            
            print(f"   ✅ Migrated {migrated_count} check-in entries")
            
        except Exception as e:
            print(f"   ❌ Error migrating check-in data: {e}")

def migrate_usage_tracking(db):
    """Migrate usage tracking data"""
    usage_file = "data/usage_tracking.json"
    if os.path.exists(usage_file):
        print("📊 Migrating usage tracking data...")
        try:
            with open(usage_file, 'r') as f:
                usage_data = json.load(f)
            
            migrated_count = 0
            
            # Migrate daily usage
            for date, count in usage_data.get('daily_usage', {}).items():
                for _ in range(count):
                    db.record_api_usage(
                        user_email='unknown@example.com',
                        feature='migrated',
                        tokens_used=None,
                        cost_usd=None
                    )
                    migrated_count += 1
            
            # Migrate user usage
            for user_email, user_data in usage_data.get('user_usage', {}).items():
                for date, count in user_data.items():
                    for _ in range(count):
                        db.record_api_usage(
                            user_email=user_email,
                            feature='migrated',
                            tokens_used=None,
                            cost_usd=None
                        )
                        migrated_count += 1
            
            print(f"   ✅ Migrated {migrated_count} usage records")
            
        except Exception as e:
            print(f"   ❌ Error migrating usage tracking: {e}")

def backup_json_files():
    """Create backup copies of JSON files before migration"""
    json_files = [
        "data/user_profile.json",
        "data/mood_data.json", 
        "data/checkin_data.json",
        "data/usage_tracking.json"
    ]
    
    print("💾 Creating backups of JSON files...")
    
    for file_path in json_files:
        if os.path.exists(file_path):
            backup_path = file_path.replace('.json', '_backup.json')
            try:
                with open(file_path, 'r') as src, open(backup_path, 'w') as dst:
                    dst.write(src.read())
                print(f"   ✅ Backed up {file_path}")
            except Exception as e:
                print(f"   ❌ Error backing up {file_path}: {e}")

if __name__ == "__main__":
    # Create backups first
    backup_json_files()
    
    # Run migration
    migrate_json_to_sqlite() 