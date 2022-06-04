import pytest
import main

class TableMock:
    def scan(self,FilterExpression={},ExclusiveStartKey={},Limit=50):
        return {
            "Items": {
                "category_id" : "category_id",
                "event_id" : "event_id"
            }
        }
class DynamoMock:
    def Table(self,table):
        assert "events" == table, "Validate table"
        return TableMock()

def test_handler():
    main.eventsTable = TableMock()
    main.dynamodb = DynamoMock()

    response = main.lambda_handler({
        "queryStringParameters": {
            "type": "own",
            "user_id": "user_id",
            "category_id": "C01"
        }
    },{})
    assert '{"error": false, "message": "Eventos listados correctamente", "data": {"items": {"category_id": "category_id", "event_id": "event_id"}}}' == response["body"], "Validate response 1"

    response = main.lambda_handler({
         "queryStringParameters": {
            "type": "default",
            "category_id": "C01"
        }
    },{})
    assert '{"error": false, "message": "Eventos listados correctamente", "data": {"items": {"category_id": "category_id", "event_id": "event_id"}}}' == response["body"], "Validate response 2"

def test_enconde_decode():

    class DynamoMock:
        def Table(self,table):
            assert "events" == table, "Validate table"

    main.dynamodb = DynamoMock()

    req = main.Request()


    base64 = req.encodeJSONToBase64({"data":"dummy"})
    json = req.decodeBase64ToJson(base64)

    assert base64 == "eyJkYXRhIjogImR1bW15In0=", "Validate base64"
    assert json == {"data":"dummy"}, "Validate json"