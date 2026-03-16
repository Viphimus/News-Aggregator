from flask import Flask, render_template
import requests
import feedparser

app = Flask(__name__)

news_sources = {
    1: {
        "name": "Al Jazeera",
        "categories": {
            1: ("World / Global South", "https://www.aljazeera.com/xml/rss/all.xml")
        }
    },
    2: {
        "name": "The New York Times",
        "categories": {
            1: ("Western / US Perspective", "https://rss.nytimes.com/services/xml/rss/nyt/World.xml")
        }
    },
    3: {
        "name": "Nikkei Asia",
        "categories": {
            1: ("Eastern / Asia Perspective", "https://asia.nikkei.com/rss/feed/nar")
        }
    },
    4: {
        "name": "Nature",
        "categories": {
            1: ("Science News", "https://www.nature.com/nature.rss")
        }
    },
    5: {
        "name": "South China Morning Post",
        "categories": {
            1: ("China / Asia", "https://www.scmp.com/rss/91/feed")
        }
    },
    6: {
        "name": "Bloomberg",
        "categories": {
            1: ("Economy", "https://feeds.bloomberg.com/economics/news.rss")
        }
    },
    7: {
        "name": "Grist",
        "categories": {
            1: ("Environment / Climate", "https://grist.org/feed/")
        }
    }
}


def get_feed(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    return feedparser.parse(response.content)


@app.route("/")
def home():
    return render_template("index.html", sources=news_sources)


@app.route("/source/<int:source_id>")
def show_articles(source_id):

    source = news_sources[source_id]
    category_name, url = list(source["categories"].values())[0]

    feed = get_feed(url)

    articles = []

    for entry in feed.entries[:5]:
        articles.append({
            "title": entry.title,
            "link": entry.link
        })

    return render_template(
        "articles.html",
        source_name=source["name"],
        category_name=category_name,
        articles=articles
    )


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

    return render_template("headlines.html", headlines=headlines)


if __name__ == "__main__":
    if __name__ == "__main__":
        app.run()