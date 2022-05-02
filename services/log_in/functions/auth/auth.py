import json
import os
import boto3
from dotenv import load_dotenv, find_dotenv

def authenticate(username,auth_code,session_code):
    
    load_dotenv(find_dotenv())
    
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env-sample")
    load_dotenv(dotenv_path)
    
    
    
    client = boto3.client("cognito-idp", region_name="us-east-1")
     # Autenticarse con codigo enviado al smartphone
    response = client.respond_to_auth_challenge(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
        ChallengeName='SMS_MFA',
        ChallengeResponses = {'USERNAME':username, 'SMS_MFA_CODE':session_code},
        Session = session_code
    )
    
    # Getting the user details.
    access_token = response["AuthenticationResult"]["AccessToken"]
    
    response = client.get_user(AccessToken=access_token)
    
    
    return response

def lambda_handler(event, context):
    # TODO implement
    
    username = event['username']
    auth_code = event['auth_code']
    session_code = event['session_code']
    
    return authenticate(username,auth_code,session_code)