import json
import boto3
from datetime import datetime
 
dynamodb = boto3.resource("dynamodb")
employees_table = dynamodb.Table("Employees")
requests_table = dynamodb.Table("SkillRequests")
 
def lambda_handler(event, context):
    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
 
        employee_id = body.get("employeeId")
        new_skill = body.get("skill")
        certification_name = body.get("certificationName")
        expiry_date = body.get("expiryDate")
 
        if not employee_id or not new_skill:
            return failure("employeeId and skill are required")
 
        # Fetch employee
        emp = employees_table.get_item(Key={"employeeId": employee_id}).get("Item")
 
        if not emp:
            return failure("Employee not found", 404)
 
        # ---- Extract EMPLOYEE skills safely ----
        raw_list = emp.get("skills", [])
        skills = []
 
        for item in raw_list:
            if isinstance(item, dict) and "S" in item:
                skills.append(item["S"])
            elif isinstance(item, str):
                skills.append(item)
 
        # Prevent duplicates
        if new_skill in skills:
            return success({"message": "Skill already exists", "skills": skills})
 
        # ---- Create Pending Request Entry ----
        request_id = f"REQ-{int(datetime.now().timestamp())}"
 
        requests_table.put_item(Item={
            "requestId": request_id,
            "employeeId": employee_id,
            "skillName": new_skill,
            "certificationName": certification_name or "",
            "expiryDate": expiry_date or "",
            "status": "PENDING",
            "requestedAt": datetime.utcnow().isoformat() + "Z"
        })
 
        return success({
            "message": "Request submitted successfully. Awaiting manager approval.",
            "requestId": request_id
        })
 
    except Exception as e:
        print("ERROR:", str(e))
        return failure("Internal server error")
 
def success(body):
    return {
        "statusCode": 200,
        "headers": cors(),
        "body": json.dumps(body)
    }
 
def failure(message, status=500):
    return {
        "statusCode": status,
        "headers": cors(),
        "body": json.dumps({"message": message})
    }
 
def cors():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
    }
 