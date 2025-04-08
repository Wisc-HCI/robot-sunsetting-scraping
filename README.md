# robot-sunsetting-scraping
Scraping for robot sunsetting data from social media

## Prerequisites
* For the reddit scripts, you just need python3.
* To run any of the tiktok scripts, you will need to install  [Docker Engine](https://docs.docker.com/engine/install/).

## Running
* To run the reddit scraper:
    ```bash
    python3 reddit_with_comments.py
    ```

* To run the tiktok scraper:
    ```bash
    docker build . -t tiktokapi:latest -f TikTok.Dockerfile

    # Linux/Mac
    sudo docker run -v TikTokApi --rm  -v $(pwd):/workspace tiktokapi:latest python3 tiktok.py

    # Windows TODO
    ```


* For the Amazon scraper, you will need to make a `.env` file in this directory with your amazon 
credentials (to get to the 2nd page of comments). This file should be in this format:
    ```bash
    AMAZON_EMAIL=YOUR_EMAIL
    AMAZON_PASSWORD=YOUR_PASSWORD
    ```

    Then to run the scraper (Recommend doing this in a venv or docker container):
    ```bash
    pip install -r requirements.txt
    python3 amazon.py

    ```



<!-- * To run the Amazon scraper:
    ```bash
    docker build . -t amazon -f Amazon.Dockerfile

    # Linux/Mac
    sudo docker run  --rm  -v $(pwd):/workspace  amazon python3 amazon.py

    # Windows TODO
    ``` -->