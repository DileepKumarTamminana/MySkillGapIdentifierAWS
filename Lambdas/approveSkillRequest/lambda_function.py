import json
import boto3
from datetime import datetime
 
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("SkillRequests")
 
def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
 
        requestId = body.get("requestId")
        action = body.get("action")   # APPROVE or REJECT
        managerId = body.get("managerId", "MANAGER1")
 
        if not requestId or not action:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing requestId or action"})
            }
 
        status_value = "APPROVED" if action == "APPROVE" else "REJECTED"
 
        response = table.update_item(
            Key={"requestId": requestId},
            UpdateExpression="SET #s = :status, approvedBy = :mgr, approvedAt = :time",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={
                ":status": status_value,
                ":mgr": managerId,
                ":time": datetime.utcnow().isoformat()
            },
            ReturnValues="UPDATED_NEW"
        )
 
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "message": f"Request {status_value} successfully",
                "updated": response.get("Attributes", {})
            })
        }
 
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e)
            })
        }