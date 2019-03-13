import logging
import os
import json
import boto3
import qrcode
import requests

s3 = boto3.resource('s3')
ec2 = boto3.client('ec2')

def get_qr(event, context):
    """Compares recieved numbers to previous saved numbers. Updates old numbers
       if a change is detected. If numbers exist in JSON from front end, the 
       lambda will attempt to fetch a qr string from the scraper.

       params:
           event -> dict: format = {'user': '27032423434', 'data': ['27234344234', '27833242345']}
                          where `user` is the user id, here represented by a phonenumber, but can
                          take the form of any string value and,
                          `data` is a list of numbers the user would like chats extracted from.
    """

    print("I am alive!!!")
    print("Okay this is what I received: ", event)
    if 'queryStringParameters' in list(event):
        if event['queryStringParameters']:
            print('query params found. Normalising request.')
            event = event['queryStringParameters']
            print('event now looks like: ', event)

    stored_data = {
        "numbers": []
    }

    try:
        obj = s3.Object('init-whatsapp-scraper-de-serverlessdeploymentbuck-10bk8g5vdrvks', '{}.json'.format(event['user']))
        try:
            stored_data = json.loads(obj.get()['Body'].read().decode('utf-8'))
        except Exception as e:
            logging.error(str(e))
        extracted_data = event['data']

        if stored_data['numbers'] == extracted_data:
            logging.info('no changes to numbers detected.')
            res = 'No changes to data detected.'
        else:
            logging.info('changes detected in selected numbers. Updating...')

            new_numbers = {
                "numbers": event["data"]
            }

            obj = json.dumps(new_numbers)
            data = str.encode(obj)
            res = s3.Bucket('init-whatsapp-scraper-de-serverlessdeploymentbuck-10bk8g5vdrvks').put_object(Key='{}.json'.format(event['user']), Body=data) 
            logging.info('successfully stored new file in s3.')

        body = {
            "message": str(res),
            "input": event,
            "extracted_data_type": str(type(extracted_data))
        }

        response = ec2.describe_instances()
        for instance in response['Reservations']:
            if instance['Instances'][0]['InstanceId'] == 'i-09c74b1061346b11c':
                if 'PublicIpAddress' in list(instance['Instances'][0]):
                    instance_ip = instance['Instances'][0]['PublicIpAddress']
                    request = requests.get('http://' + instance_ip + ':5000/index',
                                           params={'contacts': json.dumps(event['data'])})
                    if request.status_code == 200:
                        body['QRString'] = request.content.decode('utf-8')
                        body['html'] = """<!DOCTYPE html>
                                            <html>
                                            <head>
                                                <title>Index</title>
                                            </head>
                                            <body style="background-color:black;">
                                                <div style="text-align: center">
                                                        
                                                    <img src="file:///var/task/qr.png" alt="" align="center">
                                                    <h3 style="color:gray; font-family:courier;">Scan me to complete your mission.</h3>
                                                    </div>
                                            </body>
                                            </html>"""
                    else:
                        body['error'] = request.content
                else:
                    body['error'] = 'AMI found but no public ip is assigned to it.'
                break

    except Exception as e:
        body = {
            "message": str(e),
            "input": event,
            "dataExists": False
        }

    if 'QRString' in list(body):
        os.system("sudo qr '%s' > qr.png" % body['QRString'])
        body = body['html']

    response = {
        "statusCode": 200,
        "body": body,
        "headers": {
            "Content-Type": "text/html"
            }
    }
    print('generated response: ', response)
    print('path to this lambda: ', os.path.realpath(__file__))

    return response
