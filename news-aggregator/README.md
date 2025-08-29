# Flask News Aggregator

A simple, clean, and modern news aggregator web application built with Flask and Bootstrap 5. It fetches the latest articles from a customizable list of RSS feeds and displays them in a unified, reverse-chronological order.



## Features

-   **Multiple Feeds**: Fetches articles from any number of RSS/Atom feeds.
-   **Unified Timeline**: Merges all articles and sorts them by publication date, newest first.
-   **Clean UI**: Uses Bootstrap 5 for a modern, responsive, and card-based layout that looks great on desktop and mobile.
-   **Source Identification**: Displays the source name and favicon for each article, making it easy to see where news is coming from.
-   **Easy Configuration**: Add, remove, or change RSS feeds by simply editing a `.env` file.
-   **Lightweight**: No database required. It fetches live data on each request.

## Technologies Used

-   **Backend**: [Flask](https://flask.palletsprojects.com/)
-   **RSS Parsing**: [feedparser](https://pypi.org/project/feedparser/)
-   **Configuration**: [python-dotenv](https://pypi.org/project/python-dotenv/)
-   **Frontend**: [Bootstrap 5](https://getbootstrap.com/), HTML5, CSS3

## Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

-   Python 3.7+
-   pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/azario0/flask-news-aggregator.git
    cd flask-news-aggregator
    ```

2.  **Create and activate a virtual environment:**
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

The application is configured using a `.env` file in the project's root directory.

1.  Create a file named `.env`:
    ```bash
    touch .env
    ```

2.  Add your desired RSS feeds to the `.env` file. The feeds should be in a single line, separated by commas, with no spaces around the commas.

    **`.env` example:**
    ```
    RSS_FEEDS=https://feeds.bbci.co.uk/news/rss.xml,http://rss.slashdot.org/Slashdot/slashdotMain,https://www.theverge.com/rss/index.xml,https://hn.svelte.dev/rss
    ```
    You can find RSS feeds for most news sites, blogs, and publications by searching online for "[website name] RSS feed".

## Running the Application

Once you have installed the dependencies and configured your feeds, you can run the app with a single command:

```bash
flask run
```

The application will be available at `http://127.0.0.1:5000`. Open this URL in your web browser to see your news feed!

## Future Improvements

This is a simple implementation and can be extended in many ways. Here are a few ideas:

-   **Caching**: Implement a caching layer (e.g., using `Flask-Caching`) to store fetched articles for a few minutes. This would dramatically improve performance and reduce redundant requests to the feed sources.
-   **Background Worker**: Use a task queue like Celery or a scheduler like APScheduler to fetch feeds periodically in the background. The web application would then read from a local data store, making page loads instantaneous.
-   **Database Integration**: Store articles in a database (like SQLite or PostgreSQL) to build a history, mark articles as read, and allow for searching and filtering.
-   **User Accounts**: Allow users to register and manage their own list of RSS feed subscriptions.
-   **OPML Import/Export**: Add a feature to import and export feed lists using the standard OPML file format.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.