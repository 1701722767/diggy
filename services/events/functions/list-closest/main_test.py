import pytest
import main

class TableEventMock():
    def scan(self):
        return {
            "Items":[
                {
                    "coordinates" : {
                        "latitude" : 9.10,
                        "longitude" : 8.5
                    }
                },
                {
                    "coordinates" : {
                        "latitude" : 9.10,
                        "longitude" : 8.5
                    }
                }
            ]
        }


@pytest.mark.parametrize(
    "input,expected",[
        (
            {
                "requestContext":{
                    "identity":{
                        "sourceIp": "191.95.160.92"
                    }
                },
                "queryStringParameters": 
                {
                    "center_coordinates": "ew0KICAgICJsYXRpdHVkZSIgOiA1My4zMTg2MTExMTExMTExMSwNCiAgICAibG9uZ2l0dWRlIiA6IC0xLjY5OTcyMjIyMjIyMjIyMjMNCn0="
                }
            },
            '{"error": false, "message": "Eventos cercanos encontrados exitosamente", "data": {"items": []}}'
        )
    ]
)
def test_lambda_handler(input,expected):
    main.events_table = TableEventMock()
    response = main.lambda_handler(input,{})
    print(response['body'])
    assert response['body'] == expected
        

