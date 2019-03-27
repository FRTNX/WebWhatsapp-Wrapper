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

* Before you begin please make sure to have an EC2 security group that allows traffic through HTTP, HTTPS AND SSH  as well as a Custom TCP Rule accepting traffic from anywhere on port 5000. The security group should at least have the following entries:

IMAGE

* Also, be sure to have an ssh key pair in the same region as the one you plan on launching your EC2 instance from.
For information on how to create such a security group, please see [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-network-security.html).

1. Open your AWS EC2 management console and select Launch Instance.
2. You be prompted to choose a base image. select Ubuntu Server 16.04 LTS (HVM), SSD Volume Type 64 bit (x86). It is free tier eligable.
3. Under Instance Type select the default t2.micro then select the Review and Launch button.
4. Under Review Instance Launch select Edit Security Groups. 
5. Under Configure Security Group, Select an existing security group, and select your EC2 security group described at the beginning of this section. Then select Review and Launch.
6. Select `Launch`
7. Voila! You have created the perfect EC2 instance for what is to come.



### The Three Lambdas


