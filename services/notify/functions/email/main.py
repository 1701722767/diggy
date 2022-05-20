import json
import boto3
import json
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import templates

AWS_REGION = "us-east-1"
CHARSET = "UTF-8"
SENDER = "Diggy <sergio.1701510237@ucaldas.edu.co>"
REQUIRED_INPUTS = ['email','subject','template','data'];

client = boto3.client('ses',region_name=AWS_REGION)

class Request:
    """
    Request is the class used for handling the request
    """
    def __init__(self,message):
        self.message = message
        self.err = None

    def validate(self):
        for input in REQUIRED_INPUTS:
            if self.message.get(input,None) is None or self.message[input] == "":
                print("missing "+input)
                return False

        return True

    def process(self):
        if not self.validate():
            return None


        self.email = self.message['email']
        self.subject = self.message['subject']
        self.template = self.message['template']
        self.data = self.message['data']

        return self.send_email()

    def getBodyHtml(self):
        if templates.EMAILS_TEMPLATES.get(self.template,None) is None:
            return "" # for resturn a default in template

        return templates.EMAILS_TEMPLATES[self.template]


    def send_email(self):
        RECIPIENT = self.email
        SUBJECT = self.subject

        bodyHtml = self.getBodyHtml()

        client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': bodyHtml ,
                    }
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )


def getMessage(event):
    if event.get('Records', None) is None or len(event['Records']) <= 0:
        print('no records')
        return None

    if event['Records'][0].get('Sns',None) is None or event['Records'][0]['Sns'].get('Message',None) is None:
        print('no messages',event['Records'][0])
        return None

    return json.loads(event['Records'][0]['Sns']['Message'])

"""
lambda_handler function that starts the lambda
"""
def lambda_handler(event, context):
    try:
        _ = context
        message = getMessage(event)
        if message == None:
            return None

        req = Request(message)

        return req.process()

    except Exception as err:
        print(err)

        return err