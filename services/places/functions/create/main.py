import boto3
import json
import uuid
from decimal import Decimal

PAGE_SIZE = 15
AWS_REGION = "us-east-1"
REQUIRED_ATTRIBUTES = {
    "category_id" : "Debe seleccionar una categoría",
    "name" : "Debe ingresar un nombre para el lugar",
    "coordinates" : "Debe ingresar una ubicaión"
}
  

dynamodb = boto3.resource('dynamodb',region_name=AWS_REGION)
places_table = dynamodb.Table('places')
categories_table = dynamodb.Table('categories')



"""
Request is the class used for handling the request
"""
class Request:
    def __init__(self):
        self.err = None

    def validateData(self,places_data):
        for attribute in REQUIRED_ATTRIBUTES.keys():
            if attribute not in places_data or not places_data[attribute]:
                raise KeyError(attribute)

    def get_category_name(self,category_id):
        response = categories_table.get_item(
            Key = { 'id' : category_id}
        )

        if 'Item' not in response:
            raise WrongInputException(f"No se encontró la categoría seleccionada")
            
        return response['Item']['name']



    def process(self,event):
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]

        places_data = json.loads(event["body"], parse_float=Decimal)
        self.validateData(places_data)

        category = self.get_category_name(places_data["category_id"])

        places_data["id"] = "PL" + str(uuid.uuid4())
        places_data["user_id"] = user_id
        places_data["category_name"] = category
        places_data["score"] = 0
        places_data["total_comments"] = 0

        response = places_table.put_item( Item=places_data )

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200 :
            return {
                "error": False,
                "message": "Lugar agregado correctamente"
            }

        return {
            "error": True,
            "message": "No se logro agregar el lugar"
        }

"""
lambda_handler function that starts the lambda
"""
def lambda_handler(event, context):
    _ = context
    req = Request()
    try:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json', 
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(req.process(event))
        }

    except KeyError as err:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                 'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(
                {
                    "error": True,
                    "message": REQUIRED_ATTRIBUTES[err.args[0]],
                }
            )
        }

    except Exception as err:
        print(err)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(
                {
                    "error": True,
                    "message": str(err),
                }
            )
        }
    finally:
        if req.err is None:
            print(req.err)