import json
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')

def stop_whatsapp_scraper(event, context):
    """Stops the ec2 instance running the Whatsapp Web scraper.
    """
    body = {
        "message": "",
        "input": event
    }
    try:
        ec2.stop_instances(InstanceIds=['i-0cdce218490d2f160'], DryRun=True)
    except ClientError as e:
        print(e)
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=['i-0cdce218490d2f160'], DryRun=False)
        print("Dry run successful. Here art the final results: ", response)
        body['message'] = response
    except ClientError as e:
        body['message'] = str(e)
        print(e)

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    print('callback response: ', response)

    return response
