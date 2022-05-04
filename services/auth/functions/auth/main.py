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
        return str(e)

def lambda_handler(event, context):
  
    
    confirm_data_user = {
        "username" : event['username'],
        "confirmation_code" : event['confirmation_code']
    }
    
    
    return confirm_user(confirm_data_user)
