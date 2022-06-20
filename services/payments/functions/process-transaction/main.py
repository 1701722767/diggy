import boto3
import json
import base64
from urllib.parse import parse_qs
import traceback
from datetime import datetime, timedelta

AWS_REGION = "us-east-1"
REQUIRED_FIELDS = ['user_id','user_name','reference_id','description','amount']
dynamoClient = boto3.client('dynamodb', region_name=AWS_REGION)


"""
Request is the class used for handling the request
"""
class Request:

    def __init__(self):
        self.err = None

    def isValidateTransaction(self):
        if self.message is None:
            return False

        for field in REQUIRED_FIELDS:
            if self.message.get(field, "") == "":
                return False

        return True

    def process(self, message):
        self.message = message

        if not self.isValidateTransaction():
            return None

        date = datetime.now() - timedelta(hours=5)

        response = dynamoClient.transact_write_items(
            TransactItems=[
                {
                    'Update': {
                        'TableName': 'users',
                        'Key': {
                            'id': {'S': self.message["user_id"]},
                            'user_name': {'S': self.message["user_name"]},
                        },
                        'ExpressionAttributeValues': {
                            ":value": {'N': str(self.message["amount"])},
                        },
                        'UpdateExpression': "SET amount = amount + :value",
                        'ReturnValuesOnConditionCheckFailure': 'NONE'
                    }
                },
                {
                    'Put': {
                        'TableName': 'transactions',
                        'Item': {
                            'user_id': {'S': self.message["user_id"]},
                            'reference_id': {'S': self.message["reference_id"]},
                            'description': {'S': self.message["description"]},
                            'date': {'S': date.strftime("%m/%d/%Y, %H:%M:%S")},
                            'amount': {'N': str(self.message["amount"])}
                        },
                        'ConditionExpression': 'attribute_not_exists(reference_id)',
                        'ReturnValuesOnConditionCheckFailure': 'NONE'
                    }
                }
            ]
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return None

        raise("save transaction failed")


"""
lambda_handler function that starts the lambda
"""


def lambda_handler(event, context):
    _ = context
    req = Request()
    try:
        message = json.loads(event["Records"][0]["body"])

        return req.process(message)

    except Exception as err:
        print(traceback.format_exc())
        req.err = err
    finally:
        if req.err != None:
            return req.err
