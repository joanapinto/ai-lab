# 🧪 AI QA Assistant for Devs & Small Teams

An intelligent AI-powered tool that generates comprehensive testing strategies, test cases, and Playwright code snippets based on your project structure and description.

## ✨ Features

### 🤖 AI-Powered Analysis
- **Project Structure Analysis** - Upload your project ZIP file for detailed code analysis
- **Intelligent Test Strategy** - Get tailored testing recommendations based on your tech stack
- **Edge Case Detection** - Identify potential failure scenarios and critical edge cases
- **Playwright Code Generation** - Receive ready-to-use Playwright test snippets

### 📁 Multiple Input Methods
- **📁 Upload Project** - Upload a zipped version of your project folder
- **✍️ Manual Description** - Describe your project manually for quick recommendations

### 🎯 Comprehensive Output
- **Testing Strategy** - Overall approach and focus areas
- **Test Cases** - Core functionality and user flow scenarios
- **Playwright Code Snippets** - Practical examples and setup instructions
- **⚠️ Edge Cases & Failure Scenarios** - Critical failure points and unusual scenarios

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd qa-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 📖 Usage

### Method 1: Upload Project
1. Go to the **"📁 Upload Project"** tab
2. Click **"Choose a ZIP file"** and select your project folder
3. The AI will analyze your project structure and generate recommendations
4. Review the comprehensive QA strategy and test cases

### Method 2: Manual Description
1. Go to the **"✍️ Manual Description"** tab
2. Describe your project in detail (features, technologies, functionality)
3. Click **"🚀 Generate QA Strategy"**
4. Receive tailored testing recommendations

## 🎯 What You'll Get

### Testing Strategy
- Recommended testing approaches for your specific project
- Key areas to focus on based on your tech stack
- Integration and end-to-end testing suggestions

### Test Cases
- Core functionality test scenarios
- User flow test cases
- Integration test examples

### Playwright Code Snippets
- Ready-to-use Playwright test examples
- Setup and configuration instructions
- Best practices for your project type

### Edge Cases & Failure Scenarios
- **Critical edge cases** that could cause major failures
- **Unusual user behaviors** that might break the application
- **Data edge cases** (empty inputs, very long inputs, special characters)
- **Performance edge cases** (large datasets, slow network conditions)
- **Security edge cases** (malicious inputs, unauthorized access attempts)
- **Integration edge cases** (API failures, database connection issues)

## 🛠️ Project Structure

```
qa-assistant/
├── app.py                 # Main Streamlit application
├── assistant.py           # OpenAI integration and AI logic
├── repo_parser.py         # Project file analysis
├── prompts/
│   └── ai_qa_assistant.txt # AI prompt template
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Supported File Types
The tool analyzes the following file types:
- JavaScript (`.js`, `.jsx`)
- TypeScript (`.ts`, `.tsx`)
- Python (`.py`)
- HTML (`.html`)
- CSS (`.css`)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the web interface
- Powered by [OpenAI GPT](https://openai.com/) for intelligent analysis
- Inspired by the need for better QA practices in small development teams

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section below
2. Open an issue on GitHub
3. Review the project documentation

## 🔍 Troubleshooting

### Common Issues

**"OpenAI API key not found"**
- Ensure your `.env` file exists and contains a valid `OPENAI_API_KEY`
- Verify the API key is active and has sufficient credits

**"Error analyzing project"**
- Make sure your ZIP file contains a valid project structure
- Check that the ZIP file isn't corrupted
- Ensure the project contains supported file types

**"No files found to analyze"**
- Verify your project contains files with supported extensions
- Check that the ZIP file extraction was successful

### Performance Tips
- Keep project ZIP files under 50MB for faster analysis
- Provide detailed project descriptions for better recommendations
- Use the manual description method for quick testing scenarios

---

**Made with ❤️ for developers who care about quality**
