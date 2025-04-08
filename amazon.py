"""
NOTE: Amazon changes it's webpage often, so this script might
not work long after April 2025.
"""

from bs4 import BeautifulSoup
import requests


url = 'https://www.amazon.com/Moxie-Conversational-GPT-Powered-Articulating-Emotion-Responsive/dp/B0C1M76VR9'
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

print(soup)
titles = [title.text.strip() for title in soup.select(".review-title")]
print(titles)

