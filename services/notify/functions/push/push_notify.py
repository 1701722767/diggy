import firebase_admin
from firebase_admin import credentials,messaging

def init():

    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    
    # This registration token comes from the client FCM SDKs.
    registration_token = 'emwnWn_D_LD0wTHJVUaV15:APA91bFBt3ZpuVsT3R9Rrnd63FpNwHU-1zCNjlm8KGwW_bLjdJWSIVLG7uh4hGUvUTXtch-RKFcL5Kl1sVVkwyvfMKTDJI7qdQ0A5SShmiWvyhpMKk-3_wgs0DhpOCe0e1JPUbQKjY6H'

    # See documentation on defining a message payload.
    message = messaging.Message(
        notification=messaging.Notification(
            title='Hello',
            body='Hello from aws lambda',
        ),
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message :', response)

def lambda_handler(event, context):
    init()