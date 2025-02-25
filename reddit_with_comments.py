import requests
import csv
from datetime import datetime, timezone
import time
import os

subreddit = "MoxieRobot"
base_url = f"https://www.reddit.com/r/{subreddit}/.json"
headers = {"User-Agent": "Mozilla/5.0"}

csv_data = []
after = None 

while True:
    url = f"{base_url}?limit=100"
    if after:
        url += f"&after={after}"

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        break
    
    data = response.json()
    posts = data["data"]["children"]
    
    for post in posts:
        post_id = post["data"]["id"]
        post_url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}/.json"
        
        # Fetch comments
        comments_response = requests.get(post_url, headers=headers)
        if comments_response.status_code == 200:
            comments_data = comments_response.json()
            
            comments = []
            if len(comments_data) > 1:  # Comments are in the second JSON object
                for comment in comments_data[1]["data"]["children"]:
                    if "body" in comment["data"]:  # Skip deleted or removed comments
                        comments.append(comment["data"]["body"])

        # Create new line for each comment
        for comment in comments:
            post_data = {
                "title": post["data"]["title"],
                "text": post["data"].get("selftext", "").replace(",", ""), # Remove commas so doesn't mess up data
                "author": post["data"].get("author",""),
                "upvotes": post["data"].get("score", 0),
                "url": post["data"]["url"],
                "date": post["data"].get("created_utc", None),
                "date_utc": datetime.fromtimestamp(post["data"]["created_utc"], timezone.utc).strftime('%Y-%m-%d %H:%M:%S') if "created_utc" in post["data"] else None,
                "comments": comment.replace(",", "") # Remove commas so doesn't mess up data
            }

            csv_data.append(post_data)



        time.sleep(0.5)  # Delay to avoid rate limits

    after = data["data"].get("after")  
    if not after:
        break  

    time.sleep(2)  # Delay between pages

# Save to CSV
csv_filename = "data/reddit_MoxieRobot_with_comments.csv"
os.makedirs(os.path.dirname(csv_filename), exist_ok=True)

with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "text", "author", "upvotes", "url", "date", "date_utc", "comments"])
    writer.writeheader()
    writer.writerows(csv_data)

print(f"Saved {len(csv_data)} comments saved to {csv_filename}")
