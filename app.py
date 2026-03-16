from flask import Flask, render_template
import requests
import feedparser
import time

app = Flask(__name__)

# --- News sources ---
news_sources = {
    1: {"name": "Al Jazeera", "categories": {1: ("World / Global South", "https://www.aljazeera.com/xml/rss/all.xml")}},
    2: {"name": "The New York Times", "categories": {1: ("Western / US Perspective", "https://rss.nytimes.com/services/xml/rss/nyt/World.xml")}},
    3: {"name": "Nikkei Asia", "categories": {1: ("Eastern / Asia Perspective", "https://asia.nikkei.com/rss/feed/nar")}},
    4: {"name": "Nature", "categories": {1: ("Science News", "https://www.nature.com/nature.rss")}},
    5: {"name": "South China Morning Post", "categories": {1: ("China / Asia", "https://www.scmp.com/rss/91/feed")}},
    6: {"name": "Bloomberg", "categories": {1: ("Economy", "https://feeds.bloomberg.com/economics/news.rss")}},
    7: {"name": "Grist", "categories": {1: ("Environment / Climate", "https://grist.org/feed/")}},
}

# --- Feed cache ---
feed_cache = {}
CACHE_DURATION = 900  # 15 minutes

def get_feed(url):
    """Fetch RSS feed with timeout and caching."""
    now = time.time()

    # Check cache
    if url in feed_cache and now - feed_cache[url]['time'] < CACHE_DURATION:
        return feed_cache[url]['feed']

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)  # 5 second timeout
        response.raise_for_status()
        feed = feedparser.parse(response.content)
    except Exception as e:
        print(f"Warning: Could not fetch {url}: {e}")
        feed = feedparser.parse("")  # empty feed

    # Save to cache
    feed_cache[url] = {'feed': feed, 'time': now}
    return feed

# --- Routes ---
@app.route("/")
def home():
    return render_template("index.html", sources=news_sources)

@app.route("/source/<int:source_id>")
def show_articles(source_id):
    source = news_sources.get(source_id)
    if not source:
        return "Source not found", 404

    category_name, url = list(source["categories"].values())[0]
    feed = get_feed(url)

    articles = [{"title": e.title, "link": e.link} for e in feed.entries[:5]] if feed.entries else []
    return render_template("articles.html", source_name=source["name"], category_name=category_name, articles=articles)

@app.route("/headlines")
def top_headlines():
    headlines = []
    for source in news_sources.values():
        for category_name, url in source["categories"].values():
            feed = get_feed(url)
            if feed.entries:
                entry = feed.entries[0]
                headlines.append({
                    "source": source["name"],
                    "category": category_name,
                    "title": entry.title,
                    "link": entry.link
                })
            else:
                # Skip feeds with no entries
                continue
    return render_template("headlines.html", headlines=headlines)

if __name__ == "__main__":
    app.run(debug=True)