# 🧠 Focus Companion

> Your personal AI-powered focus and wellness assistant

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.47+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive focus and wellness tracking application that helps you manage your daily routines, track your mood, and achieve your goals through intelligent time-based check-ins and emotional wellness monitoring.

## ✨ Features

### 🎯 **Smart Daily Check-ins**
Time-based check-in flows that adapt to your day with persistent data storage:

- **🌅 Morning (5 AM - 12 PM)**
  - Sleep quality assessment
  - Daily focus planning
  - Energy level evaluation
  - **Persistent storage** - All check-ins saved permanently

- **☀️ Afternoon (12 PM - 6 PM)**
  - Day progress tracking
  - Plan adjustment suggestions
  - Break reminders
  - **Data continuity** - Build complete daily patterns

- **🌆 Evening (6 PM - 5 AM)**
  - Accomplishment review
  - Challenge identification
  - End-of-day reflection
  - **Historical tracking** - Review progress over time

### 😊 **Mood Tracker & Analytics**
Comprehensive emotional wellness monitoring with persistent data storage:

- **📊 Visual Analytics**
  - Mood intensity trends over time
  - Mood distribution charts
  - Interactive Plotly visualizations

- **📝 Quick Mood Logging**
  - Emoji-based mood selection
  - Intensity rating (1-10 scale)
  - Optional notes and context
  - **Persistent data storage** - Your mood history is saved permanently

- **📈 Smart Insights**
  - Daily and weekly mood averages
  - Pattern recognition
  - Progress tracking
  - Historical trend analysis

### 📖 **Mood Journal**
Comprehensive journaling system for reviewing and analyzing your wellness journey:

- **📚 Complete Entry History**
  - All mood and check-in entries in one place
  - Chronological organization by date
  - Detailed entry cards with full context

- **🔍 Advanced Filtering**
  - Filter by date range, entry type, and mood
  - Time period filters (7, 30, 90 days)
  - Quick filter clearing and reset

- **📊 Journal Statistics**
  - Total entries and averages
  - Most common moods and patterns
  - Recent activity tracking

- **📤 Export Capabilities**
  - JSON export for data analysis
  - CSV export for spreadsheet analysis
  - Timestamped files for organization

### 🤔 **Weekly Reflections**
Structured reflection system for continuous improvement:

- Weekly wins and accomplishments
- Challenge identification
- Learning capture
- Next week planning

### 📊 **Progress History**
Comprehensive tracking and visualization:

- User profile management
- Goal tracking
- Historical data review
- Progress patterns

### 🎨 **User Experience**
- **Clean, intuitive interface** with emoji-rich design
- **Responsive layout** that works on all devices
- **Time-aware interactions** that adapt to your schedule
- **Data export** functionality for personal analysis
- **🧠 Intelligent Assistant** with personalized insights and recommendations
- **🎯 Smart Recommendations** based on your patterns and preferences
- **🤖 AI-Powered Greetings** with OpenAI integration for personalized responses
- **🔐 Persistent Authentication** with "Remember me" functionality
- **📊 Usage Tracking** with real-time AI usage statistics
- **💬 Integrated Feedback System** for beta testing and improvements

### ⚡ **AI Optimization & Performance**
- **🧠 Smart Caching System** - Avoids redundant API calls for similar inputs
- **📝 Token Optimization** - Efficient prompts that reduce costs and improve speed
- **🔄 Cache Management** - Automatic expiration and cleanup of old cache entries
- **📊 Performance Monitoring** - Track cache hit rates and API call savings
- **🎯 Enhanced Dashboard** - Real-time progress tracking and mood summaries
- **📈 Weekly Summary Automation** - AI-generated insights with intelligent prompts

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd focus-companion
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 📱 Usage Guide

### First Time Setup
1. **Complete Onboarding**: Set up your profile with goals, availability, and preferences
2. **Choose Your Tone**: Select your preferred assistant communication style
3. **Set Your Situation**: Define your current life circumstances

### Daily Usage
1. **Morning Check-in**: Start your day with sleep and energy assessment
2. **Afternoon Review**: Mid-day progress check and plan adjustments
3. **Evening Reflection**: End-of-day accomplishment review
4. **Mood Tracking**: Log your emotions throughout the day
5. **Data Persistence**: All your data is automatically saved and persists across sessions

