import json
import os
import boto3

def log_in(user):
    
    client = boto3.client("cognito-idp", region_name="us-east-1")
    
     
    username = user['username']
    password = user['password']
    
    try: 
     
        response = client.initiate_auth(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": password},
        )
        
        # Getting the user details.
        access_token = response["AuthenticationResult"]["AccessToken"]
        
        response = client.get_user(AccessToken=access_token)
        
        token_user = {
            "access_token" : access_token
        }
        
        return token_user
    
    except Exception as e:
        return str(e)
        

def validate(data):
    for name in data.keys():
        if not data[name]:
            print(name," undefined")
            return False
    
    return True
    
    
def lambda_handler(event, context):
    # TODO implement

    if validate(event):
        user = {
            "username" : event['username'],
            "password" : event['password']
        }
        return log_in(user)
    else:
        return None
    
    