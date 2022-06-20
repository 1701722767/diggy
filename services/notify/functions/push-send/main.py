import json
import boto3

sns = boto3.resource('sns')
topic = sns.Topic('arn:aws:sns:us-east-1:605550406178:push-notification')

REQUIRED_ATTRIBUTES = {
    "title" : "Debe indicar el título del mensaje",
    "body" : "Debe indicar el cuerpo del mensaje",
    "token" : "No se indicó el usuario al cual se le enviará la notificación"
}

def send(message):
    response = topic.publish(
        Message = message
    )
    validate_sns_response(response)
    return response
    
def validate_sns_response(response):
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("Error al intentar usar el servicio de push-notification")

def validate(data):
    for key in REQUIRED_ATTRIBUTES.keys():
        if key not in data or not data[key]:
            print(key," missing")
            raise KeyError(key)
    
def lambda_handler(event, context):
    
    message = {
        "error" : False,
        "message": "Notificación enviada",
    }
    
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(message)
    }
    
    try:
        event_data = json.loads(event["body"])
        validate(event_data)
        send(json.dumps(event_data))
       
    except KeyError as e:
        response['statusCode'] = 400
        message['error'] = True
        message['message'] = REQUIRED_ATTRIBUTES[e.args[0]]
        
    except Exception as e:
        response['statusCode'] = 500
        message['error'] = True
        message['message'] = str(e)
    
    response['body'] = json.dumps(message,ensure_ascii=False)
    return response
    
   
