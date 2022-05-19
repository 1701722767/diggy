import pytest
import main
import json

def test_handler():
    class TableMock:
        def delete_item(self,Key,ConditionExpression,ExpressionAttributeValues):
            assert Key == {'category_id': 'CAT300', 'event_id': 'E101'}
            assert ConditionExpression == "user_id = :value"
            assert ExpressionAttributeValues == { ":value": "75fbab66-3446-468e-abe4-571cdd26ed54" }

            return {
                "ResponseMetadata" : {
                    "HTTPStatusCode" : 200
                }
            }

    main.eventsTable = TableMock()

    class DynamoMock:
        def Table(self,table):
            assert "events" == table, "Validate table"
            return TableMock()

    main.dynamodb = DynamoMock()

    req = main.Request()

    f = open('./samples/event.json')
    event = json.load(f)

    response = main.lambda_handler(event,{})
    assert '{"error": false, "message": "Evento eliminado correctamente"}' == response["body"], "Validate response"
