import boto3
import json
import base64
from boto3.dynamodb.conditions import Key

PAGE_SIZE = 15
AWS_REGION = "us-east-1"

dynamodb = boto3.resource('dynamodb',region_name=AWS_REGION)
eventsTable = dynamodb.Table('events')


class Request:
    """
    Request is the class used for handling the request
    """
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
        return json.loads(message_bytes.decode('ascii'))

    def process(self,event):
        response = None
        if event.get("start_key","") !=  "":
            response = eventsTable.scan(
                 Limit=PAGE_SIZE,
                 ExclusiveStartKey= self.decodeBase64ToJson(event["start_key"])
            )
        elif event.get("category_id","") !=  "":
            response = eventsTable.query(
                KeyConditionExpression=Key('category_id').eq(event["category_id"]),
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



def lambda_handler(event, context):
    """
    lambda_handler function that starts the lambda
    """
    _ = context
    req = Request()
    try:
        return req.process(event)

    except Exception as err:
        print(err)
        return {
            "error": True,
            "message": "Error interno en el servidor",
        }
    finally:
        if req.err is None:
            print(req.err)