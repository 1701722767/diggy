import json
import boto3
from boto3.dynamodb.conditions import Attr

AWS_REGION = "us-east-1"
client = boto3.resource('dynamodb',region_name=AWS_REGION)
sns = boto3.resource('sns',region_name=AWS_REGION)
topic = sns.Topic('arn:aws:sns:us-east-1:605550406178:push-notification')
users_table = client.Table("users")

def send_to_users(event_name,category_id):
    
    tokens = get_tokens(category_id)
    for token in tokens:
        push = {
                "token" : str(token["FCM_token"]),
                "title" : "Nuevo Evento de interés",
                "body" : event_name
            
                }
        send(json.dumps(push))

def send(message):
    response = topic.publish(
        Message = message
    )
    return response
    
def get_tokens(category_id):
    response = users_table.scan(
        FilterExpression = Attr("categories").contains(category_id) & 
        Attr("FCM_token").exists(),
        ProjectionExpression = "FCM_token"
    )
    return response['Items']

def lambda_handler(event, context):
    
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': None
    }
    
    try:
        message = json.loads(event['Records'][0]['Sns']['Message'])
        send_to_users(message['event_name'],message['category_id'])
       
    except KeyError as e:
        response['statusCode'] = 400
      
    except Exception as e:
        response['statusCode'] = 500
        
    return response
    
   
