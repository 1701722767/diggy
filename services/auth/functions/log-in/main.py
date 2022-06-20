import json
import os
import boto3
from botocore.exceptions import ClientError

AWS_REGION = "us-east-1"
client = boto3.client("cognito-idp", region_name=AWS_REGION)
client_users = boto3.resource('dynamodb',region_name=AWS_REGION)
users_table = client_users.Table("users")

KEY_ERROR_MESSAGE = {
    "username" : "Debe escribir su nombre de usuario",
    "password" : "Debe escribir su contraseña"
}


def log_in(user):
    username = user['username']
    password = user['password']
    
    response = client.initiate_auth(
    ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": username, "PASSWORD": password},
    )

    access_token = response["AuthenticationResult"]["IdToken"]
    
    sub = client.get_user(
        AccessToken= response["AuthenticationResult"]["AccessToken"]
    )
    
    user['id'] = sub["UserAttributes"][0]["Value"]
    save_firebase_token(user)

    return {
        "access_token" : access_token
    }
    
def save_firebase_token(user):
    if 'FCM_token' in user:
        FCM_token = user['FCM_token']
        response = users_table.update_item(
            Key = {
                'id' : user['id'],
                'user_name' : user['username']
            },
            UpdateExpression = "SET FCM_token=:FCM_token",
            ExpressionAttributeValues = {
                ":FCM_token":FCM_token
            }
        )
        validate_dynamodb_response(response)
        
def validate_dynamodb_response(response):
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("Error al intentar guardar el token de notificaciones push")
        
def validate(data):
    for name in KEY_ERROR_MESSAGE.keys():
        if name not in data or not data[name]:
            raise KeyError(name)

def lambda_handler(event, context):
    response = {
        "error" : False,
        "message": "Inicio de sesión exitoso",
        "data": None
    }

    try :
        validate(event)
        data = log_in(event)
        response['error'] = False
        response['data'] = data

    except KeyError as e:
        print(e)
        response['error']  = True
        response['message'] = KEY_ERROR_MESSAGE[e.args[0]]

    except ClientError as e:
        response['error']  = True
        if e.response['Error']['Code'] == 'NotAuthorizedException':
            response['message'] = "Credenciales incorrectas."
        else:
            response['message'] = "Error interno del servidor"
            
    except Exception as e:
        print(e)
        response['error']  = True
        response['message'] =  str(e)

    return response