### Weekly Review
- **Reflection Sessions**: Weekly deep-dive into your progress
- **Pattern Analysis**: Review mood and focus trends
- **Goal Adjustment**: Update objectives based on insights

## 🏗️ Architecture

```
focus-companion/
├── app.py                 # Main Streamlit application
├── auth.py                # Beta access control & authentication
├── pages/                 # Application pages
│   ├── onboarding.py      # User profile setup with feedback
│   ├── daily_checkin.py   # Time-based check-ins with AI task planning
│   ├── mood_tracker.py    # Emotion tracking & analytics
│   ├── mood_journal.py    # Comprehensive journaling system
│   ├── reflection.py      # Weekly reflections
│   └── history.py         # Progress history
├── data/                  # Data storage
│   ├── database.py        # SQLite database manager
│   ├── storage.py         # Hybrid JSON/SQLite storage
│   ├── migrate_to_sqlite.py # Data migration utility
│   └── ai_cache.json       # AI response cache (auto-generated)
│   ├── focus_companion.db # SQLite database (auto-generated)
│   ├── user_profile.json  # User profile data (backup)
│   ├── mood_data.json     # Persistent mood tracking data (backup)
│   ├── checkin_data.json  # Persistent daily check-in data (backup)
│   ├── usage_tracking.json # AI usage tracking & limits (backup)
│   └── user_session.json  # Persistent authentication sessions
├── assistant/             # AI assistant logic
│   ├── logic.py           # Core assistant intelligence
│   ├── ai_service.py      # OpenAI integration with usage limits
│   ├── prompts.py         # AI prompt templates
│   ├── ai_cache.py        # Smart caching system
│   ├── fallback.py        # Fallback intelligence system
│   └── usage_limiter.py   # Usage tracking & cost control
├── memory/                # Memory management
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
├── AI_SETUP.md           # AI features setup guide
└── README.md             # This file
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Data Visualization**: Plotly
- **Data Processing**: Pandas
- **AI Integration**: OpenAI (GPT-3.5-turbo)
- **Data Storage**: SQLite database with JSON backup for compatibility
- **Data Persistence**: Automatic saving and loading of all user data
- **Authentication**: Custom beta access control with persistent sessions
- **Usage Tracking**: SQLite-based usage monitoring with detailed analytics
- **Feedback Integration**: Tally form integration for beta testing

## 🤖 AI Features

Focus Companion now includes AI-powered personalization using OpenAI's GPT-3.5-turbo:

### **🎯 AI-Powered Greetings**
- Personalized greetings based on your mood, energy, and recent patterns
- Context-aware responses that consider your goals and preferences
- Time-of-day awareness for relevant messaging

### **💬 Daily Encouragement**
- AI-generated motivational messages tailored to your situation
- Incorporates your joy sources and energy patterns
- Adapts to your preferred communication tone

### **💡 Smart Productivity Tips**
- Context-aware tips based on your energy drainers and situation
- Personalized recommendations for your available time
- Considers your recent mood patterns for relevant advice

### **🔄 Graceful Fallback**
- Seamless fallback to rule-based responses when AI is unavailable
- No interruption to your experience
- Consistent functionality regardless of AI availability

### **🔒 Privacy & Security**
- Minimal data sent to OpenAI (only essential context)
- No personal data stored by OpenAI
- Optional feature - works perfectly without AI

### **💰 Cost Control & Usage Limits**
- **Usage tracking** with daily and monthly limits
- **Per-user limits** to prevent abuse and control costs
- **Feature control** - can disable expensive AI features
- **Transparent usage stats** - users can see their AI usage
- **Predictable costs** - maximum $4/month for 5 beta testers

### **📝 Beta Testing Features**
- **Integrated feedback system** with Tally form integration
- **Persistent authentication** - no need to re-enter email
- **Usage statistics** - real-time tracking of AI usage
- **Contextual feedback prompts** - collected at optimal moments

### **🗄️ SQLite Database Features**
- **Enhanced performance** - Faster queries and better scalability
- **Detailed analytics** - Track usage patterns, costs, and feature adoption
- **Data integrity** - ACID compliance prevents data corruption
- **Easy migration** - Automatic migration from JSON to SQLite
- **Backup compatibility** - JSON files maintained as backup
- **Advanced queries** - Complex analytics and reporting capabilities
- **Admin-only insights** - Database insights restricted to administrator during beta testing

### **⚡ AI Optimization Features**
- **Smart Caching System** - Avoids redundant API calls for similar inputs
- **Token Optimization** - Efficient prompts that reduce costs and improve speed
- **Cache Management** - Automatic expiration and cleanup of old cache entries
- **Performance Monitoring** - Track cache hit rates and API call savings
- **Enhanced Dashboard** - Real-time progress tracking and mood summaries
- **Weekly Summary Automation** - AI-generated insights with intelligent prompts
- **GPT Quota UI** - Real-time usage badges and limit notifications
- **Structured Weekly Insights** - 5 key questions with personalized answers

For setup instructions, see [AI_SETUP.md](AI_SETUP.md).

## 📊 Data Structure

### User Profile
```json
{
  "goal": "Improve focus and productivity",
  "joy_sources": ["Friends", "Movement", "Creating"],
  "energy_drainers": ["Overwhelm", "Lack of sleep"],
  "therapy_coaching": "No",
  "availability": "2–4 hours",
  "energy": "Good",
  "emotional_patterns": "Not sure yet",
  "small_habit": "Daily meditation",
  "reminders": "Yes",
  "tone": "Gentle & Supportive",
  "situation": "Freelancer"
}
```

### Usage Tracking
```json
{
  "daily_usage": {"2024-01-15": 5},
  "monthly_usage": {"2024-01": 45},
  "user_usage": {
    "user@example.com": {
      "2024-01-15": 3,
      "2024-01": 25
    }
  },
  "last_reset": {
    "daily": "2024-01-15",
    "monthly": "2024-01"
  }
}
```

### Mood Entry
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "mood": "😊 Happy",
  "intensity": 8,
  "note": "Feeling productive today!",
  "date": "2024-01-15",
  "time": "10:30"
}
```

