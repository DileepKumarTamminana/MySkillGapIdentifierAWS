import json
import boto3

dynamodb = boto3.resource('dynamodb')
roles_table = dynamodb.Table('Roles')

def lambda_handler(event, context):
    # TODO implement
    resp = roles_table.scan()
    items = resp.get('Items', [])
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(items)
    }
