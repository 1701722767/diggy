import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr
import uuid

AWS_REGION = "us-east-1"
KEY_ERROR_MESSAGE = {
    "category_id": "La categoría no existe o no fue seleccionada",
    "user_id" : "No se indicó el usuario al cual le pertenece el evento",
    "name": "Debe escribir el nombre del evento",
    "coordinates": "Es necesaria la ubicación del evento",
    "images": "El evento debe tener imagenes",
    "description": "El evento debe tener una descripción",
    "range_age": "El rango de edad debe ser selecionado",
    "price": "Debe indicar el precio del evento",
    "slots": "Debe indicar los cupos disponibles actuales del evento",
    "max": "Debe ingresar la cantidad máxima de personas al evento",
    "datestart": "Debe ingresar la hora y fecha de inicio del evento",
    "dateend": "Debe ingresar la hora y fecha en la cual termina el evento"
}

client = boto3.resource('dynamodb',region_name=AWS_REGION)
events_table = client.Table("events")
categories_table = client.Table("categories")


def create_id():    
    return "E" + str(uuid.uuid4())

def exists(category_id):
    
    select = "SPECIFIC_ATTRIBUTES"
    projection_expression = "id"
    
    response = categories_table.query(
        Select = select,
        ProjectionExpression=projection_expression,
        KeyConditionExpression=Key('id').eq(category_id)
    )
    if response['Count'] == 0:
        raise KeyError("category_id")
    
def create_event(event):

    exists(event['category_id'])
    response = events_table.put_item(
        Item= {
        "event_id": create_id(),
        "user_id": event['user_id'],
        "category_id":event['category_id'],
        "name": event['name'],
        "coordinates": event['coordinates'],
        #"images": event['images'],
        "description": event['description'],
        "range_age": event['range_age'],
        "price": event['price'],
        "slots": event['slots'],
        "max": event['max'],
        "datestart": event['datestart'],
        "dateend": event['dateend']
    })
    validate_dynamodb_response(response)
        
    return response


def validate(data):
    for name in data.keys():
        if not data[name]:
            raise KeyError(str(name))


def validate_dynamodb_response(response):
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("Error interno en la base de datos")
            
def lambda_handler(event, context):
   
    message = {
        "error" : False,
        "message": "El evento fue creado exitosamente",
    }
    
    response = {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(message)
    }
    
    
    
    try:
        
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]
        event_data = json.loads(event["body"], parse_float=Decimal)
        new_event = {
           
            "category_id":event_data['category_id'],
            "user_id": user_id,
            "name": event_data['name'],
            "coordinates": event_data['coordinates'],
            #"images": event_data['images'],
            "description": event_data['description'],
            "range_age": event_data['range_age'],
            "price": event_data['price'],
            "slots": event_data['slots'],
            "max": event_data['max'],
            "datestart": event_data['datestart'],
            "dateend": event_data['dateend']
        }
        validate(new_event)
        create_event(new_event)
       
        
    except KeyError as e:
        print(e)
        message['error']  = True
        message['message'] = KEY_ERROR_MESSAGE[e.args[0]]
        response['statusCode'] = 400
        
    except Exception as e:
        print(e)
        message['error']  = True
        message['message'] = "Error interno en el servidor"
        response['statusCode'] = 500
        
    
    response['body'] = json.dumps(message,ensure_ascii=False)
    return response
        
    
    
