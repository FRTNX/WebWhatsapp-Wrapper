#!/usr/bin/python3

import os
# os.system('sudo pkill -f firefox')
from flask import Flask, request
from webwhatsapi import WhatsAPIDriver

application = Flask(__name__)

driver = None

@application.route('/index')
def get_numbers():
    global driver
    contacts = request.args.get('contacts')
    print('Recieved contacts: {}'.format(contacts))
    if contacts:
        driver = WhatsAPIDriver(username="FRTNX", 
                                client='Firefox', 
                                headless=True)
        qr_string = driver.get_qr_plain()
        return qr_string
    else:
        return 'No numbers sprecified'

if __name__ == '__main__':
    application.run(host='0.0.0.0')

"""
def run():
    # driver = WhatsAPIDriver(username="FRTNX", client='Chrome', headless=True)
    time.sleep(15)
    logging.info('getting chats')
    chats = driver.get_all_chats()
    logging.info(chats)
    chat = None
    logging.info('finding dialogue of interest')
    for c in chats:
        if '27793644718' in str(c):
            chat = c
    logging.info('dialogue search complete. found %s' % chat)
    logging.info('loading all earlier messages')
    chat.load_all_earlier_messages()
    logging.info('extracting all messages, self included')
    messages = chat.get_messages(include_me=True)
    logging.info('chats extraction successful')
    processed = []
    logging.info('beginning iteration through messages')
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
    logging.info('iteration complete. returning result')
    logging.info(processed)
    response = requests.post("https://bvjaygf3qd.execute-api.eu-west-1.amazonaws.com/dev/store", 
                             data=json.dumps(processed))
    logging.info('response code: %s\nresponse content: %s' % (response.status_code, response.content))
"""
