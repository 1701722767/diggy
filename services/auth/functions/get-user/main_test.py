import pytest
import main


class TableUsersMock:
    def get_item(self, Key, ExpressionAttributeNames=None, ProjectionExpression=None):

        response = {
            "Item": {
                "birthdate": "2010-02-11",
                "phone_number": "+573137885484",
                "amount": "212000",
                "full_name": "Juan Pedro",
                "email": "juacagiri@gmail.com",
                "id": "bfff789e-8d09-43f1-b329-b3a47c2dda38",
                "user_name": "jgiradotest"
            }
        }

        return response


@pytest.mark.parametrize(
    "input,expected", [
        ({"requestContext": {
            "authorizer": {
                "claims": {
                    "sub": "bfff789e-8d09-43f1-b329-b3a47c2dda38",
                    "cognito:username": "jgiradotest"
                }
            }}},
            '{"error": false, "message": "Información de usuario encontrada", "data": {"birthdate": "2010-02-11", "phone_number": "+573137885484", "amount": "212000", "full_name": "Juan Pedro", "email": "juacagiri@gmail.com", "id": "bfff789e-8d09-43f1-b329-b3a47c2dda38", "user_name": "jgiradotest"}}'
         ),
        ({'queryStringParameters': None},
         '{"error": true, "message": "Error interno del servidor", "data": null}'
         )
    ]
)
def test_lambda_handler(input, expected):
    main.users_table = TableUsersMock()
    response = main.lambda_handler(input, {})
    print("response:")
    print(response['body'])
    assert response['body'] == expected
