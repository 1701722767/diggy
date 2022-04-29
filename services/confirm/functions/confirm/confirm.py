import json
import os
import boto3
from dotenv import load_dotenv, find_dotenv

def confirm_user():
    load_dotenv(find_dotenv())
    
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env-sample")
    load_dotenv(dotenv_path)
    
    username = "usertest04"
    password = "#Abc1234"
    
    client = boto3.client("cognito-idp", region_name="us-east-1")
    
    response = client.confirm_sign_up(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
        Username='usertest04',
        ConfirmationCode='282666'
    )
    
    return response

def lambda_handler(event, context):
    # TODO implement
    return confirm_user()