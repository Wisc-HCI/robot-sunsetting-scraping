import requests
import csv
from datetime import datetime, timezone
import time
import os
import json

subreddit = "MoxieRobot"
base_url = f"https://www.reddit.com/r/{subreddit}/.json"
headers = {"User-Agent": "Mozilla/5.0"}


after = None 

csv_filename = "data/reddit_MoxieRobot_with_comments.csv"
os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
fieldnames=["title", "text", "author", "upvotes", "url", "date", "date_utc", "comment", "comment_hierarchy"]

with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()


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
            comments = []  # Passed by reference

            def crawl_comments(comments_list:list, comment_level:list[int], comments:list[tuple[str, list[int]]]):
                """ Depth First search"""

                for comment in comments_list:
                    body = comment["data"].get("body")
                    if body:
                        comments.append((body, comment_level[:]))  # Comment_level passed by value
                        
                    replies = comment["data"].get("replies") 
                    if replies:
                        crawl_comments(replies["data"]['children'], comment_level[:] + [0], comments) # Comment_level passed by value
                    comment_level[-1] += 1
                        
            crawl_comments(comments_data[1]["data"]["children"], [0], comments)


            # Create new line for each comment
            post_list = []
            for comment_body, hierarchy in comments:
                post_data = {
                    "title": post["data"]["title"],
                    "text": post["data"].get("selftext", "").replace(",", ""), # Remove commas so doesn't mess up data
                    "author": post["data"].get("author",""),
                    "upvotes": post["data"].get("score", 0),
                    "url": post["data"]["url"],
                    "date": post["data"].get("created_utc", None),
                    "date_utc": datetime.fromtimestamp(post["data"]["created_utc"], timezone.utc).strftime('%Y-%m-%d %H:%M:%S') if "created_utc" in post["data"] else None,
                    "comment": comment_body.replace(",", ""), # Remove commas so doesn't mess up data
                    "comment_hierarchy": "C" + "-L".join(str(l) for l in hierarchy)
                }
                post_list.append(post_data)

            with open(csv_filename, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerows(post_list)


        time.sleep(0.5)  # Delay to avoid rate limits

    after = data["data"].get("after")  
    if not after:
        break  

    time.sleep(2)  # Delay between pages




print(f"Saved comments saved to {csv_filename}")
