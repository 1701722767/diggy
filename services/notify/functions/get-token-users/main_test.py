import main
import pytest

class TableUsersMock:
    def scan(self,FilterExpression,ProjectionExpression):
        return {
            'Items':{
                'FCM_token' : 'C-dfgDFG-dfgD-gdgwerZd'
            }
        }
    
class TableCategoriesMock:
    def get_item(self,Key):
        return {
            'Item':{
                "id" : 'C01'
            }
        }

@pytest.mark.parametrize(
    "input,expected",[
        (
            {
                "queryStringParameters":{
                    "category_id" : "C01"
                }
            },
            '{"error": false, "message": "Tokens obtenidos", "data": {"items": {"FCM_token": "C-dfgDFG-dfgD-gdgwerZd"}}}'
        )
    ]
)
def test_lambda_handler(input,expected):
    main.users_table = TableUsersMock()
    main.categories_table = TableCategoriesMock()
    response = main.lambda_handler(input,{})
    assert response['body'] == expected
