import json
import boto3
from boto3.dynamodb.conditions import Attr

AWS_REGION = "us-east-1"
client = boto3.resource('dynamodb',region_name=AWS_REGION)
users_table = client.Table("users")
categories_table = client.Table("categories")

def get_tokens(category_id):
    response = users_table.scan(
        FilterExpression = Attr("categories").contains(category_id),
        ProjectionExpression = "FCM_token"
    )
    return response['Items']

def validate(event):
    if not event['queryStringParameters']:
        raise Exception("No se indicó el id de la categoría")
        
def exists(category_id):
    
    if not category_id:
        raise Exception("El id no puede estar vacío")
    
    response = categories_table.get_item(
        Key={"id" : category_id}
    )
    if 'Item' not in response:
        raise Exception("La categoría ingresada no existe")
    
def lambda_handler(event, context):
    
    message = {
        "error" : False,
        "message": "Tokens obtenidos",
        "data" : {
            "items" : None
        }
    }
    
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': json.dumps(message)
    }
    
    try:
        
        validate(event)
        category_id = event['queryStringParameters']['category_id']
        exists(category_id)
        message['data']['items'] = get_tokens(category_id)
        
    except KeyError as e:
        print(str(e))
        message['error'] = True
        response['statusCode'] = 400
        message['message'] = f"El nombre {str(e)} no existe"
    
    except Exception as e:
        print(str(e))
        message['error'] = True
        response['statusCode'] = 500
        message['message'] = str(e)
    
    response['body'] = json.dumps(message,default=str,ensure_ascii=False)
    return response
