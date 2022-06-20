import pytest
import main
import json


class DynamoMock:
    def transact_write_items(self,TransactItems):
        assert len(TransactItems) == 2, "validate transaction items"

        return {
            "ResponseMetadata": {
                "HTTPStatusCode": 200
            }
        }


def test_handler():
    main.dynamoClient = DynamoMock()

    transaction = json.dumps({
        "user_id": "89e44df6-b8ca-4962-a842-5d336709ee00",
        "user_name": "jgiraldor",
        "amount": "40000",
        "reference_id": "12345",
        "description": "test"
    })

    response = main.lambda_handler(
        {
            "Records": [
                {
                    "body": transaction,
                }
            ]
        }, {})
    assert None == response, "Validate output"
