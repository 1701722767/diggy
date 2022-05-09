import firebase_admin
import json
from firebase_admin import credentials,messaging

def init(push):

    cred = credentials.Certificate("serviceAccountKey.json")
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    title = push["title"]
    body = push["body"]
    token  = push["token"]

    # See documentation on defining a message payload.

    try :
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token
        )

        # Send a message to the device corresponding to the provided
        # registration token.
        response = messaging.send(message)
        return response
        

    except Exception as e:
        print(str(e))
        raise e

def validate(data):
    for name in data.keys():
        if not data[name]:
            print(name," undefined")
            return False
    
    return True


def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])

    if validate(event):
        push = {
            "token" : message["token"],
            "title" : message["title"],
            "body" : message["body"]
        }
        return init(push)
    else:
        return None
