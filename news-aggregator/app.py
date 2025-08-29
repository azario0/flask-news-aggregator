import os
import feedparser
from flask import Flask, render_template
from dotenv import load_dotenv
from urllib.parse import urlparse
import time
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# --- Configuration ---
# Get RSS feeds from .env file, with a fallback to default feeds
DEFAULT_FEEDS = [
    'https://feeds.bbci.co.uk/news/rss.xml',
    'http://rss.slashdot.org/Slashdot/slashdotMain'
]
RSS_FEEDS_STR = os.getenv('RSS_FEEDS')
if RSS_FEEDS_STR:
    FEEDS = [feed.strip() for feed in RSS_FEEDS_STR.split(',')]
else:
    FEEDS = DEFAULT_FEEDS

# --- Helper Functions ---
def get_favicon_url(feed_url):
    """Constructs a URL to fetch the favicon for a given feed URL."""
    domain = urlparse(feed_url).netloc
    # Using Google's S2 service is a reliable way to get favicons
    return f"https://www.google.com/s2/favicons?domain={domain}&sz=32"

def fetch_articles():
    """Fetches and parses articles from all configured RSS feeds."""
    articles = []
    for url in FEEDS:
        try:
            print(f"Fetching feed: {url}")
            feed = feedparser.parse(url)
            source_title = feed.feed.get('title', 'Unknown Source')
            source_icon = get_favicon_url(url)

            for entry in feed.entries:
                # Use entry.get() to avoid errors if a field is missing
                articles.append({
                    'title': entry.get('title', 'No Title'),
                    'link': entry.get('link', '#'),
                    'summary': entry.get('summary', ''),
                    # published_parsed is a time.struct_time object
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
    # Convert time.struct_time to datetime object
    dt_object = datetime.fromtimestamp(time.mktime(value))
    return dt_object.strftime('%a, %d %b %Y %H:%M')


# --- Routes ---
@app.route('/')
def index():
    """Main route to display the news aggregator."""
    # Note: In a production app, you'd want to cache this result
    # to avoid fetching on every single page load.
    articles = fetch_articles()
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)