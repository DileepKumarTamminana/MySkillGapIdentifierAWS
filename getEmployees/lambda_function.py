import json
import boto3

dynamodb = boto3.resource('dynamodb')
employee_table = dynamodb.Table('Employees')

def lambda_handler(event, context):
    resp = employee_table.scan()
    items = resp.get("Items", [])
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(items)
    }
