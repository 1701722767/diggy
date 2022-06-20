import firebase_admin
import json
from firebase_admin import credentials,messaging

REQUIRED_ATTRIBUTES = {
    "title" : "Debe indicar el título del mensaje",
    "body" : "Debe indicar el cuerpo del mensaje",
    "token" : "No se indicó el token de cliente"
}

cred = credentials.Certificate("serviceAccountKey.json")

def notify(push):
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    title = push["title"]
    body = push["body"]
    token  = push["token"]

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token
    )
    response = messaging.send(message)
    return response
   
def validate(data):
    for key in REQUIRED_ATTRIBUTES.keys():
        if key not in data or not data[key]:
            print(key," missing")
            raise KeyError(key)

def lambda_handler(event, context):
    response = {
        "error" : False,
        "message": "Notificación enviada",
        "data": None
    }
    
    try :
        message = json.loads(event['Records'][0]['Sns']['Message'])
        push = {
            "token" : message["token"],
            "title" : message["title"],
            "body" : message["body"]
        }
        validate(push)
        response['data'] = notify(push)
        response['error'] = False
    
    except KeyError as e:
        response['error']  = True
        response['message'] = REQUIRED_ATTRIBUTES[e.args[0]]
        
    except Exception as e:
        response['error']  = True
        response['message'] = str(e)
        
    
    return json.dumps(response,ensure_ascii = False)