import pytest
import main
import json

def test_handler():
	x=5
	y=6
	assert x+1 == y,"test failed"
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
	assert "all is good siuuu" == response, "Validate output"