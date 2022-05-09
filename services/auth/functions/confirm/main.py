import json
import os
import boto3


"""
Confirm new user by confirmation_code
"""
def confirm_user(confirm_data_user):
  
    
    client = boto3.client("cognito-idp", region_name="us-east-1")
    
    try :
        response = client.confirm_sign_up(
            ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
            Username=confirm_data_user["username"],
            ConfirmationCode=confirm_data_user["confirmation_code"]
        )
        
        return response
    except Exception as e:
        print(str(e))
        raise e

def validate(data):
    
    for name in data.keys():
        if not data[name]:
            print(name," missing")
            raise Exception(str(name))

def lambda_handler(event, context):

    response = {
        "error" : False,
        "message": "Todo bien",
        "data": None
    }
    
    try :
        confirm_data_user = {
            "username" : event['username'],
            "confirmation_code" : event['confirmation_code']
        }
        validate(event)
    except Exception as e:
        response['error']  = True
        response['message'] = str(e).replace("'","")  + " missing"
        return response
        
    data = confirm_user(confirm_data_user)
    response['error'] = False
    response['data'] = data
    
    return response