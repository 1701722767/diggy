import pytest
import main

class TableEventMock:
    def get_item(self,Key,ExpressionAttributeNames=None,ProjectionExpression=None):

        response = { }

        events = [
            { 
                "event_id" : "Eb32e32fe-dde6-4b3c-9160-f01a67d60ab1",
                "category_id":"C01",
                "name": "Noche acústica",
                "coordinates": {
                    "latitude": 5.074297 , 
                    "longitude": -75.491561
                },
                "images": ["x","y","z"],
                "description": "Disfruta de una noche de música",
                "range_age": [18,100],
                "price": 2000,
                "slots": 100,
                "max": 100,
                "datestart": "05-12-2022 21:00:00",
                "dateend": "05-12-2022 02:00:00"
            }
        ]

        event_id = Key['event_id']
        category_id = Key['category_id']


        for event in events:
            if(event['event_id'] == event_id and event['category_id'] == category_id):
                response['Item'] = event


        return response

@pytest.mark.parametrize(
    "input,expected",[
        ({'queryStringParameters':{
            'composite_key' :"ewogICJldmVudF9pZCI6ICJFYjMyZTMyZmUtZGRlNi00YjNjLTkxNjAtZjAxYTY3ZDYwYWIxIiwKICAiY2F0ZWdvcnlfaWQiOiAiQzAxIgp9"
            }}, 
        '{"error": false, "message": "Evento encontrado", "data": {"event_id": "Eb32e32fe-dde6-4b3c-9160-f01a67d60ab1", "category_id": "C01", "name": "Noche acústica", "coordinates": {"latitude": 5.074297, "longitude": -75.491561}, "images": ["x", "y", "z"], "description": "Disfruta de una noche de música", "range_age": [18, 100], "price": 2000, "slots": 100, "max": 100, "datestart": "05-12-2022 21:00:00", "dateend": "05-12-2022 02:00:00"}}'
        ),
        ({'queryStringParameters': None },
        '{"error": true, "message": "Error interno del servidor", "data": null}'
        )
    ]
)
def test_lambda_handler(input,expected):
    main.events_table = TableEventMock()
    response = main.lambda_handler(input,{})
    assert response['body'] == expected