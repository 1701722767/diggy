import json
import boto3
import uuid
import base64

AWS_REGION = "us-east-1"
TRANSACTION_QUEUE = "https://sqs.us-east-1.amazonaws.com/605550406178/payments-transactions-queue"

client = boto3.resource('dynamodb', region_name=AWS_REGION)
events_table = client.Table("events")
users_table = client.Table("users")
sqsClient = boto3.client('sqs', region_name=AWS_REGION)


class CustomError(Exception):
    pass


def create_reference_id():
    return str(uuid.uuid4())


def get_event(composite_key):
    response = events_table.get_item(
        Key=decodeBase64ToJson(composite_key),
    )

    if 'Item' not in response:
        raise KeyError("No existe dicho evento")

    if 'user_id' in response['Item']:
        del response['Item']['user_id']

    return response['Item']


def decodeBase64ToJson(base64Data):
    base64_bytes = base64Data.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return json.loads(message_bytes.decode('ascii'))

def get_user(id, user_name):
    response = users_table.get_item(
        Key={
            "id": id,
            "user_name": user_name
        },
    )

    if 'Item' not in response:
        raise KeyError("No existe el usuario")

    return response['Item']

def sendTransaction(self, transaction):
    response = sqsClient.send_message(
        QueueUrl=TRANSACTION_QUEUE,
        MessageBody=json.dumps(transaction))

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return None

    raise("send to sqs payments failed")

def reserve(event):
    reference = create_reference_id()
    event_compositive_key = event['queryStringParameters']['composite_key']
    event = get_event(event_compositive_key)

    if event.slots <= 0:
        raise CustomError("No quedan cupos disponibles")

    id = event["requestContext"]["authorizer"]["claims"]["sub"]
    user_name = event["requestContext"]["authorizer"]["claims"]['cognito:username']
    user = get_user(id, user_name)
    if user.amount <= 0:
         raise CustomError("No tiene saldo disponible por favor recarge su cuenta en balance")

    transaction = {
        "user_id" : id,
        "user_name" : user_name,
        "reference_id": reference,
        "description": "Reserva " + event.name,
        "amount": event.price * -1
    }

    sendTransaction(transaction)

def lambda_handler(event, context):

    message = {
        "error" : False,
        "message": "Reserva creada con éxito puede verificarla revisando las transacciones.",

    }

    response = {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(message)
    }



    try:

        reserve(event)


    except KeyError as e:
        print(e)
        message['error']  = True
        message['message'] = KEY_ERROR_MESSAGE[e.args[0]]
        response['statusCode'] = 400

    except CustomError as e:
        message['error'] = True
        message['message'] = str(e)
        response['statusCode'] = 404

    except Exception as e:
        print(e)
        message['error']  = True
        message['message'] = "Error interno en el servidor"
        response['statusCode'] = 500


    response['body'] = json.dumps(message,ensure_ascii=False)
    return response



