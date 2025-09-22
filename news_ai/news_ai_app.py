import streamlit as st
import feedparser
import openai

# 🔑 Your OpenAI API key
openai.api_key = "your oenai key"

# Example news feeds
RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "http://feeds.reuters.com/reuters/worldNews",
]

def get_articles():
    articles = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # get top 5
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary if "summary" in entry else ""
            })
    return articles

def summarize(text):
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",   # or gpt-3.5-turbo if available
            messages=[{"role": "user", "content": f"Summarize this news in 2-3 bullet points:\n\n{text}"}],
            max_tokens=100
        )
        return resp["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.title("📰 News AI Bot (Live Summaries)")

if st.button("Fetch Latest News"):
    news = get_articles()
    for n in news:
        st.subheader(n["title"])
        st.write(f"[Read full article]({n['link']})")
        with st.spinner("Summarizing..."):
            st.info(summarize(n["summary"]))
        st.markdown("---")
