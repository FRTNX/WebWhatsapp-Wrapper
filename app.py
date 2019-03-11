#!/usr/bin/python3

import os
import json
import threading
import requests
from log import *
from flask import Flask, request, Response
from webwhatsapi import WhatsAPIDriver

application = Flask(__name__)

driver = None

@application.route('/index')
def get_numbers():
    global driver
    contacts_raw = request.args.get('contacts')
    print('Recieved contacts: {}'.format(contacts_raw))
    contacts = json.loads(contacts_raw)
    print('input type: %s' % type(contacts))
    if contacts:
        driver = WhatsAPIDriver(username="FRTNX", 
                                client='Chrome', 
                                headless=False)
        qr_string = driver.get_qr_plain()
        threading.Thread(target=run, args=(contacts,)).start()
        return qr_string
    else:
        return 'No numbers sprecified'


def run(contacts):
    print('waiting for connection')
    driver.wait_for_login()
    print('getting chats')
    chats = driver.get_all_chats()
    print(chats)
    print('finding dialogue of interest')
    for contact in contacts:
        for c in chats:
            if contact in str(c):
                chat = c
                print('dialogue search complete. found %s' % chat)
                print('loading all earlier messages')
                chat.load_all_earlier_messages()
                print('extracting all messages, self included')
                messages = chat.get_messages(include_me=True)
                print('chats extraction successful')
                processed = []
                print('beginning iteration through messages')
                for msg in messages:
                    try:
                        js = msg.get_js_obj()
                        content = js["content"]
                        timestamp = js['timestamp']
                        recipient = js['to']['user']
                        if js['sender']['isMe']:
                            sender = '%s@Grassroot' % js['sender']['id']['user']
                        else:
                            sender = js['chat']['contact']['name']
                        processed.append({'content': content,
                                        'timestamp': timestamp,
                                        'sender': sender,
                                        'recipient': recipient})
                    except KeyError:
                        f = open('errors.json', 'a')
                        f.write(json.dumps(str(msg.get_js_obj()), indent=4))
                        f.close()
                        pass
                print('iteration complete. returning result')
                print(processed)
                # response = requests.post("https://bvjaygf3qd.execute-api.eu-west-1.amazonaws.com/dev/store", 
                #                         data=json.dumps(processed))
                # print('response code: %s\nresponse content: %s' % (response.status_code, response.content))

# After data has been sent, call a lambda that will shutdown this codes host ec2 instance

if __name__ == '__main__':
    application.run(host='0.0.0.0')