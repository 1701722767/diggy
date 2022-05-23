import json
import os
from botocore.exceptions import ClientError
import boto3

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

def validate(data):
    for name in data.keys():
        if not data[name]:
            raise KeyError(str(name))


def lambda_handler(event, context):


    response = {
        "error" : False,
        "message": "Cuenta creada exitosamente",
    }

    try :
        new_user = {
            "username" : event['username'],
            "password" : event['password'],
            "email" : event['email'],
            "phone_number" : event['phone_number'],
            "birthdate" : event['birthdate'],
            "name": event['name']

        }
        validate(new_user)
        response['data'] = sign_up(new_user)
        response['error'] = False
    except KeyError as e:
        response['error']  = True
        response['message'] = KEY_ERROR_MESSAGE[e.args[0]]
    except ClientError as e:
        response['error']  = True
        if e.response['Error']['Code'] == 'UsernameExistsException':
            response['message'] = "El usuario ya existe"
        else:
            response['message'] = "Error interno del servidor"
    except Exception as e:
        print(e)
        response['error']  = True
        response['message'] = "Error interno del servidor"

    return response


