import boto3
import json
import base64
from urllib.parse import parse_qs
import traceback

AWS_REGION = "us-east-1"
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

        user_id = self.message.get("user_id", "")
        if user_id == "":
            return False

        user_name = self.message.get("user_name", "")
        if user_name == "":
            print("not user name")
            return False

        reference_id = self.message.get("reference_id", "")
        if reference_id == "":
            return False

        description = self.message.get("description", "")
        if description == "":
            return False

        amount = self.message.get("amount", "")

        return amount != ""

    def process(self, message):
        self.message = message

        if not self.isValidateTransaction():
            return None

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
