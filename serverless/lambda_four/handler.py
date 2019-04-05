import json
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')

def check_ec2_status(event, context):
    """Stops the ec2 instance running the Whatsapp Web scraper.
    """

    body = {
        'message': 'not found'
    }
    response = ec2.describe_instances()
    for instance in response['Reservations']:
        print('Searching for target machine.')
        if instance['Instances'][0]['InstanceId'] == 'i-0cdce218490d2f160':
            print('Found target machine.')
            state = instance['Instances'][0]['State']['Name']
            print('Target machine is in state: ' + state)
            body['message'] = state

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET"
        }
    }
    print('callback response: ', response)

    return response
