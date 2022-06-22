import json
import boto3

AWS_REGION = "us-east-1"
client = boto3.resource('dynamodb',region_name=AWS_REGION)
users_table = client.Table("users")

REQUIRED_ATTRIBUTES = {
    "id" : "No se indicó el id del usuario",
    "user_name" : "No se indicó el user_name del usuario",
    "FCM_token" : "No se indicó el token FCM del usuario"
}

def validate(data):
    for key in REQUIRED_ATTRIBUTES.keys():
        if key not in data or not data[key]:
            print(key," missing")
            raise KeyError(key)
            
def save_FCM_token(user):
    FCM_token = user['FCM_token']
    response = users_table.update_item(
        Key = {
            'id' : user['id'],
            'user_name' : user['user_name']
        },
        UpdateExpression = "SET FCM_token=:FCM_token",
        ExpressionAttributeValues = {
            ":FCM_token":FCM_token
        }
    )
    validate_dynamodb_response(response)
    return response
    
def validate_dynamodb_response(response):
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("Error interno en la base de datos")

def lambda_handler(event, context):
    message = {
        "error" : False,
        "message": "Token de notificaciones push guardado exitosamente",
    }
    
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(message)
    }
    
    try:
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]
        user_name = event['requestContext']['authorizer']['claims']['cognito:username']
        user_data = json.loads(event["body"])
        user_data['id'] = user_id
        user_data['user_name'] = user_name
        validate(user_data)
        save_FCM_token(user_data)
       
    except KeyError as e:
        response['statusCode'] = 400
        message['error'] = True
        message['message'] = REQUIRED_ATTRIBUTES[e.args[0]]
        
    except Exception as e:
        response['statusCode'] = 500
        message['error'] = True
        message['message'] = str(e)
    
    response['body'] = json.dumps(message,ensure_ascii=False)
    return response
