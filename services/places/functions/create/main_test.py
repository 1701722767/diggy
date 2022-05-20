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

    req = main.Request()

    f = open('./samples/event.json')
    event = json.load(f)

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

    req = main.Request()

    f = open('./samples/event.json')
    event = json.load(f)
    event["body"] = '{"category_id":"CA101"}'

    response = main.lambda_handler(event,{})
    assert 400 == response["statusCode"], "Validate response"
    assert '{"error": true, "message": "Debe ingresar un nombre para el lugar"}' == response["body"], "Validate response"