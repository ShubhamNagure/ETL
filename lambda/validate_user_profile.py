import json
import boto3
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Bucket']
    key = event['Key']
    
    response = s3.get_object(Bucket=bucket, Key=key)
    raw_data = response['Body'].read().decode('utf-8')
    
    if "valid" in raw_data:
        valid_bucket = os.environ['VALID_BUCKET']
        s3.put_object(Bucket=valid_bucket, Key=key, Body=raw_data)
        statusCode = 200
    else:
        statusCode = 400
    
    return {
        'statusCode': statusCode,
        'data': raw_data
    }

