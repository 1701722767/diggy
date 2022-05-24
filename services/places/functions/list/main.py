import json
import boto3
import base64
from decimal import Decimal

PAGE_SIZE = 5
AWS_REGION = "us-east-1"

dynamodb = boto3.resource('dynamodb',region_name=AWS_REGION)
places_table= dynamodb.Table('places')


def list_places(event):
    
    queryStringParameters = event["queryStringParameters"]
    
    items = {
        'Items' : []
    }
    
    if ((queryStringParameters) and ('last_evaluated_key' in queryStringParameters) and
        (queryStringParameters['last_evaluated_key'])):
            
        last_evaluated_key = queryStringParameters['last_evaluated_key']
        response = places_table.scan(
            Limit = PAGE_SIZE,
            ExclusiveStartKey = decodeBase64ToJson(last_evaluated_key)
        )
        
    else:
        response = places_table.scan(
            Limit = PAGE_SIZE,
        )
    
    items['Items'] = response['Items']
    
    if 'LastEvaluatedKey' in response:
        items['last_evaluated_key'] = encodeJSONToBase64(response['LastEvaluatedKey'])
        
    validate_dynamodb_response(response)
    
    return items
    
    
def encodeJSONToBase64(jsonData):
    stringJSON = json.dumps(jsonData)
    json_bytes = stringJSON.encode('ascii')
    base64_bytes = base64.b64encode(json_bytes)
    return base64_bytes.decode('ascii')

def decodeBase64ToJson(base64Data):
    base64_bytes = base64Data.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return json.loads(message_bytes.decode('ascii'), parse_float=Decimal)
    
def validate_dynamodb_response(response):
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("Error interno")

def lambda_handler(event, context):
    
    message = {
        "error" : False,
        "message" : "Lugares listados correctamente",
        "data":None
    }
    
    response =  {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body' : None
    }
    
    try:
        message['data'] = list_places(event)
    except Exception as e:
        print(e)
        response['statusCode'] = 500
        message['error'] = True
        message['message'] = "Error interno del servidor"
    
    response['body'] = json.dumps(message,default=str,ensure_ascii=False)
    return response
