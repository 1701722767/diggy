import json
import os
import boto3

client = boto3.client("cognito-idp", region_name="us-east-1")

def log_in(user):

    username = user['username']
    password = user['password']

    try:

        response = client.initiate_auth(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": password},
        )

        # Getting the user details.
        access_token = response["AuthenticationResult"]["IdToken"]

        return {
            "access_token" : access_token
        }

    except Exception as e:
        return str(e)


def validate(data):

    for name in data.keys():
        if not data[name]:
            print(name," missing")
            raise Exception(str(name))


def lambda_handler(event, context):
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

        data = log_in(user)
        response['error'] = False
        response['data'] = data

    except Exception as e:
        response['error']  = True
        response['message'] = str(e).replace("'","")  + " missing"
        return response



    return response


