import json
import os
import boto3
from dotenv import load_dotenv, find_dotenv

def sign_up(new_user):
    load_dotenv(find_dotenv())

    # read the .env-sample, to load the environment variable.
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env-sample")
    load_dotenv(dotenv_path)
    
    
    client = boto3.client("cognito-idp", region_name="us-east-1")
    
    print(os.getenv("COGNITO_USER_CLIENT_ID"))
    
     # TODO implement
    response = client.sign_up(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
        Username=new_user['username'],
        Password=new_user['password'],
        UserAttributes=[
            {"Name": "email", "Value": new_user['email']},
            { "Name": "phone_number", "Value": new_user['phone_number']},
            {"Name": "birthdate" , "Value": new_user['birthdate']}])
    
    
    return response

def lambda_handler(event, context):

    new_user = {
        "username" : event.body['username'],
        "password" : event.body['password'],
       " email" : event.body['email'],
        "phone_number" : event.body['phone_number'],
        "birthdate" : event.body['birthdate']

    }
    
    return sign_up(new_user)