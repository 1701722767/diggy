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
        
        return access_token
        
    except Exception as e:
        return str(e)
        

def validate(data):
    
    for name in data.keys():
        if not data[name]:
            print(name," missing")
            raise Exception(str(name))
    
    
def lambda_handler(event, context):
    # TODO implement
    
    response = {
        "error" : False,
        "message": "Todo bien",
        "data": None
    }
    
    try :
        user = {
            "username" : event['username'],
            "password" : event['password']
        }
        validate(event)
    except Exception as e:
        response['error']  = True
        response['message'] = str(e).replace("'","")  + " missing"
        return response
        
    data = log_in(user)
    response['error'] = False
    response['data'] = data
    
    return response
        
    
    