import boto3
import json
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


'''El evento contiene los siguientes elementos:
    -Email: Correo que se registró por parte del usuario
    -Tipo:
    -Template:
    -data:
'''

def lambda_handler(event, context):

    _ = context
    req = Request()
    message= event['email']

    try:
        if message is not None:
            req.process(event)   
            send_email(message)
        else return print("No se encontro el correo")

    except Exception as err:
        print(err)
    finally:
        if req.err is None:
            return "Correo enviado con éxito"
        else:
            return "El correo no pudo ser enviado"

def send_email(message):
    # Correo desde el cual se envia el email. 
    SENDER = "Diggy <sergio.1701510237@ucaldas.edu.co>"

    #Correo del destinatario. 
    #Se puede establecer por medio de la consulta y los datos obtenidos de la API.
    RECIPIENT = message

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    #CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "Correo de prueba"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Correo de prueba para envio de mensaje\r\n"
                "Correo de prueba para usuarios registrados en DB "
                )
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Bienvenido usuario</h1>
    <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
        AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
                """            

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])