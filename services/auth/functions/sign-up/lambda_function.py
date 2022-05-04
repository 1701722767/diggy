import json
import os
import boto3

def sign_up(new_user):
  
    client = boto3.client("cognito-idp", region_name="us-east-1")
    
    try:
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
    except Exception as e:
       return str(e)
    
    

def lambda_handler(event, context):
    
    new_user = {
        "username" : event['username'],
        "password" : event['password'],
        "email" : event['email'],
        "phone_number" : event['phone_number'],
        "birthdate" : event['birthdate'],
        "name": event['name']

    }
    
    return sign_up(new_user)