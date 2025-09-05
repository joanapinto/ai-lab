# 🧠 Humsy

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
  - Current feeling tracking
  - **AI-Powered Task Planning** - Personalized daily plans based on your energy, mood, and goals

- **☀️ Afternoon (12 PM - 6 PM)**
  - Day progress tracking
  - Plan adjustment suggestions
  - Break reminders
  - Energy level and focus assessment
  - **Data continuity** - Build complete daily patterns

- **🌆 Evening (6 PM - 5 AM)**
  - Accomplishment review
  - Challenge identification
  - End-of-day reflection
  - Tomorrow's focus planning
  - **Historical tracking** - Review progress over time

### 😊 **Mood Tracker & Analytics**
Comprehensive emotional wellness monitoring with persistent data storage:

- **📝 Enhanced Mood Logging** - **NEW: Multiple moods + reasons tracking**
  - **Multiple mood selection** - Choose all emotions you're feeling
  - **Predefined reasons** - Context-aware options for each mood
  - **Custom reason input** - Add your own reasons when needed
  - **Beautiful gradient-styled form** positioned above analytics
  - **Persistent data storage** - Your mood history is saved permanently

- **📊 Advanced Analytics**
  - **Mood distribution** - See which emotions you experience most
  - **Mood frequency over time** - Track emotional patterns with interactive bar charts
  - **Reasons analysis** - Understand what triggers each mood
  - **Mood-reason correlations** - Discover patterns in your emotional landscape
  - Interactive Plotly visualizations with enhanced insights

- **📈 Smart Insights**
  - **Top reasons analysis** - Most common triggers for your moods
  - **Pattern recognition** - Understand your emotional patterns
  - **Progress tracking** - Monitor your emotional wellness journey
  - **Historical trend analysis** - See how your emotional landscape evolves

- **🎯 Context-Aware Reasons System**
  - **10 emotion categories** with tailored reason options
  - **Smart suggestions** based on your selected mood
  - **Custom input** for unique situations
  - **Mood-reason mapping** for deeper emotional understanding
  - **Pattern discovery** to identify emotional triggers

### 👤 **User Profile Management** - **NEW FEATURE**
Comprehensive profile system for personalization:

- **🎯 Editable Goals** - Update your main focus anytime
- **📝 Onboarding Answers** - Review and edit your initial setup
- **💬 Feedback Integration** - Direct access to feedback and bug report forms
- **📋 Beta Tester Guide** - Comprehensive guide for new users
- **🔧 Profile Statistics** - Track your wellness journey

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
  - Timestamped files for organization

### 🤔 **Weekly Reflections**
Structured reflection system for continuous improvement:

- Weekly wins and accomplishments
- Challenge identification
- Learning capture
- Next week planning
- **AI Summary** - Optional AI-generated insights

### 📊 **Insights & Analytics** - **RENAMED & ENHANCED**
Comprehensive tracking and visualization (formerly "History"):

- **📈 Overview Dashboard** - Profile info and recent activity
- **😊 Mood Analytics** - Trends, time patterns, and insights
- **📝 Check-in Insights** - Frequency and energy level analysis
- **📖 Journal by Month** - Organized monthly journal entries
- **🔍 Reflection Archive** - Complete reflection history

### 🎨 **User Experience & Navigation** - **MAJORLY IMPROVED**
- **🧭 Custom Navigation Menu** - Clean, organized sidebar navigation
- **🏠 Streamlined Dashboard** - Focused home page with essential features
- **📱 Minimalist Design** - Reduced visual clutter and improved aesthetics
- **🎯 Quick Actions** - Easy access to daily check-in, mood logging, and weekly reflection
- **🔐 Persistent Authentication** with "Remember me" functionality
- **📊 Usage Tracking** with real-time AI usage statistics
- **💬 Integrated Feedback System** - Easy access to feedback and bug report forms via sidebar navigation
- **🧠 Intelligent Assistant** with personalized insights and recommendations
- **🎯 Smart Recommendations** based on your patterns and preferences
- **🤖 AI-Powered Greetings** with OpenAI integration for personalized responses

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

### 🧭 **New Navigation Structure**
- **Custom Sidebar**: Clean, organized navigation replacing Streamlit's default
- **Page Organization**: Logical flow from Home → Profile → Daily Check-in → Weekly Reflection → Insights
- **Quick Actions**: Easy access to essential features from the dashboard
- **Consistent Experience**: Same navigation available on all pages

## 📱 Usage Guide

### First Time Setup
1. **Complete Onboarding**: Set up your profile with goals, availability, and preferences
2. **Choose Your Tone**: Select your preferred assistant communication style
3. **Set Your Situation**: Define your current life circumstances

### Navigation & Pages
- **🏠 Home**: Streamlined dashboard with quick actions and AI insights
- **👤 Profile**: Manage your goals, review onboarding answers, and access feedback
- **📝 Daily Check-in**: Time-based check-ins with AI-powered task planning
- **🌱 Weekly Reflection**: Weekly progress review and planning
- **📊 Insights**: Comprehensive analytics and mood patterns (formerly History)

### Daily Usage
1. **Morning Check-in**: Start your day with sleep, energy, and focus assessment
2. **Afternoon Review**: Mid-day progress check and plan adjustments
3. **Evening Reflection**: End-of-day accomplishment review and tomorrow's planning
4. **Mood Tracking**: Log your emotions with the beautiful new form above graphs
5. **Data Persistence**: All your data is automatically saved and persists across sessions

