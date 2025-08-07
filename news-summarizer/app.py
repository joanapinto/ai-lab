import streamlit as st
from dotenv import load_dotenv
import os
from news_gpt import get_newsapi_articles, summarize_with_gpt

# Load API keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="News Summary with GPT", layout="wide")
st.title("🧠 News Summary with GPT")

# Helper function for summarization
def display_summary(content):
    if not OPENAI_API_KEY:
        st.info("No active OpenAI key — summary not generated.")
        return
    try:
        summary = summarize_with_gpt(content)
        st.success(summary)
    except Exception as e:
        st.error(f"Error summarizing with GPT: {e}")
        with open('error.log', 'a') as f:
            f.write(str(e) + '\n')

# Input field
query = st.text_input("Search topic:", "Artificial Intelligence")

# Button
if st.button("🔎 Search and summarize"):
    with st.spinner("Searching for articles..."):
        try:
            articles = get_newsapi_articles(query=query)
        except Exception as e:
            st.error(f"Error fetching articles: {e}")
            articles = []

    if not articles:
        st.warning("No articles found.")
    else:
        for i, article in enumerate(articles):
            st.markdown(f"### 📌 {article['title']}")
            st.markdown(f"[🔗 Link to the news]({article['url']})")

            content = article.get("content") or article.get("description") or "No content available"
            display_summary(content)
            st.divider()

# Optionally, disable the button if no API key is set
if not OPENAI_API_KEY:
    st.warning("OpenAI API key not found. Summaries will not be generated.")
