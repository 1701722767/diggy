import json
import boto3
from decimal import Decimal

AWS_REGION = "us-east-1"
KEY_ERROR_MESSAGE = {
    "event_id" : "No se indicó el evento al cual se comentará",
    "category_id" : "No se indicó la categoría",
    "user_id" : "No se indicó el usuario que escribió el comentario",
    "full_name": "El nombre es obligatorio",
    "comment": "El comentario no puede estar vacío",
    "score" : "Es obligatorio indicar el puntaje"
}

client = boto3.resource('dynamodb',region_name=AWS_REGION)
events_table = client.Table("events")

def put_comment(comment_info):
    
    validate(comment_info)
    
    new_comment = {
        "user_id" : comment_info['user_id'],
        "full_name": comment_info['full_name'],
        "comment": comment_info['comment'],
        "score": comment_info['score']
    }
    
    key = {
            "event_id" : comment_info['event_id'],
            "category_id" : comment_info['category_id']
         }
    
    old_score, total = get_score_comments(key)
    
    new_score = compute_score(old_score,total + 1 ,comment_info['score'])
    
   
    response = events_table.update_item(
        Key = key,
        UpdateExpression = 
        "SET comments=list_append(if_not_exists (comments, :empty_list),:new_comment)," + 
        "score=:new_score," + 
        "total_comments=total_comments + :one",
        ExpressionAttributeValues={
            ":new_comment": [new_comment],
            ":empty_list" : [],
            ":new_score":new_score,
            ":one":1,
            }
        )
        
    validate_dynamodb_response(response)
    
def compute_score(old_score,total,score):
    return ((old_score)*(total - 1) + score) / total

def get_score_comments(key):
    response = events_table.get_item(
        Key = key,
        ProjectionExpression = "score,total_comments"
        )
    if 'Item' not in response:
        raise Exception("El evento no existe")
        
    if 'score' not in response['Item'] or 'total_comments' not in response['Item']:
        raise Exception("El evento no tiene los atributos score y total_comments")
    
    return response['Item']['score'],response['Item']['total_comments']
    

def validate(data):
    for key in KEY_ERROR_MESSAGE.keys():
        if key not in data.keys() or not data[key]:
            raise KeyError(key)


def validate_dynamodb_response(response):
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception("Error interno en la base de datos")
            
def lambda_handler(event, context):
   
    message = {
        "error" : False,
        "message": "El comentario fue guardado exitosamente"
    }
    
    response = {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(message)
    }
    
    try:
        
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]
        event_data = json.loads(event["body"], parse_float=Decimal)
        event_data['user_id'] = user_id
        
        put_comment(event_data)

    except KeyError as e:
        print(e)
        message['error']  = True
        message['message'] = KEY_ERROR_MESSAGE[e.args[0]]
        response['statusCode'] = 400
        
    except Exception as e:
        print(e)
        message['error']  = True
        message['message'] = str(e)
        response['statusCode'] = 500
        
    
    response['body'] = json.dumps(message,ensure_ascii=False)
    return response
        
    
    
