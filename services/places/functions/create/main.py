import boto3
import json
import uuid
from boto3.dynamodb.conditions import Key
from decimal import Decimal

PAGE_SIZE = 15
AWS_REGION = "us-east-1"
REQUIRED_ATTRIBUTES = [
    {
        "key": "category_id",
        "message" : "Debe seleccionar una categoría"
    },
    {
        "key": "name",
        "message" : "Debe ingresar un nombre para el lugar"
    },
    {
        "key": "coordinates",
        "message" : "Debe ingresar la ubicación del lugar"
    }
]

dynamodb = boto3.resource('dynamodb',region_name=AWS_REGION)
places_table = dynamodb.Table('places')
categories_table = dynamodb.Table('categories')

class WrongInputException(Exception):
    """Base class for other exceptions"""
    pass

"""
Request is the class used for handling the request
"""
class Request:
    def __init__(self):
        self.err = None

    def validateData(self,places_data):
        for attribute in REQUIRED_ATTRIBUTES:
            if places_data.get(attribute["key"],"") == "":
                raise WrongInputException(attribute["message"])

    def existsCategory(self,category_id):
        response = categories_table.query(
            KeyConditionExpression=Key('category_id').eq(category_id)
        )

        if response['Count'] == 0:
            raise WrongInputException(f"No se encontró la categoría seleccionada")



    def process(self,event):
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]

        places_data = json.loads(event["body"], parse_float=Decimal)
        self.validateData(places_data)

        self.existsCategory(places_data["category_id"])

        places_data["id"] = "PL" + str(uuid.uuid4())
        places_data["user_id"] = user_id

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
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(req.process(event))
        }

    except WrongInputException as err:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(
                {
                    "error": True,
                    "message": str(err),
                }
            )
        }

    except Exception as err:
        print(err)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
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