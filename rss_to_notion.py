import feedparser
import requests
from datetime import datetime

NOTION_TOKEN = "secret_xxx"  # 你的 Notion Integration Token
DATABASE_ID = "xxxx-xxxx-xxxx-xxxx"  # 你的 Notion 数据库 ID

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_page_in_notion(article):
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Title": {"title": [{"text": {"content": article["title"]}}]},
            "URL": {"url": article["link"]},
            "Publisher": {"rich_text": [{"text": {"content": "NYT"}}]},
            "Published Date": {"date": {"start": article["date"]}},
            "Summary": {"rich_text": [{"text": {"content": article["summary"][:500]}}]},
            "Status": {"select": {"name": "待审核"}},
        }
    }
    r = requests.post(url, headers=headers, json=data)
    if r.status_code != 200:
        print("Error:", r.text)
    else:
        print("Inserted:", article["title"])

def fetch_rss():
    feed = feedparser.parse("https://rss.nytimes.com/services/xml/rss/nyt/RealEstate.xml")
    articles = []
    for entry in feed.entries:
        pub_date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "date": pub_date,
            "summary": entry.summary,
        })
    return articles

if __name__ == "__main__":
    for art in fetch_rss():
        create_page_in_notion(art)
