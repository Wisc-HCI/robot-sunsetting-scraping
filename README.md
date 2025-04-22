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
    sudo docker build . -t tiktokapi:latest -f TikTok.Dockerfile

    # Linux/Mac
    sudo docker run -v TikTokApi --rm  -v $(pwd):/workspace tiktokapi:latest python3 tiktok.py

    # Windows TODO
    ```

    NOTE: this often does not run due to TikTok catching bots with captchas.


* To run the Amazon scraper:
    ```bash
    sudo docker build . -t amazon -f Amazon.Dockerfile

    # Linux/Mac
    sudo docker run  --rm  -v $(pwd):/workspace  amazon python3 amazon.py

    # Windows TODO
    ```