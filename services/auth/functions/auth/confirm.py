import json
import os
import boto3
from dotenv import load_dotenv, find_dotenv

def confirm_user(username,confirmation_code):
    load_dotenv(find_dotenv())
    
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env-sample")
    load_dotenv(dotenv_path)
    
    
    client = boto3.client("cognito-idp", region_name="us-east-1")
    
    response = client.confirm_sign_up(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
        Username=username,
        ConfirmationCode=confirmation_code
    )
    
    return response

def lambda_handler(event, context):
    # TODO implement
    
    
    username = event['username']
    confirmation_code = event['confirmation_code']
    
    return confirm_user(username,confirmation_code)
