import pytest
import main

def test_handler():

    class DynamoMock:
        def Table(self,table):
            assert "events" == table, "Validate table"

    main.dynamodb = DynamoMock()

    req = main.Request()


    base64 = req.encodeJSONToBase64({"data":"dummy"})
    json = req.decodeBase64ToJson(base64)

    assert base64 == "eyJkYXRhIjogImR1bW15In0=", "Validate base64"
    assert json == {"data":"dummy"}, "Validate json"