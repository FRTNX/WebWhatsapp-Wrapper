#!/bin/sh

pip install --upgrade pip
pip install -r requirements.txt
pip install webwhatsapi
pip install Flask
pip install qrcode


docker network create selenium
docker run -d -p 4444:4444 -p 5900:5900 --name firefox --network selenium -v /dev/shm:/dev/shm selenium/standalone-firefox-debug
docker build -t webwhatsapi .
docker run --network selenium -it -e SELENIUM='http://firefox:4444/wd/hub' -v $(pwd):/app  webwhatsapi /bin/bash -c "pip install ./;pip list;python sample/remote.py"
