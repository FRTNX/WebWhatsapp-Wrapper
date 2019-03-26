import os
import json
import boto3
from html_gen import generate_chips
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')
ec2 = boto3.client('ec2')

def initialise(event, context):
    """Extracts previous stored numbers from s3 and wakes up container if numbers
       have been found.
       
       params:
          event -> dict: format = {'user': 'user_x'}
    """

    print("I am alive!!! For some reason my creator made me mute")
    print("Okay this is what I received: ", event)

    if 'queryStringParameters' in list(event):
        if event['queryStringParameters']:
            print('query params found. Normalising request.')
            event = event['queryStringParameters']
            print('event now looks like: ', event)

    try:
        obj = s3.Object(os.getenv('WAS3Bucket'), '{}.json'.format(event['user']))
        data = obj.get()['Body'].read().decode('utf-8')
        contacts = json.loads(data)
        numbers = json.loads(contacts['numbers'])
        print('User has pre-existing data: ', contacts)
        print(numbers)
    except Exception as e:
        print(e)
        if 'NoSuchKey' in str(e):
            print('new user detected')
            numbers = []

    html_data = generate_chips(event['user'], numbers)
    body = {
        'message': html_data,
        'input': event,
        'dataExists': True
    }
    print('contructed body: ', body)

    if body['dataExists']:
        try:
            ec2.start_instances(InstanceIds=['i-0cdce218490d2f160'], DryRun=True)
        except ClientError as e:
            print(e)
            body['Ec2Response'] = str(e)
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, run start_instances without dryrun
        try:
            response = ec2.start_instances(InstanceIds=['i-0cdce218490d2f160'], DryRun=False)
            body['Ec2Response'] = response
            print('body after call to ec2 now looks like: ', body)
        except ClientError as e:
            print(e)
            body['Ec2Response'] = str(e)

    response = {
        "statusCode": 200,
        "body": body["message"],
        "headers": {
            "Content-Type": "text/html"
        }
    }
    print('callback response: ', response)

    return response
