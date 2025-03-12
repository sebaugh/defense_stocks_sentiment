### libraries
from dotenv import load_dotenv
import os
import requests
import json

### load .env vars
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

if not API_KEY:
    raise ValueError("Missing API! Add API to .env file")

### def query for NewsAPI
QUERY = "defense industry OR war OR peace talks"
URL = f"https://newsapi.org/v2/everything?q={QUERY}&language=en&sortBy=publishedAt&apiKey={API_KEY}"



def get_news():
    """Downloads news from NEWSapi and number of repetitions"""
    response = requests.get(URL)
    data = response.json()

    if "articles" in data:
        articles = {}
        
        for article in data["articles"]:
            title = article["title"]
            description = article["description"] or "no description"
            url = article["url"]
            published_at = article["publishedAt"]

            if title in articles:
                articles[title]["count"] += 1  # add count
            else:
                articles[title] = {
                    "title": title,
                    "description": description,
                    "url": url,
                    "published_at": published_at,
                    "count": 1  # first count
                }

        return list(articles.values())
    else:
        print("Error during download:", data)
        return []
    
def save_news(news, filename="news.json"):
    """Save found news to a json file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(news, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    news = get_news()
    if news:
        save_news(news)
        print(f"Found {len(news)} news saved to news.json")
    else:
        print("No news found.")