import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("line-weather-notification-users")

def lambda_handler(event, context):
    print("=== LINE Webhook Received ===")
    print(json.dumps(event, ensure_ascii=False))

    body = json.loads(event.get("body", "{}"))
    print(json.dumps(body, ensure_ascii=False))

    for line_event in body.get("events", []):
        source = line_event.get("source", {})
        user_id = source.get("userId")

        message = line_event.get("message", {})
        message_text = message.get("text")

        if user_id and message_text == "登録":
            print(f"USER_ID: {user_id}")

            table.put_item(
                Item={
                    "userId": user_id
                }
            )

            print("Saved userId to DynamoDB")

    return {
        "statusCode": 200,
        "body": "OK"
    }
