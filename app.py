#!/usr/bin/python3

import os
import sys
import json
import threading
import requests
from flask import Flask, request, Response, copy_current_request_context
from webwhatsapi import WhatsAPIDriver

application = Flask(__name__)

driver = None

@application.route('/index')
def get_numbers():
    global driver

    contacts_raw = request.args.get('contacts')
    print('Recieved contacts: {}'.format(contacts_raw), file=sys.stderr)
    contacts = json.loads(contacts_raw.replace('"', ''))
    print('input type: %s' % type(contacts), file=sys.stderr)

    if contacts:
        driver = WhatsAPIDriver(username="FRTNX", 
                                client='Firefox', 
                                headless=True)
        qr_string = driver.get_qr_plain()

        @copy_current_request_context
        def run(contacts):
            # TODO: validate that contacts is of type list
            print('waiting for connection', file=sys.stderr)
            driver.wait_for_login()
            print('getting chats', file=sys.stderr)
            chats = driver.get_all_chats()
            print(chats)
            print('finding dialogue of interest', file=sys.stderr)
            for contact in contacts:
                print('Now searching for %s in in contacts' % contact, file=sys.stderr)
                for c in chats:
                    if str(contact) in str(c):
                        chat = c
                        print('dialogue search complete. found %s' % chat, file=sys.stderr)
                        print('loading all earlier messages', file=sys.stderr)
                        chat.load_all_earlier_messages()
                        print('extracting all messages, self included', file=sys.stderr)
                        messages = chat.get_messages(include_me=True)
                        print('chats extraction successful', file=sys.stderr)
                        processed = []
                        print('beginning iteration through messages', file=sys.stderr)
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
                        print('iteration complete. returning result', file=sys.stderr)
                        print(processed, file=sys.stderr)
                        # response = requests.post("https://bvjaygf3qd.execute-api.eu-west-1.amazonaws.com/dev/store", 
                        #             data=json.dumps(processed))
                        # print('response code: %s\nresponse content: %s' % (response.status_code, response.content))
            shutdown_req = request.get("https://ii8i6r3mcd.execute-api.us-east-1.amazonaws.com/dev/stop_whatsapp_scraper")
            print(shutdown_req.content, file=sys.stderr)
            
        threading.Thread(target=run, args=(contacts,)).start()
        return qr_string
    else:
        return 'No numbers sprecified'


if __name__ == "__main__":
    application.run(host='0.0.0.0')
