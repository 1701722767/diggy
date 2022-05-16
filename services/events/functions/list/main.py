import boto3

dynamodb = boto3.resource('dynamodb')
eventsTable = dynamodb.Table('my-table')

class Request:
    """
    Request is the class used for handling the request
    """
    def __init__(self):
        self.err = None

    def process(self,event):
        response = eventsTable.scan()
        data = response['Items']

        return {
            "error": False,
            "message": "Eventos listados correctamente",
            "data" : response
        }

        # while 'LastEvaluatedKey' in response:
        #     response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        #     data.extend(response['Items'])
        # print("process")



def lambda_handler(event, context):
    """
    lambda_handler function that starts the lambda
    """
    _ = context
    req = Request()
    try:
        return req.process(event)

    except Exception as err:
        return {
            "error": True,
            "message": "Error interno en el servidor",
        }
    finally:
        if req.err is None:
            print(req.err)