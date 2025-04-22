"""
This script parses all the amazon reviews of the Moxie robot from html pages 
(in the amazon pages folder) saved 2025-04-18 from
https://www.amazon.com/Moxie-Conversational-GPT-Powered-Articulating-Emotion-Responsive/dp/B0C1M76VR9/ref=cm_cr_arp_d_product_top?ie=UTF8.
It leaves out the 2 international reviews because they have a funky format. 
Outputs to data/amazon_reviews.csv. Review data includes title, rating, text, date, country.
user, upvotes, whether the review was sponsored (vine), and the url.
"""

from bs4 import BeautifulSoup
import csv
import re

# Clear file and write header
csv_file = 'data/amazon_reviews.csv'
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Rating', 'Text', 'Date', 'Location', 'User', 'Upvotes', 'Is Vine?' 'URL'])  # header row

review_pages = 7

for i in range(1, review_pages+1):

    
    with open(f'amazon_pages/{i}.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # First 2 are top reviews so skip in some instances

    headers = soup.select(".review-title")[2:]      
    titles = [ stripped.split("\n")[1] if "\n" in stripped else stripped
        for head in headers if (stripped := head.text.strip())]

    rating_tags = soup.select('[data-hook="review-star-rating"] .a-icon-alt')
    ratings = [tag.text for tag in soup.select('[data-hook="review-star-rating"] .a-icon-alt')]

    texts = [text.text.strip() for text in soup.select(".review-text")]

    location_dates = [date.text.strip() for date in soup.select(".review-date")[2:]]
    locations = []
    dates = []
    for date_loc in location_dates:
        match = re.search(r"Reviewed in (.+?) on (.+)", date_loc)

        locations.append(match.group(1))
        dates.append(match.group(2))


    aria_labels = soup.find_all('a', attrs={'aria-label': True})
    users = [ tag['aria-label'].replace("Report review by ", "").strip() for tag in aria_labels
        if tag['aria-label'].startswith("Report review by ")]


    reviews = soup.select('[data-hook="review"]')
    upvotes = []
    is_vines = []
    for review in reviews:
        vote_span = review.select_one('[data-hook="helpful-vote-statement"]')
        if vote_span:
            # Extract digits from string like "44 people found this helpful"
            match = re.search(r'(\d+)', vote_span.text)
            count = int(match.group(1)) if match else 0
        else:
            count = 0
        upvotes.append(count)

        review_text = review.get_text().lower()  # Make it lowercase for easy matching
        is_vine = "vine" in review_text
        is_vines.append(is_vine)



    urls = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/gp/customer-reviews/')]
    base_url = "https://www.amazon.com"
    full_urls = [base_url + link for link in urls[2:]]





    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)

        for i in range(len(titles)):
            writer.writerow([titles[i], ratings[i], texts[i], dates[i], locations[i], users[i], upvotes[i], is_vines[i], full_urls[i]])
    
    print(f"Scraping page {i}. Total reviews: {len(titles)}.")


print(f"CSV file {csv_file} created successfully.")