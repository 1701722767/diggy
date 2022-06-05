import pytest
import main


class TableMock():
    def scan(self, FilterExpression={}, ExclusiveStartKey={}, Limit=50):

        places = [
            {'name': 'PollosMarios', 'id': 'P01'},
            {'name': 'PollosJC', 'id': 'P02'}
        ]

        response = {
            'ResponseMetadata': {
                'HTTPStatusCode': 200
            },
            'Items': places,
            'LastEvaluatedKey': 'P01',
            'Count': 1
        }

        if(ExclusiveStartKey and (ExclusiveStartKey != places[0]['id'])):
            response['ResponseMetadata']['HTTPStatusCode'] = 500
            response['Items'] = []
            response['Count'] = 0

        return response


@pytest.mark.parametrize(
    "input,expected", [
        ({'queryStringParameters': {'type': 'default'}},
         '{"error": false, "message": "Lugares listados correctamente", "data": {"items": [{"name": "PollosMarios", "id": "P01"}, {"name": "PollosJC", "id": "P02"}], "start_key": "IlAwMSI="}}'
         ),
        ({'queryStringParameters': {'type': 'default','start_key': 'IlAwMSI='}},
         '{"error": false, "message": "Lugares listados correctamente", "data": {"items": [{"name": "PollosMarios", "id": "P01"}, {"name": "PollosJC", "id": "P02"}], "start_key": "IlAwMSI="}}'
         ),
        ({'queryStringParameters': {'type': 'default', 'start_key': 'P01'}},
         '{"error": true, "message": "Error interno en el servidor", "data": null}'
         )
    ]
)
def test_lambda_handler(input, expected):
    main.placesTable = TableMock()
    response = main.lambda_handler(input, {})
    assert response['body'] == expected


@pytest.mark.parametrize(
    "input", [
        (400),
        (500),
        (501)
    ]
)
def test_validate_dynamodb_response_failure(input):
    with pytest.raises(Exception) as e:
        main.validate_dynamodb_response(input)
