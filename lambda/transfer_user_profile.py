import json

def handler(event, context):
    print("Transferring user profile:", event)
    # logic to transfer user profile
    return {
        'statusCode': 200,
        'body': json.dumps('User profile transferred')
    }
