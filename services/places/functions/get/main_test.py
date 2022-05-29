import pytest
import main


class TableEventMock:
    def get_item(self, Key, ExpressionAttributeNames=None, ProjectionExpression=None):

        response = {}

        places = [
            {
                "id": "Eb32e32fe-dde6-4b3c-9160-f01a67d60ab1",
                "category_id": "C01",
                "name": "Noche acústica",
                "coordinates": {
                    "latitude": 5.074297,
                    "longitude": -75.491561
                },
                "images": ["x", "y", "z"],
                "description": "Disfruta de una noche de música"
            }
        ]

        place_id = Key['id']
        category_id = Key['category_id']

        for place in places:
            if(place['id'] == place_id and place['category_id'] == category_id):
                response['Item'] = place

        return response


@pytest.mark.parametrize(
    "input,expected", [
        (
            {
                'queryStringParameters': {
                    'composite_key': "ewogICJldmVudF9pZCI6ICJFYjMyZTMyZmUtZGRlNi00YjNjLTkxNjAtZjAxYTY3ZDYwYWIxIiwKICAiY2F0ZWdvcnlfaWQiOiAiQzAxIgp9"
                }
            },
            '{"error": true, "message": "Búsqueda erronea", "data": null}'
        ),
        (
            {
                'queryStringParameters': {
                    'composite_key': "eyJpZCI6ICJQTDAwZDY1MmM4LTYwZDMtNGQ2Ni04NGE1LTIxZWVkZTFmNWQ3ZiIsICJjYXRlZ29yeV9pZCI6ICJDMDEifQ=="
                }
            },
            '{"error": true, "message": "No existe el lugar", "data": null}'
        ),
        (
            {
                'queryStringParameters': None
            },
            '{"error": true, "message": "Error interno del servidor", "data": null}'
        ),
        (
            {
                'queryStringParameters': {
                     'composite_key': "ewoiaWQiOiAiRWIzMmUzMmZlLWRkZTYtNGIzYy05MTYwLWYwMWE2N2Q2MGFiMSIsCiAgICAgICAgICAgICAgICAiY2F0ZWdvcnlfaWQiOiAiQzAxIgp9"
                }
            },
            '{"error": false, "message": "Lugar encontrado", "data": {"id": "Eb32e32fe-dde6-4b3c-9160-f01a67d60ab1", "category_id": "C01", "name": "Noche acústica", "coordinates": {"latitude": 5.074297, "longitude": -75.491561}, "images": ["x", "y", "z"], "description": "Disfruta de una noche de música"}}'
        )
    ]
)
def test_lambda_handler(input, expected):
    main.events_table = TableEventMock()
    response = main.lambda_handler(input, {})
    assert response['body'] == expected
