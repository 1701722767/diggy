import firebase_admin
from firebase_admin import credentials,messaging

def init(push):

    cred = credentials.Certificate("serviceAccountKey.json")
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    title = push["title"]
    body = push["body"]
    registration_token  = push["registration_token"]

    # See documentation on defining a message payload.

    try :
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=registration_token
        )

        # Send a message to the device corresponding to the provided
        # registration token.
        response = messaging.send(message)
        return response

    except Exception as e:
        return str(e)


def lambda_handler(event, context):


    push = {
        "registration_token" : event["registration_token"],
        "title" : event["title"],
        "body" : event["body"]
    }

    return init(push)