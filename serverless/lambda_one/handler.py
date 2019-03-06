import json
import boto3
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')
ec2 = boto3.client('ec2')

def initialise(event, context):
    """Extracts previous stored numbers from s3 and wakes up container if numbers
       have been found.
       
       params:
          event -> dict: format = {'user': 'user_x'}
    """
    try:
        obj = s3.Object('init-whatsapp-scraper-de-serverlessdeploymentbuck-10bk8g5vdrvks', '{}.json'.format(event['user']))
        data = obj.get()['Body'].read().decode('utf-8')
        body = {
            'message': json.loads(data),
            'input': event,
            'dataExists': True
        }
    except Exception as e:
        body = {
            "message": str(e),
            "input": event,
            "dataExists": False
        }

    if body['dataExists']:
        try:
            ec2.start_instances(InstanceIds=['i-09c74b1061346b11c'], DryRun=True)
        except ClientError as e:
            body['ec2Response'] = str(e)
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, run start_instances without dryrun
        try:
            response = ec2.start_instances(InstanceIds=['i-09c74b1061346b11c'], DryRun=False)
            body['ec2Response'] = response
        except ClientError as e:
            body['ec2Response'] = str(e)
    """
        # Code for stopping ec2 instance.
        # Do a dryrun first to verify permissions
        try:
            ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, call stop_instances without dryrun
        try:
            response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)
    """
    response = {
        "statusCode": 200,
        "body": json.dumps(body),
    }

    return response
