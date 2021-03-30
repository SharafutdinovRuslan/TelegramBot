FROM ubuntu:20.04


RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.8 \
    python3-pip

WORKDIR /usr/src/backend

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt
