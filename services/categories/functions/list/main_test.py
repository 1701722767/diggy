import pytest
import main

def test_handler():
    class TableMock:
        def scan(self,Limit=50):
            return {
                "Items": {
                    "category_id" : "category_id",
                    "category_name" : "name"
                }
            }

    main.categories_table = TableMock()

    class DynamoMock:
        def Table(self,table):
            assert "categories" == table, "Validate table"
            return TableMock()

    main.dynamodb = DynamoMock()

    req = main.Request()


    response = main.lambda_handler({},{})
    assert {
        "data": {
            "items": {"category_id": "category_id", "category_name": "name"}},
            "error": False,
            "message": "Categorias listadas correctamente"
    } == response, "Validate response"

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