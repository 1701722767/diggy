import boto3
import json
import base64
import traceback
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

PAGE_SIZE = 15
AWS_REGION = "us-east-1"

dynamodb = boto3.resource('dynamodb',region_name=AWS_REGION)
eventsTable = dynamodb.Table('events')


"""
Request is the class used for handling the request
"""
class Request:
    def __init__(self):
        self.err = None

    def encodeJSONToBase64(self,jsonData):
        stringJSON = json.dumps(jsonData)
        json_bytes = stringJSON.encode('ascii')
        base64_bytes = base64.b64encode(json_bytes)
        return base64_bytes.decode('ascii')

    def decodeBase64ToJson(self,base64Data):
        base64_bytes = base64Data.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        return json.loads(message_bytes.decode('ascii'), parse_float=Decimal)

    def process(self,event):
        body = event.get("queryStringParameters",{})
        response = None

        if body == None:
            response = eventsTable.scan(Limit=PAGE_SIZE)
        elif body.get("start_key","") !=  "":
            response = eventsTable.scan(
                 Limit=PAGE_SIZE,
                 ExclusiveStartKey= self.decodeBase64ToJson(body["start_key"])
            )
        elif body.get("category_id","") !=  "":
            response = eventsTable.scan(
                FilterExpression=Attr("category_id").eq(body["category_id"]),
                Limit=PAGE_SIZE
            )
        else:
            response = eventsTable.scan(Limit=PAGE_SIZE)

        data = {
            "items":response['Items']
        }

        if 'LastEvaluatedKey' in response:
            data["start_key"] = self.encodeJSONToBase64(response['LastEvaluatedKey'])

        return {
            "error": False,
            "message": "Eventos listados correctamente",
            "data" : data
        }


"""
lambda_handler function that starts the lambda
"""
def lambda_handler(event, context):
    _ = context
    req = Request()
    try:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(req.process(event),default=str)
        }

    except Exception as err:
        print(err)
        print(traceback.format_exc())
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                "error": True,
                "message": "Error interno en el servidor",
            })
        }
        return
    finally:
        if req.err is None:
            print(req.err)