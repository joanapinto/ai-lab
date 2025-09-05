# 🤖 AI Features Setup Guide

The Humsy app now includes AI-powered personalized greetings and responses! Here's how to enable them.

## 🚀 Quick Setup

### 1. Get an OpenAI API Key

1. Go to [OpenAI's API Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to "API Keys" in the sidebar
4. Click "Create new secret key"
5. Copy your API key (it starts with `sk-`)

### 2. Set Up Your API Key

**Option A: Environment Variable (Recommended)**
```bash
# On macOS/Linux
export OPENAI_API_KEY="your-api-key-here"

# On Windows (Command Prompt)
set OPENAI_API_KEY=your-api-key-here

# On Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"
```

**Option B: .env File**
1. Create a `.env` file in the `focus-companion` directory
2. Add your API key:
```
OPENAI_API_KEY=your-api-key-here
```

### 3. Test the Setup

Run the app to verify everything works:
```bash
streamlit run app.py
```

If you see AI-generated responses in the greetings and tips, you're all set! If you see rule-based responses, check that your API key is set correctly.

## 🎯 What AI Features Are Available?

### ✅ Currently Implemented
- **Personalized Greetings**: AI-generated greetings that consider your mood, energy, and recent patterns
- **Daily Encouragement**: Personalized motivational messages based on your goals and preferences
- **Productivity Tips**: Context-aware tips that consider your energy drainers and situation

### 🔄 How It Works
1. **AI First**: The app tries to generate AI responses using your data
2. **Graceful Fallback**: If AI is unavailable, it uses intelligent rule-based responses
3. **No Data Loss**: Your experience remains consistent regardless of AI availability

## 💰 Cost Considerations

- **GPT-3.5-turbo**: ~$0.002 per 1K tokens (very affordable)
- **Typical Usage**: ~50-100 tokens per greeting/response
- **Estimated Cost**: Less than $1/month for regular use

## 🔒 Privacy & Security

- **Local Processing**: Your data stays on your device
- **Minimal API Calls**: Only essential context is sent to OpenAI
- **No Data Storage**: OpenAI doesn't store your personal data
- **Optional Feature**: AI can be disabled by not setting the API key

## 🛠️ Troubleshooting

### "OpenAI API key not found"
- Check that your API key is set correctly
- Verify the environment variable or .env file
- Restart your terminal/application

### "Error generating AI greeting"
- Check your internet connection
- Verify your OpenAI account has credits
- Check the OpenAI status page for service issues

### Rule-based responses only
- This is normal when AI is unavailable
- The app will work perfectly with rule-based responses
- Check your API key setup if you want AI features

## 🎉 Ready to Go!

Once you've set up your API key, the app will automatically:
- Generate personalized greetings based on your mood and patterns
- Provide context-aware encouragement
- Give tailored productivity tips
- Fall back gracefully if AI is unavailable

Your Humsy will feel more personal and responsive than ever! 🚀 