# scraper.py
# Fetches news from RSS feeds and NewsAPI
# RSS = free news feeds, no key needed
# NewsAPI = topic-based search, free 100/day

import feedparser
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Free RSS feeds - no API key needed
RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/rss.xml",
    "https://feeds.feedburner.com/TechCrunch",
    "https://www.theverge.com/rss/index.xml",
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "https://feeds.feedburner.com/ndtvnews-top-stories",
]

def fetch_rss_news():
    articles = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            source = feed.feed.get("title", url)
            for entry in feed.entries[:4]:
                title = entry.get("title", "").strip()
                summary = entry.get("summary", "").strip()[:400]
                link = entry.get("link", "")
                if title:
                    articles.append({
                        "title": title,
                        "summary": summary,
                        "source": source,
                        "link": link
                    })
            print(f"  ✓ {source}: fetched articles")
        except Exception as e:
            print(f"  ✗ Failed {url}: {e}")
    return articles

def fetch_newsapi_news(topics):
    articles = []
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("  ✗ NEWS_API_KEY missing")
        return articles

    for topic in topics[:3]:
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": topic,
                "language": "en",
                "sortBy": "relevancy",
                "pageSize": 5,
                "apiKey": api_key
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            if data.get("status") == "ok":
                for a in data.get("articles", []):
                    title = (a.get("title") or "").strip()
                    summary = (a.get("description") or "").strip()[:400]
                    source = a.get("source", {}).get("name", "NewsAPI")
                    link = a.get("url", "")
                    if title and "[Removed]" not in title:
                        articles.append({
                            "title": title,
                            "summary": summary,
                            "source": source,
                            "link": link
                        })
                print(f"  ✓ NewsAPI '{topic}': fetched articles")
        except Exception as e:
            print(f"  ✗ NewsAPI failed for '{topic}': {e}")
    return articles

def remove_duplicates(articles):
    unique = []
    for article in articles:
        words = set(article["title"].lower().split())
        is_dup = False
        for existing in unique:
            existing_words = set(existing["title"].lower().split())
            common = {w for w in words & existing_words if len(w) > 3}
            if len(common) > 0:
                sim = len(common) / max(len(words), len(existing_words))
                if sim > 0.6:
                    is_dup = True
                    break
        if not is_dup:
            unique.append(article)
    return unique

def get_all_news(topics):
    print("\n📡 Fetching news...")
    print("\nRSS Feeds:")
    rss = fetch_rss_news()
    print("\nNewsAPI:")
    api = fetch_newsapi_news(topics)
    all_articles = rss + api
    print(f"\nRaw articles: {len(all_articles)}")
    unique = remove_duplicates(all_articles)
    print(f"After dedup: {len(unique)} unique articles")
    return unique

# TEST - run: python scraper.py
if __name__ == "__main__":
    topics = ["AI", "cricket", "India tech"]
    articles = get_all_news(topics)
    print("\n--- SAMPLE ---")
    for i, a in enumerate(articles[:5]):
        print(f"{i+1}. [{a['source']}] {a['title']}")
    print(f"\n✓ Scraper working! {len(articles)} articles found")