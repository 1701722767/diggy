import json
import boto3
from decimal import Decimal
import base64


AWS_REGION = "us-east-1"

client = boto3.resource('dynamodb',region_name=AWS_REGION)
events_table = client.Table("places")

class CustomError(Exception):
    pass


def get_event(composite_key):
    response = events_table.get_item(
        Key=decodeBase64ToJson(composite_key),
    )

    if 'Item' not in response:
        raise KeyError("Lugar no encontrado")

    if 'user_id' in response['Item']:
        del response['Item']['user_id']

    return response['Item']


def decodeBase64ToJson(base64Data):
    base64_bytes = base64Data.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    jsonData = json.loads(message_bytes.decode('ascii'))

    if 'id' not in jsonData:
        raise CustomError("Búsqueda erronea")

    if 'category_id' not in jsonData:
        raise CustomError("Búsqueda erronea")

    return jsonData


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
        composite_key = (event['queryStringParameters']['composite_key'])
        data = get_event(composite_key)
        message['data'] = data

    except KeyError as e:
        message['error'] = True
        message['message'] = 'No existe el lugar'
        response['statusCode'] = 400

    except CustomError as e:
        message['error'] = True
        message['message'] = str(e)
        response['statusCode'] = 404

    except Exception as e:
        print(e)
        message['error'] = True
        message['message'] = 'Error interno del servidor'
        response['statusCode'] = 500


    response['body'] = json.dumps(message, default=str, ensure_ascii=False)
    return response





