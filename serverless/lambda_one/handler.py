import json
import boto3

s3 = boto3.resource('s3')

def initialise(event, context):
    """Extracts previous stored numbers from s3 and wakes up container if numbers
       have been found.
       
       params:
          event -> dict: format = {'user': 'user_x'}
    """
    try:
        obj = s3.Object('whatsapp-scraper-numbers', '{}.json'.format(event['user']))
        data = obj.get()['Body'].read().decode('utf-8')
        body = {
            'message': json.loads(data),
            'input': event,
            'dataExists': True
        } # render this on web page with input field for adding more numbers

    except Exception as e:
        body = {
            "message": str(e),
            "input": event,
            "dataExists": False
        }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
    }

    if body['dataExists']:
        # wake up container
        pass

    return response
