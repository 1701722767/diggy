import pytest
import main

class TableCategoryMock:
    def get_item(self,Key):

        # FAKE IDS FROM THE DATABASE 
        categories = [{
            'id' : 'C01',
            'name': 'Música'
        },
        {
            'id' : 'C02',
            'name': 'Deportes'
        }]

        response = {}

        for cat in categories:
            if(cat['id'] == Key['id']):
                response['Item'] = cat

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

    
