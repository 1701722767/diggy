import boto3
import json
import base64
from urllib.parse import parse_qs
import traceback

AWS_REGION = "us-east-1"
TRANSACTION_QUEUE = "https://sqs.us-east-1.amazonaws.com/605550406178/payments-transactions-queue"
sqsClient = boto3.client('sqs',region_name=AWS_REGION)


"""
Request is the class used for handling the request
"""


class Request:

    def __init__(self):
        self.err = None

    def isValidateWebhook(self):
        if self.meessage is None:
            return False

        state_pol = self.meessage.get("state_pol", "")
        if state_pol == "" or state_pol[0] != "4":
            False

        response_message_pol = self.meessage.get("response_message_pol", "")

        return response_message_pol != "" and response_message_pol[0] == "APPROVED"

    def createTransaction(self):
        value = self.meessage.get("value", "")
        if value == "" or len(value) != 1:
            return None

        amount = float(value[0])

        reference_sale = self.meessage.get("reference_sale", "")
        if reference_sale == "" or len(reference_sale) != 1:
            return None

        reference_sale = reference_sale[0]
        user_id = reference_sale.split('#')[0]

        return {
            "user_id": user_id,
            "amount": amount
        }

    def sendTransaction(self, transaction):
        response = sqsClient.send_message(
            QueueUrl=TRANSACTION_QUEUE,
            MessageBody=json.dumps(transaction))

        print(response)

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return None

        raise("send to sqs payments failed")

    def process(self, message):
        self.meessage = message

        if not self.isValidateWebhook():
            return None

        transaction = self.createTransaction()
        if transaction is None:
            return None

        return self.sendTransaction(transaction)

    def decodeBase64ToString(self, base64Data):
        base64_bytes = base64Data.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        return message_bytes.decode('ascii')


"""
lambda_handler function that starts the lambda
"""


def lambda_handler(event, context):
    _ = context
    req = Request()
    try:
        message = parse_qs(req.decodeBase64ToString(
            event["Records"][0]["body"]))

        return req.process(message)

    except Exception as err:
        print(traceback.format_exc())
        req.err = err
    finally:
        if req.err != None:
            return req.err
