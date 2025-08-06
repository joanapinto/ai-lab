# AI Lab - News Summarizer

A Python project that fetches news articles from NewsAPI and Hacker News, and summarizes them using OpenAI's GPT models.

## Features

- Fetches news articles about artificial intelligence from NewsAPI and Hacker News.
- Summarizes articles using OpenAI GPT (if API key is provided).
- Simple command-line interface and Streamlit web app.

## Requirements

- Python 3.10+
- [NewsAPI](https://newsapi.org/) API key
- [OpenAI](https://platform.openai.com/) API key (optional, for summaries)
- (Recommended) Create a virtual environment

## Installation

1. **Clone the repository:**
   ```sh
   git clone git@github.com:joanapinto/ai-lab.git
   cd ai-lab
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the project root with:
     ```
     NEWS_API_KEY=your_newsapi_key
     OPENAI_API_KEY=your_openai_key  # Optional, only if you want summaries
     ```

## Usage

### Streamlit Web App

To launch the web interface, run:
```sh
streamlit run app.py
```

- Enter your search topic in the input field (default: "Artificial Intelligence").
- Click the "🔎 Search and summarize" button.
- The app will fetch news articles and display their titles and links.
- If an OpenAI API key is set, each article will be summarized using GPT and the summary will be shown below the article.
- If no OpenAI API key is set, summaries will not be generated and a warning will be displayed.

### Command-Line Script

You can also run the script in the terminal:
```sh
python news_gpt.py
```
Follow the prompts to choose the news source and view summaries.

## Project Structure

- `app.py` — Streamlit web app for news summarization.
- `news_gpt.py` — Main script for fetching and summarizing news.
- `requirements.txt` — Python dependencies.
- `.env` — (Not committed) Your API keys.

## Notes

- The OpenAI API key is optional. If not provided, summaries will not be generated.
- The project is for educational and personal use.

## License

MIT License

## Author

Joana Pinto
