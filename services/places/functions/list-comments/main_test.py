import pytest
import main

class TablePlaceMock:
    def get_item(self,Key,ExpressionAttributeNames=None,ProjectionExpression=None):
        response = { }
        places = [
            { 
                "category_id": "C03",
                "id": "PL56c82f49-72d6-4ca9-9dc3-187d4da1887d",
                "comments":[
                   {
                    "name": "Nicolás",
                    "comment": "Me gustó"
                   } 
                 ]
            }
        ]

        id = Key['id']
        category_id = Key['category_id']

        for place in places:
            if(place['id'] == id and place['category_id'] == category_id):
                response['Item'] = place['comments']
        return response
        
@pytest.mark.parametrize(
    "input,expected",[
        ({'queryStringParameters':{
            'composite_key' :"ew0KICJjYXRlZ29yeV9pZCI6ICJDMDMiLA0KICJpZCI6ICJQTDU2YzgyZjQ5LTcyZDYtNGNhOS05ZGMzLTE4N2Q0ZGExODg3ZCINCn0="
            }}, 
        '{"error": false, "message": "Lugar encontrado", "data": [{"name": "Nicolás", "comment": "Me gustó"}]}'
        )
    ]
)
def test_lambda_handler(input,expected):
    main.places_table = TablePlaceMock()
    response = main.lambda_handler(input,{})
    print(response['body'])
    assert response['body'] == expected