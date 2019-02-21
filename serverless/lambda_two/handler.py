import logging
import json
import boto3

s3 = boto3.resource('s3')

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
    stored_data = {
        "numbers": []
    }

    try:
        obj = s3.Object('whatsapp-scraper-numbers', '{}.json'.format(event['user']))
        try:
            stored_data = json.loads(obj.get()['Body'].read().decode('utf-8'))
        except Exception as e:
            logging.error(str(e))
        extracted_data = event['data']

        if stored_data['numbers'] == extracted_data:
            logging.info('no changes to numbers detected.')
        else:
            logging.info('changes detected in selected numbers. Updating...')

            new_numbers = {
                "numbers": event["data"]
            }

            obj = json.dumps(new_numbers)
            data = str.encode(obj)
            res = s3.Bucket('whatsapp-scraper-numbers').put_object(Key='{}.json'.format(event['user']), Body=data) 
            logging.info('successfully stored new file in s3.')

        # get QR code from scraper here
        # add qr string to lambda response body
  
        body = {
            "message": str(res),
            "input": event,
            "extracted_data_type": str(type(extracted_data))
        }

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

    return response
