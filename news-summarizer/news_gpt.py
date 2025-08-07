import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

# Get .env vars
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Font: NewsAPI ---
def get_newsapi_articles(query="artificial intelligence", language="en", max_articles=3):
    print("🔍 Getting articles from NewsAPI...")
    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&pageSize={max_articles}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("articles", [])

# --- Font: Hacker News ---
def get_hackernews_articles(keywords=["AI", "OpenAI", "LLM"], max_articles=5):
    print("🔍 Getting articles from Hacker News...")
    results = []
    base_url = "https://hn.algolia.com/api/v1/search?query={query}&tags=story"

    for keyword in keywords:
        url = base_url.format(query=keyword)
        response = requests.get(url)
        data = response.json()
        for hit in data.get("hits", []):
            results.append({
                "title": hit.get("title"),
                "url": hit.get("url") or "https://news.ycombinator.com/item?id=" + str(hit.get("objectID")),
            })

    # Removing duplicated titles
    seen = set()
    unique_results = []
    for r in results:
        if r["title"] not in seen:
            unique_results.append(r)
            seen.add(r["title"])
        if len(unique_results) >= max_articles:
            break

    return unique_results

# --- Resume with GPT ---
def summarize_with_gpt(text):
    prompt = f"""Resume in a clear and concise way the following info:

{text}

Resume:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )

    return response.choices[0].message.content.strip()

# --- APP ---
def main():
    print("🧠 Choose your news font:")
    print("1. NewsAPI")
    print("2. Hacker News")

    # Future options: Hacker News, GNews, ContextualWeb...

    choice = input("Choose (1 or 2): ")

    if choice == "1":
        articles = get_newsapi_articles()
    elif choice == "2":
        articles = get_hackernews_articles()
    else:
        print("Invalid or unavailable font.")
        return

    print("\n🔎 Resuming articles...\n")

    for i, article in enumerate(articles):
        title = article.get("title", "Untitles")
        content = article.get("content", "")
        url = article.get("url", "")


        print(f"📌 News {i+1}: {title}")
        print(f"🔗 URL: {url}")
        print(f"📝 Content:\n{content}")

        if OPENAI_API_KEY:
            try:
                resumo = summarize_with_gpt(content)
                print(f"📄 Resume:\n{resumo}")
            except Exception as e:
                print("⚠️ Failed trying to resume with GPT:", str(e))
        else:
            print("⚠️ No OpenAI key or insufficient funds - resume not generated.")

        print("-" * 60)

if __name__ == "__main__":
    main()
