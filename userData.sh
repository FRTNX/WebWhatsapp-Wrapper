#!/bin/bash
/bin/rm /home/ubuntu/setup.sh;
/bin/echo "cd /home/ubuntu/WebWhatsapp-Wrapper; export PATH=$PATH:/home/ubuntu/WebWhatsapp-Wrapper; /usr/bin/pip3 install -r /home/ubuntu/WebWhatsapp-Wrapper/requirements.txt; /usr/bin/python3 app.py" >> /home/ubuntu/setup.sh
/bin/bash /home/ubuntu/setup.sh
