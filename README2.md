# Whatsapp Scraper API

### Installation

Before beginning please make sure to launch an instance of the Whatsapp-Scraper AMI. If an AMI is not immediately availabe see the section on Creating a New Whatsapp-Scraper AMI below.

Once that has been taken care of launch the instance and ssh into it. Ensure that the contents of the home folder are `setup.sh` and `WebWhatsapp-Wrapper`.
After this has been asserted true, stop the instance in your AWS EC2 instance panel. Once it has been stopped, select instance Actions > Instance Settings > View/Change User Data, then enter the following into the textbox in plain text mode:
```
Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash
/bin/rm /home/ubuntu/setup.sh;
/bin/echo "cd /home/ubuntu/WebWhatsapp-Wrapper; export PATH=$PATH:/home/ubuntu/WebWhatsapp-Wrapper; /usr/bin/pip3 install -r /home/ubuntu/WebWhatsapp-Wrapper/requirements.txt; /usr/bin/python3 app.py" >> /home/ubuntu/setup.sh
/bin/bash /home/ubuntu/setup.sh
--//
```

This will ensure that the API is initialised every time the instance is started up. 

### Creating a New Whatsapp-Scraper AMI

In the event that a prebuilt AMI image is not available, below are instructions on how to create one.

