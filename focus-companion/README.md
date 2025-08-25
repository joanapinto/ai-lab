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
├── pages/                 # Application pages
│   ├── onboarding.py      # User profile setup
│   ├── daily_checkin.py   # Time-based check-ins with persistence
│   ├── mood_tracker.py    # Emotion tracking & analytics with persistence
│   ├── mood_journal.py    # Comprehensive journaling system
│   ├── reflection.py      # Weekly reflections
│   └── history.py         # Progress history
├── data/                  # Data storage
│   ├── storage.py         # User profile & data management
│   ├── user_profile.json  # User profile data
│   ├── mood_data.json     # Persistent mood tracking data
│   └── checkin_data.json  # Persistent daily check-in data
├── assistant/             # AI assistant logic
│   ├── logic.py           # Core assistant intelligence
│   ├── prompts.py         # AI prompt templates
│   └── fallback.py        # Fallback intelligence system
├── memory/                # Memory management
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Data Visualization**: Plotly
- **Data Processing**: Pandas
- **AI Integration**: OpenAI (planned)
- **Data Storage**: JSON files with persistent storage (expandable to database)
- **Data Persistence**: Automatic saving and loading of all user data

## 📊 Data Structure

### User Profile
```json
{
  "goal": "Improve focus and productivity",
  "availability": "2-4 hours",
  "energy": "Good",
  "check_ins": "Yes",
  "tone": "Gentle & supportive",
  "situation": "Freelancer"
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

### Phase 2: AI Enhancement 🚧
- [x] **🧠 Intelligent Assistant System** - Pattern analysis and personalized insights
- [x] **📊 Smart Recommendations** - Data-driven suggestions based on user patterns
- [x] **🎯 Personalized Greetings** - Time and context-aware interactions
- [x] **💡 Fallback Intelligence** - Smart responses without external AI
- [ ] OpenAI integration for advanced insights
- [ ] Natural language processing for reflections
- [ ] Predictive mood analysis

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

