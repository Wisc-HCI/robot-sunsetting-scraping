from TikTokApi import TikTokApi
import asyncio
import os
import json
import csv
from datetime import datetime

# This is cookie from visiting tiktok, if this doesn't work, go to tiktok and replace this
ms_token = "QFCg1Xunr-1N6uoAIxz0oJc_ufbynBiexRoSpmjVQnECB1RIbfh2UaPOsPClcCPf2B-OBWmOmGLSSYkNl5W1P1Q6H9VZ51M3vLq48xHIjp6IltUWTT370ci3YM-Jky1v3I_wy4rn7QFWyA=="


async def get_comments(video_id):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=2, sleep_after=3, browser='webkit')
        video = api.video(id=video_id)
        comments = []
        async for comment in video.comments(count=200):
            comments.append(comment.as_dict)
    
    return comments


async def get_hashtag_videos(hashtag):

    # Prep CSV file
    csv_filename = f"data/tiktok_{hashtag}.csv"
    os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
    fieldnames=["title", "author", "url", "date", "date_utc", "post_likes", "comment_count", "views", "comment", "comment_likes", "query_hashtag"]
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
    
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=2, sleep_after=3, browser='webkit')
        tag = api.hashtag(name=hashtag)

        async for video in tag.videos(count=200):
            video = video.as_dict
            # formatted_data = json.dumps(video, indent=4)

            comments = await get_comments(video['id'])
            for comment in comments:
                post_data = {
                    "title": video.get('desc', ''), 
                    "author": video['author']['uniqueId'],
                    "url": f"https://www.tiktok.com/@{video['author']['uniqueId']}/video/{video['id']}", 
                    "date": video.get('createTime', ""), 
                    "date_utc": datetime.fromtimestamp(video['createTime']).strftime('%Y-%m-%d %H:%M:%S') if "createTime" in video else None,
                    "post_likes": video.get("stats", {}).get("diggCount", 0),
                    "comment_count": video.get("stats", {}).get("commentCount", 0),
                    "views": video.get("stats", {}).get("playCount", 0),
                    "comment": comment.get("text", ""),
                    "comment_likes": comment.get("digg_count", 0),
                    "query_hashtag":hashtag,
                    
                }

                with open(csv_filename, "a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writerows([post_data])



if __name__ == "__main__":
    asyncio.run(get_hashtag_videos("moxierobot"))  