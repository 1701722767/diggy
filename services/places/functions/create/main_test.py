import pytest
import main
import json

def test_handler():
    class TableMock:
        def query(self,KeyConditionExpression):
            assert None != KeyConditionExpression, "validate query"
            return {
                "Count": 1
            }
        def put_item(self,Item):
            assert "Nuevo evento" == Item["name"], "validate Item"
            return {
                "ResponseMetadata"  : {
                    "HTTPStatusCode": 200
                }
            }

    main.categories_table = TableMock()
    main.places_table = TableMock()

    class DynamoMock:
        def Table(self,table):
            assert "events" == table, "Validate table"
            return TableMock()

    main.dynamodb = DynamoMock()

    event = {
        "requestContext": {
            "authorizer": {
                "claims": {
                    "sub": "75fbab66-3446-468e-abe4-571cdd26ed54"
                }
            }
        },
        "body" : '{"category_id" : "CAT300","name" : "Nuevo evento", "coordinates": {"latitude" : 5.074297,"longitude" : -75.491561}}'
    }

    response = main.lambda_handler(event,{})
    assert '{"error": false, "message": "Lugar agregado correctamente"}' == response["body"], "Validate response"


def test_handler_missin_name():
    class TableMock:
        def query(self,KeyConditionExpression):
            assert None != KeyConditionExpression, "validate query"
            return {
                "Count": 1
            }
        def put_item(self,Item):
            assert "Nuevo evento" == Item["name"], "validate Item"
            return {
                "ResponseMetadata"  : {
                    "HTTPStatusCode": 200
                }
            }

    main.categories_table = TableMock()
    main.places_table = TableMock()

    class DynamoMock:
        def Table(self,table):
            assert "events" == table, "Validate table"
            return TableMock()

    main.dynamodb = DynamoMock()

    event = {
        "requestContext": {
            "authorizer": {
                "claims": {
                    "sub": "75fbab66-3446-468e-abe4-571cdd26ed54"
                }
            }
        },
        "body" : '{"category_id":"CA101"}'
    }

    response = main.lambda_handler(event,{})
    assert 400 == response["statusCode"], "Validate response"
    assert '{"error": true, "message": "Debe ingresar un nombre para el lugar"}' == response["body"], "Validate response"