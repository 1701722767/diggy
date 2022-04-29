import json
import os
import boto3
from dotenv import load_dotenv, find_dotenv

def sign_up():
    load_dotenv(find_dotenv())

    # read the .env-sample, to load the environment variable.
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env-sample")
    load_dotenv(dotenv_path)
    
    username = "usertest041"
    password = "#Abc1234"
    
    client = boto3.client("cognito-idp", region_name="us-east-1")
    
    print(os.getenv("COGNITO_USER_CLIENT_ID"))
    
     # TODO implement
    response = client.sign_up(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
        Username=username,
        Password=password,
        UserAttributes=[
            {"Name": "email", "Value": "nicolascr181@outlook.com"},
            { "Name": "phone_number", "Value": "+573234440587"},
            {"Name": "birthdate" , "Value": "5 Jun 1998"}])
    
    
    return response

def lambda_handler(event, context):
    
    return sign_up()