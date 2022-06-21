import json
import boto3
from decimal import Decimal
import base64

AWS_REGION = "us-east-1"
client = boto3.resource('dynamodb',region_name=AWS_REGION)
places_table = client.Table("places")

def get_comments(composite_key):
    response = places_table.get_item(
        Key=decodeBase64ToJson(composite_key),
        ProjectionExpression="comments"
    )
    return response['Item']
    
def decodeBase64ToJson(base64Data):
    base64_bytes = base64Data.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return json.loads(message_bytes.decode('ascii'))

def lambda_handler(event, context):
    message = {
        'error' : False,
        'message' : 'Lugar encontrado',
        'data': None
    }
    
    
    response =  {
        'statusCode':200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body' : None
    }
    
    try:
        composite_key = event['queryStringParameters']['composite_key']
        message['data'] = get_comments(composite_key)
        
    except KeyError as e:
        message['error'] = True
        message['message'] = str(e)
        response['statusCode'] = 400
        
    except Exception as e:
        message['error'] = True
        message['message'] = 'Error interno del servidor'
        response['statusCode'] = 500
        
    
    response['body'] = json.dumps(message, default=str, ensure_ascii=False)
    return response
    
    
    
    
    
