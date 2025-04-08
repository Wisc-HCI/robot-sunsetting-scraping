# Modified version of Dockerfile at https://github.com/davidteather/TikTok-Api

FROM mcr.microsoft.com/playwright:focal

RUN apt-get update && apt-get install -y python3.9 python3-pip
RUN ln -sf /usr/bin/python3.9 /usr/bin/python3  # Ensure python3 points to 3.9

RUN pip3 install TikTokApi
RUN python3 -m playwright install

WORKDIR /workspace/