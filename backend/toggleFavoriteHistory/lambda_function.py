# toggleFavoriteHistory.py
import json
import boto3
from botocore.exceptions import ClientError
 
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("SkillGapHistory")
 
def lambda_handler(event, context):
    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body) if body else {}
 
        history_id = body.get("historyId")
        favorite = body.get("favorite")  # true/false expected
 
        if not history_id or favorite is None:
            return response(400, {"message": "historyId and favorite (true/false) required"})
 
        # Update item (set or remove attribute based on value)
        if favorite:
            update_expr = "SET favorite = :v"
            expr_vals = {":v": True}
        else:
            # remove favorite attribute
            update_expr = "REMOVE favorite"
            expr_vals = {}
 
        if expr_vals:
            r = table.update_item(
                Key={"historyId": history_id},
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expr_vals,
                ReturnValues="ALL_NEW"
            )
        else:
            r = table.update_item(
                Key={"historyId": history_id},
                UpdateExpression=update_expr,
                ReturnValues="ALL_NEW"
            )
 
        updated = r.get("Attributes", {})
        return response(200, {"updated": updated})
 
    except ClientError as e:
        print("Dynamo error:", e)
        return response(500, {"message": "DynamoDB error", "error": str(e)})
    except Exception as e:
        print("ERROR:", e)
        return response(500, {"message": "Internal Error", "error": str(e)})
 
def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }
 