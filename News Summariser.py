import requests
import feedparser
import webbrowser

# News sources and RSS feeds
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
     },
}


def get_feed(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        if not feed.entries:
            print("Warning: No articles found in this feed.")
        return feed
    except Exception as e:
        print(f"Error fetching feed: {e}")
        return feedparser.parse("")  # empty feed

def show_top_headlines_all_sources():
    print("\n===== TOP HEADLINE FROM EACH SOURCE =====\n")
    for source in news_sources.values():
        for cat_name, feed_url in source["categories"].values():
            feed = get_feed(feed_url)
            if feed.entries:
                entry = feed.entries[0]
                print(f"{source['name']} - {cat_name}")
                print(f"Title: {entry.title}")
                print(f"Link: {entry.link}\n")
            else:
                print(f"{source['name']} - {cat_name}: No articles found.\n")

print("Welcome to Global News Aggregator!\n")

while True:
    # --- Step 1: Choose news source or view top headlines ---
    while True:
        print("Menu:")
        print("0. Show top headline from all sources")
        for key, source in news_sources.items():
            print(f"{key}. {source['name']}")
        try:
            source_choice = int(input("Pick a news source (0 for top headlines, 8 to exit): "))
            if source_choice == 8:
                print("Goodbye!")
                exit()
            elif source_choice == 0:
                show_top_headlines_all_sources()
                break
            elif source_choice in news_sources:
                source = news_sources[source_choice]
                break
            else:
                print("Invalid choice. Enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    if source_choice == 0:
        continue  # after top headlines, go back to menu

    # --- Step 2: Choose category (most sources have 1 category) ---
    categories = source["categories"]
    if len(categories) == 1:
        cat_choice = list(categories.keys())[0]
        print(f"\nSelected category: {categories[cat_choice][0]}")
    else:
        while True:
            print(f"\nCategories for {source['name']}:")
            for key, (cat_name, _) in categories.items():
                print(f"{key}. {cat_name}")
            try:
                cat_choice = int(input("Pick a category (0 to go back to sources): "))
                if cat_choice == 0:
                    break
                if cat_choice in categories:
                    break
                print("Invalid choice. Please enter a valid category number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    if cat_choice == 0:
        continue  # back to source selection

    category_name, feed_url = categories[cat_choice]
    feed = get_feed(feed_url)
    feed_date = getattr(feed.feed, 'updated', 'No date available')
    print(f"\n===== {source['name']} - {category_name.upper()} =====\nLast Updated: {feed_date}\n")

    # --- Display top 5 articles ---
    articles = []
    for i, entry in enumerate(feed.entries[:5], 1):
        title = entry.title
        link = entry.link
        articles.append(link)
        print(f"{i}. {title}")

    if not articles:
        print("No articles available for this feed.")

    # --- Option to open an article ---
    while articles:
        try:
            open_choice = int(input("\nEnter the number of the article to open (0 to skip): "))
            if open_choice == 0:
                break
            elif 1 <= open_choice <= len(articles):
                webbrowser.open(articles[open_choice - 1])
                print("Opening article in your browser...")
                break
            else:
                print(f"Invalid input. Enter a number from 1 to {len(articles)}, or 0 to skip.")
        except ValueError:
            print(f"Invalid input. Enter a number from 1 to {len(articles)}, or 0 to skip.")

    print("\n")  # spacing before next loop