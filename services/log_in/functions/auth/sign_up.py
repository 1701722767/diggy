import json
import os
import boto3
from dotenv import load_dotenv, find_dotenv

def sign_up(username,password,email,phone_number,birthdate):
    load_dotenv(find_dotenv())

    # read the .env-sample, to load the environment variable.
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env-sample")
    load_dotenv(dotenv_path)
    
    
    client = boto3.client("cognito-idp", region_name="us-east-1")
    
    print(os.getenv("COGNITO_USER_CLIENT_ID"))
    
     # TODO implement
    response = client.sign_up(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
        Username=username,
        Password=password,
        UserAttributes=[
            {"Name": "email", "Value": email},
            { "Name": "phone_number", "Value": phone_number},
            {"Name": "birthdate" , "Value": birthdate}])
    
    
    return response

def lambda_handler(event, context):
    
    username = event['username']
    password = event['password']
    email = event['email']
    phone_number =event['phone_number']
    birthdate = event['birthdate']
    
    return sign_up(username,password,email,phone_number,birthdate)