import json
import os
import boto3

"""
Confirm new user by confirmation_code
"""
client = boto3.client("cognito-idp", region_name="us-east-1")

KEY_ERROR_MESSAGE = {
    "username" : "Debe indicar su nombre de usuario",
    "confirmation_code" : "Debe escribir el número de confirmación enviado a su celular"
}

def confirm_user(confirm_data_user):
  
    
    response = client.confirm_sign_up(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
        Username=confirm_data_user["username"],
        ConfirmationCode=confirm_data_user["confirmation_code"]
    )
        
    return response
   
def validate(data):
    
    for name in data.keys():
        if not data[name]:
            raise KeyError(str(name))

def lambda_handler(event, context):

    response = {
        "error" : False,
        "message": "Tu cuenta ha sido confirmada satisfactoriamente",
    }
    
    try :
        confirm_data_user = {
            "username" : event['username'],
            "confirmation_code" : event['confirmation_code']
        }
        validate(confirm_data_user)
        confirm_user(confirm_data_user)
        response['error'] = False
    except KeyError as e:
        print(e)
        response['error']  = True
        response['message'] = KEY_ERROR_MESSAGE[e.args[0]]
    except Exception as e:
        print(e)
        response['error']  = True
        response['message'] = "Error interno del servidor"
        
    
    return response