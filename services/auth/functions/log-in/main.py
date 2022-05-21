import json
import os
import boto3

client = boto3.client("cognito-idp", region_name="us-east-1")

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

    return {
        "access_token" : access_token
    }


def validate(data):

    for name in data.keys():
        if not data[name]:
            raise KeyError(str(name))


def lambda_handler(event, context):
    response = {
        "error" : False,
        "message": "Inicio de sesión exitoso",
        "data": None
    }

    try :
        user = {
            "username" : event['username'],
            "password" : event['password']
        }
        validate(user)
        data = log_in(user)
        response['error'] = False
        response['data'] = data

    except KeyError as e:
        print(e)
        response['error']  = True
        response['message'] = KEY_ERROR_MESSAGE[e.args[0]]
    except Exepcion as e:
        print(e)
        response['error']  = True
        response['message'] = "Error interno del servidor"

    return response


