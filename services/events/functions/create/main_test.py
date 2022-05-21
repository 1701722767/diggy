import pytest
import main

class TableCategoryMock:
    def query(self,Select,ProjectionExpression,KeyConditionExpression):

        # FAKE IDS FROM THE DATABASE 
        categories_id = ['C01']

        response = {
            'Count' : 1
        }

        if KeyConditionExpression._values[1] not in categories_id:
            response['Count'] = 0
        return response

class TableEventMock:
    def put_item(self,Item):
        response = {
             "ResponseMetadata"  : {
                    "HTTPStatusCode": 200
                }
        }
        if not Item:
            response["ResponseMetadata"]["HTTPStatusCode"] = 500
        
        return response

@pytest.mark.parametrize(
    "input",[
        ("C010"),
        ("B120"),
        ("24324342")
    ]
)
def test_exists_category_failure(input):    
    main.categories_table = TableCategoryMock()

    with pytest.raises(KeyError) as e:
        main.exists(input)


#Each tuple is a test case
@pytest.mark.parametrize(
    "input,expected" , [
        (
           {   "requestContext": { 
                    "authorizer" : {
                        "claims": {
                           "sub" : "abc"
                        }
                    } 
                },

               "body" : '{ "category_id": "C01", "name": "Noche acústica","coordinates": {"latitude": 5.074297 , "longitude": -75.491561 },"images": ["x","y","z"],"description": "Disfruta de una noche de música","range_age": [18,100],"price": 2000,"slots": 100,"max": 100,"datestart": "05-12-2022 21:00:00","dateend": "05-12-2022 02:00:00"}'
           },
           '{"error": false, "message": "El evento fue creado exitosamente"}'
        ),
        (
           {   "requestContext": { 
                    "authorizer" : {
                        "claims": {
                           "sub" : "abc"
                        }
                    } 
                },

               "body" : '{ "category_id": "C10", "name": "Noche acústica","coordinates": {"latitude": 5.074297 , "longitude": -75.491561 },"images": ["x","y","z"],"description": "Disfruta de una noche de música","range_age": [18,100],"price": 2000,"slots": 100,"max": 100,"datestart": "05-12-2022 21:00:00","dateend": "05-12-2022 02:00:00"}'
           },
           '{"error": true, "message": "La categoría no existe o no fue seleccionada"}'
        ),
        (
           {   "requestContext": { 
                    "authorizer" : {
                        "claims": {
                           "sub" : "abc"
                        }
                    } 
                },

               "body" : '{ "category_id": "", "name": "Noche acústica","coordinates": {"latitude": 5.074297 , "longitude": -75.491561 },"images": ["x","y","z"],"description": "Disfruta de una noche de música","range_age": [18,100],"price": 2000,"slots": 100,"max": 100,"datestart": "05-12-2022 21:00:00","dateend": "05-12-2022 02:00:00"}'
           },
           '{"error": true, "message": "La categoría no existe o no fue seleccionada"}'
        ),
        (
           {   "requestContext": { 
                    "authorizer" : {
                        "claims": {
                           "sub" : "abc"
                        }
                    } 
                },

               "body" : '{ "category_id": "C01", "name": "","coordinates": {"latitude": 5.074297 , "longitude": -75.491561 },"images": ["x","y","z"],"description": "Disfruta de una noche de música","range_age": [18,100],"price": 2000,"slots": 100,"max": 100,"datestart": "05-12-2022 21:00:00","dateend": "05-12-2022 02:00:00"}'
           },
           '{"error": true, "message": "Debe escribir el nombre del evento"}'
        ),
        (
           {   "requestContext": { 
                    "authorizer" : {
                        "claims": {
                           "sub" : "abc"
                        }
                    } 
                },

               "body" : '{ "category_id": "C01", "name": "Noche Acústica","images": ["x","y","z"],"description": "Disfruta de una noche de música","range_age": [18,100],"price": 2000,"slots": 100,"max": 100,"datestart": "05-12-2022 21:00:00","dateend": "05-12-2022 02:00:00"}'
           },
           '{"error": true, "message": "Es necesaria la ubicación del evento"}'
        )
    ]
)


def test_lambda_handler(input,expected):
    main.categories_table = TableCategoryMock()
    main.events_table = TableEventMock()

    response = main.lambda_handler(input,{})

    assert response['body'] == expected

    