### Weekly Review
- **Reflection Sessions**: Weekly deep-dive into your progress
- **Pattern Analysis**: Review mood and focus trends
- **Goal Adjustment**: Update objectives based on insights
- **AI Summary**: Optional AI-generated weekly insights

## 🏗️ Architecture

```
focus-companion/
├── app.py                 # Main Streamlit application
├── auth.py                # Beta access control & authentication
├── pages/                 # Application pages
│   ├── profile.py         # NEW: User profile management & editing
│   ├── onboarding.py      # User profile setup with feedback
│   ├── daily_checkin.py   # Time-based check-ins with AI task planning
│   ├── mood_tracker.py    # Enhanced emotion tracking & analytics
│   ├── mood_journal.py    # Comprehensive journaling system
│   ├── reflection.py      # Weekly reflections
│   ├── history.py         # RENAMED: Insights & analytics
│   └── insights.py        # Admin database insights
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

### **🚀 AI-Powered Task Planning**
- **Personalized Daily Plans** based on your energy, mood, and goals
- **Deep Personalization** considering how you feel, what you need to do, and your motivations
- **Overwhelm Prevention** with smart task breakdown strategies
- **Energy-Aware Design** that adapts to your current energy levels
- **Emotional Intelligence** that considers your feelings and stress triggers
- **Context-Aware Recommendations** based on your recent patterns and goals

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
- **Admin bypass** - unlimited access for admin user (joanapnpinto@gmail.com)
- **Feature control** - can disable expensive AI features
- **Transparent usage stats** - users can see their AI usage
- **Predictable costs** - maximum $4/month for 5 beta testers
- **Smart fallback** - graceful degradation when limits are reached

### **📝 Beta Testing Features**
- **Integrated feedback system** with Tally form integration for feedback and bug reports
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
- **Inline Summary Generation** - One-click weekly summary from main dashboard
- **Enhanced Loading Animations** - Beautiful progress indicators for AI responses
- **AI-Powered Task Planning** - Personalized daily plans based on energy, mood, and goals
- **Enhanced AI Prompts** - Comprehensive task planning prompts with deep personalization

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
  "moods": ["😊 Happy", "💪 Confident"],
  "reasons": {
    "😊 Happy": ["A win or achievement", "Productive day"],
    "💪 Confident": ["Solved a problem", "Completed a task"]
  },
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

## 🎉 **Major Update - December 2024** 

### **🚀 What's New Today:**
- **🏷️ App Rebranding**: "Focus Companion" → **"Humsy"** - A fresh, memorable name for your wellness journey
- **🧭 Custom Navigation**: Beautiful, organized sidebar navigation replacing Streamlit's default
- **👤 Profile Page**: New dedicated page for managing goals, onboarding answers, and feedback
- **📝 Enhanced Mood Tracker**: Quick mood logging moved above graphs with beautiful gradient styling
- **🎨 UI/UX Overhaul**: Minimalist design with reduced clutter and improved aesthetics
- **🏠 Streamlined Dashboard**: Cleaner home page focused on essential features
- **📊 Page Restructuring**: Better information architecture and user flow
- **🐛 Bug Report System**: Easy access to bug reporting via sidebar navigation
- **📊 Improved Analytics**: Enhanced mood frequency charts with better visualization

### **💡 Key Improvements:**
- **Better User Experience**: More intuitive navigation and cleaner interface
- **Enhanced Mood Tracking**: Prominent mood logging with beautiful visual design
- **Improved Profile Management**: Easy access to edit goals and review onboarding
- **Consistent Design**: Unified styling across all pages and components
- **Mobile-First Approach**: Better responsive design for all devices

---

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
- [x] **🎯 AI Task Planning** - Personalized daily plans based on energy, mood, and goals
- [x] **💰 Usage Limits & Cost Control** - Predictable costs for beta testing
- [x] **📊 Usage Tracking** - Real-time monitoring of AI usage
- [x] **🔐 Enhanced Authentication** - Persistent sessions with "Remember me"
- [x] **💬 Feedback Integration** - Tally form integration for beta testing

### Phase 2.5: UI/UX Overhaul ✅ - **COMPLETED TODAY**
- [x] **🏷️ App Renaming** - Rebranded from "Focus Companion" to "Humsy"
- [x] **🧭 Custom Navigation** - Replaced Streamlit's default navigation with clean sidebar
- [x] **👤 Profile Page** - New dedicated profile management page
- [x] **📝 Enhanced Mood Tracker** - Moved quick mood log above graphs with beautiful styling
- [x] **📊 Page Restructuring** - Reorganized pages and improved information architecture
- [x] **🎨 Minimalist Design** - Reduced visual clutter and improved aesthetics
- [x] **🏠 Streamlined Dashboard** - Cleaner home page with focused quick actions
- [x] **🎯 Advanced Mood Tracking** - Multiple moods + context-aware reasons system

### Phase 3: Advanced Features 📋
- [ ] **🧠 Enhanced AI Task Planning** - Further improvements to personalization and overwhelm prevention
- [ ] **📱 Mobile App Development** - Native mobile application
- [ ] **🎯 Advanced Goal Tracking** - Goal achievement metrics and progress visualization
- [ ] **📊 Enhanced Analytics** - More sophisticated pattern recognition and insights
- [ ] **🔔 Smart Notifications** - Intelligent reminders based on your patterns
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
- **OpenAI** for AI capabilities and GPT-3.5-turbo integration
- **The open-source community** for inspiration and tools
- **Beta Testers** for valuable feedback and feature suggestions

