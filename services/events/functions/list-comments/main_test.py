import pytest
import main

class TableEventMock:
    def get_item(self,Key,ExpressionAttributeNames=None,ProjectionExpression=None):

        response = { }

        events = [
            { 
                "event_id" : "Eb32e32fe-dde6-4b3c-9160-f01a67d60ab1",
                "category_id":"C01",
                "comments":[
                   {
                    "name": "Nicolás",
                    "comment": "Me gustó"
                   } 
                 ]
            }
        ]

        event_id = Key['event_id']
        category_id = Key['category_id']

        for event in events:
            if(event['event_id'] == event_id and event['category_id'] == category_id):
                response['Item'] = event['comments']

        return response


@pytest.mark.parametrize(
    "input,expected",[
        ({'queryStringParameters':{
            'composite_key' :"ewogICJldmVudF9pZCI6ICJFYjMyZTMyZmUtZGRlNi00YjNjLTkxNjAtZjAxYTY3ZDYwYWIxIiwKICAiY2F0ZWdvcnlfaWQiOiAiQzAxIgp9"
            }}, 
        '{"error": false, "message": "Evento encontrado", "data": [{"name": "Nicolás", "comment": "Me gustó"}]}'
        )
    ]
)
def test_lambda_handler(input,expected):
    main.events_table = TableEventMock()
    response = main.lambda_handler(input,{})
    print(response['body'])
    assert response['body'] == expected