# Weekly Coach GPT

An AI-powered personal coach that helps you achieve your goals through personalized weekly planning, daily check-ins, and intelligent progress tracking.

## 🚀 Features

- **🎯 Goal Setting & Setup** - Define your main objective and preferences
- **📋 Weekly Planning** - AI-generated personalized weekly plans
- **🌤️ Daily Check-ins** - Track progress and get motivational guidance
- **📝 Weekly Reflections** - Review your week and learn from patterns
- **📊 Progress Tracking** - Visual progress metrics and achievements
- **🧠 Smart Insights** - AI-generated insights based on your patterns
- **🏆 Achievement System** - Unlock badges as you progress

## 🎯 How It Works

1. **Setup** - Tell us about your goals and preferences
2. **Plan** - Generate personalized weekly plans
3. **Check-in** - Daily progress updates and motivation
4. **Reflect** - Weekly reviews and insights
5. **Grow** - Track progress and celebrate achievements

## 📋 Requirements

- Python 3.10+
- [OpenAI](https://platform.openai.com/) API key
- Streamlit

## 🛠️ Installation

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd weekly-coach
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Copy the example environment file and add your API keys:
   ```sh
   cp .env.example .env
   ```
   Then edit `.env` and add your actual API keys:
   ```
   OPENAI_API_KEY=your_openai_key
   ```

## 🚀 Usage

### Start the Application
```sh
streamlit run main.py
```

### Navigation Structure
- **🏠 Main Dashboard** - Overview and quick actions
- **🎯 Setup** - Configure your goals and preferences
- **📋 Weekly Plan** - Create and view weekly plans
- **🌤️ Daily Check-in** - Daily progress tracking
- **📝 Reflection** - Weekly reviews and insights
- **📊 Progress** - View detailed progress metrics
- **📚 History** - View past plans and check-ins
- **🔧 Settings** - Manage your preferences
- **❓ Help** - Tips and troubleshooting

## 🎯 First-Time User Guide

1. **Welcome Screen** - Learn about the app and see demo features
2. **Setup** - Complete the guided setup process
3. **Create Your First Plan** - Generate a personalized weekly plan
4. **Start Daily Check-ins** - Begin tracking your progress
5. **Weekly Reflection** - Review your week and get insights

## 📊 Progress Tracking

The app automatically tracks:
- **Total check-ins** and weeks
- **Completion rates** for tasks
- **Streak days** of consistent check-ins
- **Achievement badges** for milestones
- **Pattern insights** from your behavior

## 🏆 Achievement System

Unlock badges as you progress:
- 🎯 **Week Warrior** - Complete 7 daily check-ins
- 🔥 **Streak Master** - Maintain a 5+ day streak
- ✅ **High Achiever** - Maintain 80%+ completion rate
- 📅 **Monthly Planner** - Complete 4 weeks of planning

## 🧠 Smart Features

- **Personalized Coaching** - Adapts to your preferred style
- **Context Awareness** - Remembers your current week's plan
- **Pattern Recognition** - Learns from your success patterns
- **Intelligent Insights** - Provides actionable advice
- **Progress Analytics** - Visual progress tracking

## 📁 Project Structure

```
weekly-coach/
├── main.py                 # Main dashboard
├── pages/                  # Multi-page structure
│   ├── 1_Setup.py         # User setup and preferences
│   ├── 2_Weekly_Plan.py   # Weekly plan generation
│   ├── 3_Daily_Checkin.py # Daily check-in interface
│   ├── 4_Reflection.py    # Weekly reflection
│   ├── 5_Progress.py      # Progress tracking
│   ├── 6_Settings.py      # User settings
│   ├── 7_History.py       # View history
│   └── 8_Help.py          # Help and tips
├── coach.py               # Core AI coaching functions
├── setup.py               # Setup utilities
├── prompts/               # AI prompt templates
├── logs/                  # User data storage
└── user_profile.json      # User profile and preferences
```

## 💡 Tips for Success

- **Be Specific** - Set clear, measurable goals
- **Check in Daily** - Build momentum with regular check-ins
- **Be Honest** - Accurate feedback leads to better guidance
- **Stay Flexible** - Plans can be adjusted as needed
- **Celebrate Wins** - Acknowledge your progress

## 🔧 Troubleshooting

**Common Issues:**
- "No weekly plan found" → Create your first plan
- "Please complete setup first" → Go through the setup process
- API errors → Check your API keys and internet connection

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome!

## 📄 License

MIT License

---

**Weekly Coach GPT** - Your AI-powered personal coach for goal achievement and productivity! 🚀 