import json
import boto3
dynamodb = boto3.resource("dynamodb")
assign_table = dynamodb.Table("LearningAssignments")
def lambda_handler(event, context):
    resp = assign_table.scan()
    items = resp.get("Items", [])
    return {
        "statusCode": 200,
        "headers": _cors(),
        "body": json.dumps(items)
    }
def _cors():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
    }
 