import boto3
import json
import base64
import traceback
from decimal import Decimal
from boto3.dynamodb.conditions import Key

PAGE_SIZE = 15
AWS_REGION = "us-east-1"

dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
transactions_table = dynamodb.Table('transactions')


class CustomError(Exception):
    pass


"""
Request is the class used for handling the request
"""
class Request:
    def __init__(self):
        self.err = None

    def encodeJSONToBase64(self, jsonData):
        stringJSON = json.dumps(jsonData)
        json_bytes = stringJSON.encode('ascii')
        base64_bytes = base64.b64encode(json_bytes)
        return base64_bytes.decode('ascii')

    def decodeBase64ToJson(self, base64Data):
        base64_bytes = base64Data.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        return json.loads(message_bytes.decode('ascii'), parse_float=Decimal)

    def process(self, event):
        body = event.get("queryStringParameters", {})
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]

        exclusiveStartkey = None
        if body != None and body.get("start_key", "") != "":
            exclusiveStartkey = self.decodeBase64ToJson(body["start_key"])

        filterExpression = Key("user_id").eq(user_id)

        if exclusiveStartkey == None:
            return self.createResponse(transactions_table.query(Limit=PAGE_SIZE, KeyConditionExpression=filterExpression))

        return self.createResponse(
            transactions_table.query(
                ExclusiveStartKey=exclusiveStartkey,
                KeyConditionExpression=filterExpression,
                Limit=PAGE_SIZE
            )
        )

    def createResponse(self, response):
        print(response)

        data = {
            "items": response['Items']
        }

        if 'LastEvaluatedKey' in response and response['Count'] > 0:
            data["start_key"] = self.encodeJSONToBase64(
                response['LastEvaluatedKey'])

        return data


"""
lambda_handler function that starts the lambda
"""
def lambda_handler(event, context):
    _ = context

    message = {
        'error': False,
        'message': 'Transacciones listadas correctamente',
        'data': None
    }

    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': None
    }

    req = Request()
    try:
        message['data'] = req.process(event)

    except CustomError as e:
        message['error'] = True
        message['message'] = str(e)
        response['statusCode'] = 404

    except Exception as err:
        print(err)
        print(traceback.format_exc())
        message['error'] = True
        message['message'] = "Error interno en el servidor"
        response['statusCode'] = 500
    finally:
        if req.err is None:
            print(req.err)

        response['body'] = json.dumps(message, default=str, ensure_ascii=False)
        return response
