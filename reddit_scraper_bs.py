# reddit_scraper_bs.py
import requests
import json
import time
import os

headers = {'User-Agent': 'Mozilla/5.0'}

def fetch_reddit_data(username, data_type="comments", limit=30):
    base_url = f"https://www.reddit.com/user/{username}/{data_type}/.json?limit={limit}"
    response = requests.get(base_url, headers=headers)
    time.sleep(1)

    if response.status_code != 200:
        print(f"Error fetching {data_type} for {username}")
        return []

    data = response.json()
    results = []
    children = data.get("data", {}).get("children", [])

    for item in children:
        entry = item.get("data", {})
        if data_type == "comments":
            results.append({
                "type": "comment",
                "text": entry.get("body", ""),
                "link": f"https://reddit.com{entry.get('permalink', '')}"
            })
        else:
            results.append({
                "type": "post",
                "title": entry.get("title", ""),
                "text": entry.get("selftext", ""),
                "link": f"https://reddit.com{entry.get('permalink', '')}"
            })

    return results

def save_user_data(username, posts, comments):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{username}_data.json", "w", encoding="utf-8") as f:
        json.dump({"posts": posts, "comments": comments}, f, indent=2)