### Daily Check-in
```json
{
  "timestamp": "2024-01-15T08:00:00",
  "time_period": "morning",
  "sleep_quality": "Good",
  "focus_today": "Complete project proposal",
  "energy_level": "High"
}
```

### Check-in Data Storage
All daily check-ins are automatically saved to `data/checkin_data.json` and persist across sessions.

## 🔮 Roadmap

### Phase 1: Core Features ✅
- [x] User onboarding system
- [x] Time-based daily check-ins with persistent storage
- [x] Mood tracking with analytics and data persistence
- [x] Weekly reflections
- [x] Progress history
- [x] **Persistent data storage system** - All user data saved permanently

### Phase 2: AI Enhancement ✅
- [x] **🧠 Intelligent Assistant System** - Pattern analysis and personalized insights
- [x] **📊 Smart Recommendations** - Data-driven suggestions based on user patterns
- [x] **🎯 Personalized Greetings** - Time and context-aware interactions
- [x] **💡 Fallback Intelligence** - Smart responses without external AI
- [x] **🤖 OpenAI Integration** - AI-powered personalized responses
- [x] **💰 Usage Limits & Cost Control** - Predictable costs for beta testing
- [x] **📊 Usage Tracking** - Real-time monitoring of AI usage
- [x] **🔐 Enhanced Authentication** - Persistent sessions with "Remember me"
- [x] **💬 Feedback Integration** - Tally form integration for beta testing

### Phase 3: Advanced Features 📋
- [ ] Habit tracking integration
- [ ] Goal achievement metrics
- [ ] Social sharing capabilities
- [ ] Mobile app development
- [ ] Database integration
- [ ] **🧠 Emotional Trends Reports**
  - AI-powered pattern recognition
  - Personalized insights like "You're most energized on Tuesdays after 9h sleep"
  - Focus optimization recommendations
  - Sleep and energy correlation analysis

### Phase 4: Social & Wellness Features 🌟
- [ ] **👥 Team or Couple Mode**
  - Shared rhythms for people living together
  - Gentle partner nudges and support
  - Collaborative goal setting
  - Mutual accountability features
- [ ] **🎁 Therapy Companion Pack**
  - Export designed summaries for therapists/coaches
  - Monthly review reports
  - Progress tracking for professional support
  - Secure data sharing capabilities
- [ ] Community challenges
- [ ] Anonymous progress sharing
- [ ] Focus buddy system
- [ ] Expert coaching integration

## 🙏 Acknowledgments

- **Streamlit** for the amazing web app framework
- **Plotly** for beautiful data visualizations
- **OpenAI** for AI capabilities (planned)
- **The open-source community** for inspiration and tools

