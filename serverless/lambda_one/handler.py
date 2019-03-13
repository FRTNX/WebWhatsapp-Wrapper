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
    html = False

    print("I am alive!!! For some reason my creator made me mute")
    print("Okay this is what I received: ", event)

    if 'queryStringParameters' in list(event):
        if event['queryStringParameters']:
            print('query params found. Normalising request.')
            event = event['queryStringParameters']
            print('event now looks like: ', event)

    try:
        obj = s3.Object('init-whatsapp-scraper-de-serverlessdeploymentbuck-10bk8g5vdrvks', '{}.json'.format(event['user']))
        data = obj.get()['Body'].read().decode('utf-8')
        contacts = json.loads(data)
        print('s3 get object successfully called.')
        html_data = generate_chips(contacts['numbers'])
        html = True
        body = {
            'message': html_data,
            'input': event,
            'dataExists': True
        }
        print('contructed body: ', body)
    except Exception as e:
        body = {
            "message": str(e),
            "input": event,
            "dataExists": False
        }
        print('Exception generated body: ', body)

    if body['dataExists']:
        try:
            ec2.start_instances(InstanceIds=['i-09c74b1061346b11c'], DryRun=True)
        except ClientError as e:
            print(e)
            body['Ec2Response'] = str(e)
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, run start_instances without dryrun
        try:
            response = ec2.start_instances(InstanceIds=['i-09c74b1061346b11c'], DryRun=False)
            body['Ec2Response'] = response
            print('body after call to ec2 now looks like: ', body)
        except ClientError as e:
            print(e)
            body['Ec2Response'] = str(e)

    if html:
        response = {
            "statusCode": 200,
            "body": body["message"],
            "headers": {
                "Content-Type": "text/html"
            }
        }
    else:
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
    print('callback response: ', response)

    return response
