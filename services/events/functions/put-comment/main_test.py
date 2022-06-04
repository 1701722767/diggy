import pytest
import main
from decimal import Decimal

class TableEventMock:
    def get_item(self,Key, ProjectionExpression):


        events = [
                {
                    "event_id" : "E5b25ec9c-b545-421f-97d8-028aa27de16e",
                    "category_id" : "C01",
                    "score" : 3.1,
                    "total_comments" : 4
                }
            ]

        for event in events:
            if (Key['event_id'] == event['event_id'] and Key['category_id'] == event['category_id']):
                return {
                        'Item' : {
                            'score' : Decimal(event['score']),
                            'total_comments': Decimal(event['total_comments'])
                        }
                    }
        
        return {}

    def update_item(self,Key,UpdateExpression,ExpressionAttributeValues):
        response = {
                    "ResponseMetadata"  : {
                            "HTTPStatusCode": 200
                        }
                    }   

        events = [
                        {
                            "event_id" : "E5b25ec9c-b545-421f-97d8-028aa27de16e",
                            "category_id" : "C01",
                            "score" : 3.1,
                            "total_comments" : 4
                        }
                    ]

        for event in events:
            if (Key['event_id'] == event['event_id'] and Key['category_id'] == event['category_id']):
                return response

        response['ResponseMetadata']['HTTPStatusCode']  = 500
        return response

@pytest.mark.parametrize(
    "input,expected" ,[
        (
            {   "requestContext": { 
                    "authorizer" : {
                        "claims": {
                           "sub" : "abc"
                        }
                    } 
                },
               "body" : '{"full_name": "Nicolas Cardona","comment": "Me gustó","score": 3.2}',
               "queryStringParameters" : {
                   "composite_key" : "ew0KICJldmVudF9pZCI6ICJFNWIyNWVjOWMtYjU0NS00MjFmLTk3ZDgtMDI4YWEyN2RlMTZlIiwNCiAiY2F0ZWdvcnlfaWQiOiAiQzAxIg0KfQ=="
               }
           },
           '{"error": false, "message": "El comentario fue guardado exitosamente"}'
        ),
        (
            {   "requestContext": { 
                    "authorizer" : {
                        "claims": {
                           "sub" : "abc"
                        }
                    } 
                },
               "body" : '{"full_name": "Nicolas Cardona","comment": "Me gustó","score": 3.2}',
               "queryStringParameters" : {
                   "composite_key" : ""
               }
           },
           '{"error": true, "message": "No se indicó el evento ni la categoría"}'
        )
    ]
)
def test_lambda_handler(input,expected):
    main.events_table = TableEventMock()

    response = main.lambda_handler(input,{})

    assert response['body'] == expected