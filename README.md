# Robot-Sunsetting Scraping
This is collection of scripts for scraping Reddit, Amazon, and Tiktok for data for Moxie Robot. Please see the comment headers in reddit.py, amazon.py, or tiktok.py for more details about what each script does.

## Prerequisites
* For the Reddit scripts, you just need python3.
* To run any of the Tiktok or Amazon scripts, you will need to install [Docker Engine](https://docs.docker.com/engine/install/).

## Running
* To run the reddit scraper:
    ```bash
    python3 reddit_with_comments.py
    ```


* To run the Amazon scraper:
    
    First build the container:
    ```bash
    sudo docker build . -t amazon -f Amazon.Dockerfile
    ```

    Next, run one of these:
    ```bash
    # Linux/Mac Bash
    sudo docker run  --rm  -v $(pwd):/workspace  amazon python3 amazon.py

    # Windows Powershell
    sudo docker run  --rm  -v ${PWD}:/workspace  amazon python3 amazon.py
    ```


* To run the Tiktok scraper:
    
    First build the container:
    ```bash
    sudo docker build . -t tiktokapi:latest -f TikTok.Dockerfile
    ```

    Next, run one of these:
    ```bash
    # Linux/Mac Bash
    sudo docker run -v TikTokApi --rm  -v $(pwd):/workspace tiktokapi:latest python3 tiktok.py

    # Windows PowerShell
    docker run --rm -v ${PWD}:/workspace tiktokapi:latest python tiktok.py
    ```

