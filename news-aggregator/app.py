import os
import feedparser
from flask import Flask, render_template, request
from dotenv import load_dotenv
from urllib.parse import urlparse
import time
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# --- Configuration ---
DEFAULT_FEEDS = [
    'https://feeds.bbci.co.uk/news/rss.xml',
    'http://rss.slashdot.org/Slashdot/slashdotMain'
]
RSS_FEEDS_STR = os.getenv('RSS_FEEDS')
if RSS_FEEDS_STR:
    FEEDS = [feed.strip() for feed in RSS_FEEDS_STR.split(',')]
else:
    FEEDS = DEFAULT_FEEDS

# --- Pre-load Feed Details (for the dropdown menu) ---
# This is more efficient than fetching titles on every request.
def get_feed_details(url):
    """Fetches the title for a given feed URL."""
    try:
        feed = feedparser.parse(url)
        return {
            'url': url,
            'title': feed.feed.get('title', urlparse(url).netloc) # Fallback to domain name
        }
    except Exception as e:
        print(f"Could not fetch details for {url}: {e}")
        return {'url': url, 'title': urlparse(url).netloc}

print("Fetching feed details for the filter menu...")
FEEDS_WITH_DETAILS = [get_feed_details(url) for url in FEEDS]
print("Done.")


# --- Helper Functions ---
def get_favicon_url(feed_url):
    """Constructs a URL to fetch the favicon for a given feed URL."""
    domain = urlparse(feed_url).netloc
    return f"https://www.google.com/s2/favicons?domain={domain}&sz=32"

def fetch_articles(selected_feed_url=None):
    """
    Fetches articles. If a selected_feed_url is provided,
    it fetches only from that feed. Otherwise, it fetches from all feeds.
    """
    articles = []
    
    # Determine which feeds to process
    feeds_to_process = [selected_feed_url] if selected_feed_url else FEEDS

    for url in feeds_to_process:
        try:
            print(f"Fetching feed: {url}")
            feed = feedparser.parse(url)
            source_title = feed.feed.get('title', 'Unknown Source')
            source_icon = get_favicon_url(url)

            for entry in feed.entries:
                articles.append({
                    'title': entry.get('title', 'No Title'),
                    'link': entry.get('link', '#'),
                    'summary': entry.get('summary', ''),
                    'published_parsed': entry.get('published_parsed', time.gmtime()),
                    'source_title': source_title,
                    'source_icon': source_icon
                })
        except Exception as e:
            print(f"Error fetching or parsing feed {url}: {e}")

    # Sort articles by publication date, newest first
    articles.sort(key=lambda x: x['published_parsed'], reverse=True)
    return articles

@app.template_filter('datetimeformat')
def format_datetime(value):
    """Jinja2 filter to format a time.struct_time into a readable string."""
    if not value:
        return ""
    dt_object = datetime.fromtimestamp(time.mktime(value))
    return dt_object.strftime('%a, %d %b %Y %H:%M')


# --- Routes ---
@app.route('/')
def index():
    """Main route to display the news aggregator with filtering."""
    # Get the selected feed from URL query parameter (e.g., /?feed=...)
    selected_feed = request.args.get('feed')
    
    # Validate that the selected feed is in our configured list
    if selected_feed and selected_feed not in FEEDS:
        # Optional: Handle invalid feed parameter, e.g., redirect or show an error
        selected_feed = None 

    articles = fetch_articles(selected_feed)

    # Determine the page title based on the filter
    page_title = "All News"
    if selected_feed:
        # Find the title from our pre-loaded details
        for feed_info in FEEDS_WITH_DETAILS:
            if feed_info['url'] == selected_feed:
                page_title = feed_info['title']
                break

    return render_template(
        'index.html',
        articles=articles,
        feeds=FEEDS_WITH_DETAILS,
        selected_feed=selected_feed,
        page_title=page_title
    )

if __name__ == '__main__':
    app.run(debug=True)