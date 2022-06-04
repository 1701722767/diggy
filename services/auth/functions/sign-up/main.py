import json
import os
from botocore.exceptions import ClientError
import boto3

AWS_REGION = "us-east-1"

client_users = boto3.resource('dynamodb',region_name=AWS_REGION)
users_table = client_users.Table("users")

client = boto3.client("cognito-idp", region_name="us-east-1")
KEY_ERROR_MESSAGE = {
    "username" : "Debe escribir un nombre de usuario",
    "password" : "Debe escribir una contraseña",
    "email" : "Debe indicar el email",
    "phone_number" : "Debe escribir el número de teléfono",
    "birthdate" : "Debe indicar su fecha de nacimiento",
    "name": "Debe escribir su nombre y apellidos"
}

def sign_up(new_user):
    
    validate(new_user)
    
    response = client.sign_up(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
        Username=new_user['username'],
        Password=new_user['password'],
        UserAttributes=[
            {"Name": "email", "Value": new_user['email']},
            {"Name": "phone_number", "Value": new_user['phone_number']},
            {"Name": "birthdate" , "Value": new_user['birthdate']},
            {"Name": "name","Value": new_user['name']},]
    )
    
    return response

def create_user(new_user,user_id):
    
    if 'password' in new_user:
        del new_user['password']
    
    new_user['id']  = user_id
    response = users_table.put_item(
        Item=new_user
    )
    
    validate_dynamodb_response(response)

def validate_dynamodb_response(response):
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("Error interno en la base de datos")

def validate(data):
    for key in KEY_ERROR_MESSAGE.keys():
        if key not in data.keys() or not data[key]:
            raise KeyError(key)


def lambda_handler(event, context):
    response = {
        "error" : False,
        "message": "Cuenta creada exitosamente",
    }

    try :
    
        response['data'] = sign_up(event)
        create_user(event,response['data']['UserSub'])
        
    except KeyError as e:
        print(e)
        response['error']  = True
        response['message'] = KEY_ERROR_MESSAGE[e.args[0]]
        
    except ClientError as e:
        print(e)
        response['error']  = True
        if e.response['Error']['Code'] == 'UsernameExistsException':
            response['message'] = "El usuario ya existe"
        elif e.response['Error']['Code'] == 'CodeDeliveryFailureException':
            response['message'] = "No se logro enviar el email de verificación"
        else:
            response['message'] = "Error interno del servidor 1"
        
    except Exception as e:
        print(e)
        response['error']  = True
        response['message'] = "Error interno del servidor"

    return response


