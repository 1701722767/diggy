import pytest
import main
import json
import templates
import boto3

def test_handler():
	class clientMock:
		def send_email(self,Destination={},Message={},Source={}):
			assert Destination == {'ToAddresses': ['sergiomontao19@hotmail.com']}, "Validate destination"
			assert Message['Body']['Html']['Data'] == templates.EMAILS_TEMPLATES['register'], "Validate body"
			assert Source == main.SENDER, "Validate destination"

	main.client = clientMock()

	response = main.lambda_handler({
		'Records': [
			{
				'Sns' : {
					'Message' : json.dumps(
						{
							"email":"sergiomontao19@hotmail.com",
							"subject": "test",
							"template": "register",
							"data" : "data"
						}
					),
				}
			}
		]
	}, {})
	assert response == None, "Validate output"

	main.client = boto3.client('ses',region_name=main.AWS_REGION)

def test_handler_failed():
	response = main.lambda_handler({
		'Records': [
			{
				'Sns' : {
					'Message' : json.dumps(
						{
							"email":"sergiomontao19@hotmail.com",
							"subject": "test",
							"template": "register",
							"data" : "data"
						}
					),
				}
			}
		]
	}, {})
	assert str(response) == 'Unable to locate credentials', "Validate output error"



def test_handler_missing_params(mocker):
	response = main.lambda_handler({
		'Records': [
			{
				'Sns' : {
					'Message' : json.dumps(
						{
							"email":"",
							"subject": "test",
							"template": "register",
							"data" : "data"
						}
					),
				}
			}
		]
	}, {})
	assert response == None, "Validate output none"