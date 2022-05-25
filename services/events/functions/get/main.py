import json
import boto3
from decimal import Decimal
import base64

AWS_REGION = "us-east-1"

client = boto3.resource('dynamodb',region_name=AWS_REGION)
events_table = client.Table("events")


def get_event(composite_key):
    response = events_table.get_item(
        Key=decodeBase64ToJson(composite_key),
        ExpressionAttributeNames= { '#max' : 'max', '#name' : 'name'},
        ProjectionExpression='#name,coordinates,datestart,dateend,description,images,#max,price,range_age,slots'
    )
    
    if 'Item' not in response:
        raise KeyError("No existe dicho evento")
    
    return response['Item']


def decodeBase64ToJson(base64Data):
    base64_bytes = base64Data.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return json.loads(message_bytes.decode('ascii'))

def lambda_handler(event, context):
    
    
    message = {
        'error' : False,
        'message' : 'Evento encontrado',
        'data': None
    }
    
    
    response =  {
        'statusCode':200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body' : None
    }
    
    try:
        composite_key = (event['queryStringParameters']['composite_key'])
        data = get_event(composite_key)
        message['data'] = data
        
    except KeyError as e:
        message['message'] = 'No existe el evento'
        response['statusCode'] = 400
        
        
    except Exception as e:
        message['error'] = True
        message['message'] = 'Error interno del servidor'
        response['statusCode'] = 500
        
    
    response['body'] = json.dumps(message, default=str, ensure_ascii=False)
    return response
    
    
    
    
    
