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
            print(name," missing")
            raise Exception(str(name))


def lambda_handler(event, context):
    
    response = {
        "error" : False,
        "message": "Todo bien",
        "data": None
    }
    
    try :
        message = json.loads(event['Records'][0]['Sns']['Message'])
        push = {
            "token" : message["token"],
            "title" : message["title"],
            "body" : message["body"]
        }
        validate(message)
    except Exception as e:
        response['error']  = True
        response['message'] = str(e).replace("'","")  + " missing"
        return response
        
    data = init(push)
    response['error'] = False
    response['data'] = data
    
    return response
