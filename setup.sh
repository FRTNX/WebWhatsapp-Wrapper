#!/bin/sh

# initial setup
sudo apt-get update
sudo apt install python-pip
sudo apt-get -y install python3-pip

# Setup repo
git clone https://github.com/FRTNX/WebWhatsapp-Wrapper
cd WebWhatsapp-Wrapper

# Install python dependencies
pip3 install -r requirements.txt
pip3 install flask requests
pip3 install python-axolotl
sudo pip3 install python-magic
pip3 install numpy

# Setup docker environment
sudo apt install docker.io
pip install webwhatsapi
sudo docker network create selenium
sudo docker run -d -p 4444:4444 -p 5900:5900 --name firefox --network selenium -v /dev/shm:/dev/shm selenium/standalone-firefox-debug
sudo docker build -t webwhatsapi .
sudo docker run --network selenium -it -e SELENIUM='http://firefox:4444/wd/hub' -v $(pwd):/app  webwhatsapi /bin/bash -c "pip install ./;pip list;python sample/remote.py"

# Install Firefox
sudo apt-get purge firefox
sudo apt-get install firefox
wget sourceforge.net/projects/ubuntuzilla/files/mozilla/apt/pool/main/f/firefox-mozilla-build/firefox-mozilla-build_61.0.2-0ubuntu1_amd64.deb
sudo dpkg -i firefox-mozilla-build_61.0.2-0ubuntu1_amd64.deb
firefox --version

# The console output of app.py is output to /var/log/cloud-init-output.log at run-time
# You're welcome
