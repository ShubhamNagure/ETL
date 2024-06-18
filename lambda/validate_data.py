import json
import boto3
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extract bucket and key from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Download the file from S3
    download_path = f'/tmp/{key}'
    s3.download_file(bucket, key, download_path)

    # Validate the data (example validation logic)
    with open(download_path, 'r') as file:
        data = json.load(file)
        if not validate(data):
            raise ValueError("Invalid data")

    # Upload validated data to the user valid bucket
    valid_bucket = os.environ['USER_VALID_BUCKET']
    s3.upload_file(download_path, valid_bucket, key)

    return {
        'statusCode': 200,
        'body': json.dumps('Data validated and uploaded to user-valid-bucket')
    }

def validate(data):
    # Example validation logic
    return 'required_field' in data
