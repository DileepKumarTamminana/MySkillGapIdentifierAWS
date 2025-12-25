import json
import boto3
from boto3.dynamodb.conditions import Attr
 
dynamodb = boto3.resource("dynamodb")
requests_table = dynamodb.Table("SkillRequests")
employees_table = dynamodb.Table("Employees")
 
 
def lambda_handler(event, context):
    try:
        # FIX: Proper scan with closing parenthesis + case-insensitive status check
        response = requests_table.scan(
            FilterExpression=(
                Attr("status").eq("PENDING") |
                Attr("status").eq("Pending") |
                Attr("status").eq("pending")
            )
        )
 
        items = response.get("Items", [])
        output = []
 
        for req in items:
            empId = req.get("employeeId")
 
            # Safe lookup
            emp = employees_table.get_item(Key={"employeeId": empId}).get("Item", {})
            empName = emp.get("name", f"Employee {empId}")
 
            output.append({
                "requestId": req.get("requestId"),
                "employeeId": empId,
                "employeeName": empName,
                "skillName": req.get("skillName"),
                "certificationName": req.get("certificationName"),
                "expiryDate": req.get("expiryDate"),
                "requestedAt": req.get("requestedAt"),
                "status": req.get("status")
            })
 
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps(output)
        }
 
    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e)
            })
        }
