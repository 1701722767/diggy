import pytest
import main


class TableMock():
    def scan(self,Limit, ExclusiveStartKey=None):

        places = [
            {'name' : 'PollosMarios','id' : 'P01'},
            {'name' : 'PollosJC','id' : 'P02'}
        ]

        response = {
            'ResponseMetadata' :{
                'HTTPStatusCode': 200
            },
            'Items': places,
            'LastEvaluatedKey' : 'P01'
        }

        if(ExclusiveStartKey and (ExclusiveStartKey != places[0]['id'])):
            response['ResponseMetadata']['HTTPStatusCode'] = 500
            response['Items'] = []

        return response

@pytest.mark.parametrize(
    "input,expected",[
        ({ 'queryStringParameters' : None},
        '{"error": false, "message": "Lugares listados correctamente", "data": {"Items": [{"name": "PollosMarios", "id": "P01"}, {"name": "PollosJC", "id": "P02"}], "last_evaluated_key": "IlAwMSI="}}'
        ),
        ({ 'queryStringParameters' : {
            'last_evaluated_key': 'IlAwMSI='}},
        '{"error": false, "message": "Lugares listados correctamente", "data": {"Items": [{"name": "PollosMarios", "id": "P01"}, {"name": "PollosJC", "id": "P02"}], "last_evaluated_key": "IlAwMSI="}}'
        ),
        ({ 'queryStringParameters' : {
            'last_evaluated_key': 'P01'}},
        '{"error": true, "message": "Error interno del servidor", "data": null}'
        )
    ]
)
def test_lambda_handler(input,expected):
    main.places_table = TableMock()
    response =  main.lambda_handler(input,{})
    assert response['body'] == expected

@pytest.mark.parametrize(
    "input",[
        (400),
        (500),
        (501)
    ]
)
def test_validate_dynamodb_response_failure(input):
    with pytest.raises(Exception) as e:
        main.validate_dynamodb_response(input)



