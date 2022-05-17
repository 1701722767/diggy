import json
import boto3
from decimal import Decimal

client = boto3.resource('dynamodb')
table = client.Table("events")

def create_event(event=None):
    
    # this will search for dynamoDB table 
    
    try:
        response = table.put_item(
            Item= {
            "event_id": event['event_id'],
            "category_id":event['category_id'],
            "event_name": event['event_name'],
            "event_coordinates": event['event_coordinates'],
            "event_images": event['event_images'],
            "event_description": event['event_description'],
            "event_range_age": event['event_range_age'],
            "event_price": event['event_price'],
            "event_slots": event['event_slots'],
            "event_max": event['event_max'],
            "event_datestart": event['event_datestart'],
            "event_dateend": event['event_dateend']
        })
    
        return response
    except Exception as e:
        print(str(e))
        raise Exception(str(e))

def validate(data):
    for name in data.keys():
        if not data[name]:
            print(name," missing")
            raise Exception(str(name))
            
def lambda_handler(event, context):
    # TODO implement
    response = {
        "error" : False,
        "message": "Event was created successfully",
        "data": None
    }
    
    try:
        new_event = {
            "event_id": event['event_id'],
            "category_id":event['category_id'],
            "event_name": event['event_name'],
            "event_coordinates": event['event_coordinates'],
            "event_images": event['event_images'],
            "event_description": event['event_description'],
            "event_range_age": event['event_range_age'],
            "event_price": event['event_price'],
            "event_slots": event['event_slots'],
            "event_max": event['event_max'],
            "event_datestart": event['event_datestart'],
            "event_dateend": event['event_dateend']
        }
        validate(new_event)
        new_event = json.loads(json.dumps(new_event), parse_float=Decimal)
        data = create_event(new_event)
        response['error'] = False
        response['data'] = data

    except Exception as e:
        response['error']  = True
        response['message'] = str(e).replace("'","")  + " missing"
    
    return response
        
    
    
