import json
import boto3

PAGE_SIZE = 15
AWS_REGION = "us-east-1"

dynamodb = boto3.resource('dynamodb',region_name=AWS_REGION)
places_table= dynamodb.Table('places')

def list_places():
    response = places_table.scan(Limit = PAGE_SIZE)
    validate_dynamodb_response(response)
    return response['Items']
    
def validate_dynamodb_response(response):
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("Error interno")

def lambda_handler(event, context):
    # TODO implement
    
    response = {
        "error" : False,
        "message" : "Lugares listados correctamente",
        "data":None
    }
    
    try:
        response['data'] = list_places()
    except Exception as e:
        print(e)
        response['error'] = True
        response['message'] = "Error interno del servidor"
    
    return response
