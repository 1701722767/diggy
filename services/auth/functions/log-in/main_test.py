import pytest
import main
import json


def test_handler():
    class CognitoMock:
        def initiate_auth(self, ClientId, AuthFlow, AuthParameters):

            return {
                "AuthenticationResult": {
                    "IdToken": "token-response"
                }
            }

    main.client = CognitoMock()

    event = {
        "username": "nicolascr181",
        "password": "12345678"
    }

    response = main.lambda_handler(event, {})
    assert {
        'data': {'access_token': 'token-response'},
        'error': False,
        'message': 'Inicio de sesión exitoso'
    } == response, "Validate response"
