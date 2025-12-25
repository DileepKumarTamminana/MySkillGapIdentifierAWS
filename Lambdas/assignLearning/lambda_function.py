import json
import boto3
import uuid
from datetime import datetime
dynamodb = boto3.resource("dynamodb")
assign_table = dynamodb.Table("LearningAssignments")
employees_table = dynamodb.Table("Employees")
def lambda_handler(event, context):
    body = event.get("body")
    if isinstance(body, str):
        body = json.loads(body)
    employee_id = body.get("employeeId")
    skill_name = body.get("skillName")
    course_name = body.get("courseName")
    due_date = body.get("dueDate")  # YYYY-MM-DD
    manager_id = body.get("managerId", "MANAGER")
    if not employee_id or not skill_name or not course_name:
        return _error("employeeId, skillName, courseName required", 400)
    # check employee exists
    emp_resp = employees_table.get_item(Key={"employeeId": employee_id})
    if "Item" not in emp_resp:
        return _error("Employee not found", 404)
    assignment_id = str(uuid.uuid4())
    item = {
        "assignmentId": assignment_id,
        "employeeId": employee_id,
        "skillName": skill_name,
        "courseName": course_name,
        "dueDate": due_date or "",
        "status": "ASSIGNED",
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "createdBy": manager_id
    }
    assign_table.put_item(Item=item)
    return {
        "statusCode": 200,
        "headers": _cors(),
        "body": json.dumps({"message": "Learning assigned", "assignmentId": assignment_id})
    }
def _error(msg, code=500):
    return {
        "statusCode": code,
        "headers": _cors(),
        "body": json.dumps({"message": msg})
    }
def _cors():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
    }