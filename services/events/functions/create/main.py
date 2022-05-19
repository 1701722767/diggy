import json
import boto3
from decimal import Decimal
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
import uuid

client = boto3.resource('dynamodb')
events_table = client.Table("events")
categories_table = client.Table("categories")

# UUID, Universal Unique Identifier, is a python library which helps
# in generating random objects of 128 bits as ids. 
# It provides the uniqueness as it generates ids on the basis of time, Computer hardware (MAC etc.).
def create_id():
    
    # # Generate a UUID from a host ID, sequence number, and the current time. If node is not given, 
    # # getnode() is used to obtain the hardware address. If clock_seq is given, it is used as the sequence number; 
    # # otherwise a random 14-bit sequence number is chosen.
    # new_id = "E" + str(uuid.uuid1())
    
    # Generate a random UUID.
    # probability of collision really really small
    new_id = "E" + str(uuid.uuid4())
    
    return new_id


def exists(category_id):
    
    select = "SPECIFIC_ATTRIBUTES"
    projection_expression = "category_id"
    
    response = categories_table.query(
        Select = select,
        ProjectionExpression=projection_expression,
        KeyConditionExpression=Key('category_id').eq(category_id)
    )
    if response['Count'] == 0:
        raise Exception(f"category_id = {category_id} not found")
    
def create_event(event):
    
    # this will search for dynamoDB table 
    
    new_id = create_id()
    
    try:
        exists(event['category_id'])
    except Exception as e:
        print(str(e))
        raise Exception(str(e))
        
    
    try:
        response = events_table.put_item(
            Item= {
            "event_id": new_id,
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
        response['data'] = data

    except Exception as e:
        response['error']  = True
        response['message'] = str(e).replace("'","") + " missing" 
    
    return response
        
    
    
