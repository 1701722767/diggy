import json
import boto3
from decimal import Decimal


AWS_REGION = "us-east-1"

client = boto3.resource('dynamodb', region_name=AWS_REGION)
users_table = client.Table("users")


def get_user(id, user_name):
    response = users_table.get_item(
        Key={
            "id": id,
            "user_name": user_name
        },
    )

    if 'Item' not in response:
        raise KeyError("No existe el usuario")

    return response['Item']


def lambda_handler(event, context):

    message = {
        'error': False,
        'message': 'Información de usuario encontrada',
        'data': None
    }

    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': None
    }

    try:
        id = event["requestContext"]["authorizer"]["claims"]["sub"]
        user_name = event["requestContext"]["authorizer"]["claims"]['cognito:username']
        data = get_user(id, user_name)
        message['data'] = data

    except KeyError as e:
        message['error'] = True
        message['message'] = "Error interno del servidor"
        response['statusCode'] = 400


    except Exception as e:
        message['error'] = True
        message['message'] = 'Error interno del servidor'
        response['statusCode'] = 500


    response['body'] = json.dumps(message, default=str, ensure_ascii=False)
    return response