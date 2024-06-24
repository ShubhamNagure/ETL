import json
import boto3
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    raw_data = event['data']
    
    transformed_data = raw_data.upper()
    
    final_bucket = os.environ['USER_FINAL_BUCKET']
    final_key = 'transformed_data.json'
    
    s3.put_object(Bucket=final_bucket, Key=final_key, Body=transformed_data)
    
    return {
        'statusCode': 200,
        'transformedData': transformed_data
    }

