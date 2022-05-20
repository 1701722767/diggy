import boto3
import json
from boto3.dynamodb.conditions import Key

AWS_REGION = "us-east-1"

dynamodb = boto3.resource('dynamodb',region_name=AWS_REGION)
eventsTable = dynamodb.Table('events')


"""
Request is the class used for handling the request
"""
class Request:
    def __init__(self):
        self.err = None

    def setParameters(self,event):
        self.user_id = event["requestContext"]["authorizer"]["claims"]["sub"]
        self.body = json.loads(event["body"])

    def process(self,event):
        self.setParameters(event)

        event_id = self.body.get("event_id","")
        if event_id ==  "":
            raise  Exception("debe ingresar el id del evento")
        category_id = self.body.get("category_id","")
        if category_id ==  "":
            raise  Exception("debe ingresar el la categoria del evento")

        response = eventsTable.delete_item(
            Key = {'category_id':category_id,'event_id':event_id},
            ConditionExpression="user_id = :value",
            ExpressionAttributeValues={
                ":value": self.user_id
            }
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200 :

            # TODO: add code for notify users that hace realtion with this event
            # TODO: notify the payment service for return cash to accounts

             return {
                "error": False,
                "message": "Evento eliminado correctamente"
            }

        return {
            "error": True,
            "message": "No se logro eliminar el evento"
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

    except Exception as err:
        print(err)

        return {
            'statusCode': 200,
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