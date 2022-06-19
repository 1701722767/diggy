import json
import boto3
import base64
from decimal import Decimal
from math import radians, cos, sin, asin, sqrt

AWS_REGION = "us-east-1"
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
events_table = dynamodb.Table('events')
MIN_DISTANCE = 900

def get_closest_events(center_coordinates):
    
    response = events_table.scan()
    
    if 'Items'not in response or not response['Items']:
        raise Exception("No existe ningún evento registrado")
    
    events = response['Items']
    closest_events = [event for event in events if isClose(event['coordinates'],center_coordinates)]
    return closest_events

def isClose(coordinates1,coordinates2):
    return distance(coordinates1,coordinates2) <= MIN_DISTANCE
    
def distance(coordinates1,coordinates2):
    
	lon1 = radians(coordinates1['longitude'])
	lon2 = radians(coordinates2['longitude'])
	lat1 = radians(coordinates1['latitude'])
	lat2 = radians(coordinates2['latitude'])
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * asin(sqrt(a))
	earth_radio = 6371
	return(c * earth_radio)*1000

def decodeBase64ToJson(base64Data):
    base64_bytes = base64Data.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return json.loads(message_bytes.decode('ascii'), parse_float=Decimal)
	
	
def lambda_handler(event, context):
    
    message = {
        "error" : False,
        "message": "Eventos cercanos encontrados exitosamente",
        "data" : {
            "items" : None
        }
    }
    
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': json.dumps(message)
    }
    
    try:
        base64_coordinates = event['queryStringParameters']['center_coordinates']
        center_coordinates = decodeBase64ToJson(base64_coordinates)
        message['data']['items'] = get_closest_events(center_coordinates)
        
    except Exception as e:
        message['error'] = True
        response['statusCode'] = 500
        message['message'] = str(e)
    
    response['body'] = json.dumps(message,default=str,ensure_ascii=False,)
    return response
    