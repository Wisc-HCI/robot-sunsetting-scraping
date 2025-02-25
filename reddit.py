import requests
import csv
from datetime import datetime, timezone
import time
import os

subreddit = "MoxieRobot"
base_url = f"https://www.reddit.com/r/{subreddit}/.json"


csv_data = []
after = None 

while True:
    url = f"{base_url}?limit=100"  # Request up to 100 posts per call (Reddit’s max)
    if after:
        url += f"&after={after}"

    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        break
    
    data = response.json()

    posts = data["data"]["children"]
    
    for post in posts:
        post_data = {
            "title": post["data"]["title"],
            "url": post["data"]["url"],
            "date": post["data"].get("created_utc", None),
            "date_utc": datetime.fromtimestamp(post["data"]["created_utc"], timezone.utc).strftime('%Y-%m-%d %H:%M:%S') if "created_utc" in post["data"] else None
        }
        csv_data.append(post_data)

    after = data["data"].get("after")  
    if not after:
        break  

    time.sleep(2)  # Delay to prevent hitting Reddit’s rate limit

# Save to CSV
csv_filename = "data/reddit_MoxieRobot.csv"

os.makedirs(os.path.dirname(csv_filename), exist_ok=True)

with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "url", "date", "date_utc"])
    writer.writeheader()
    writer.writerows(csv_data)

print(f"Saved {len(csv_data)} posts to {csv_filename}")
