import json
import os
import boto3
from dotenv import load_dotenv, find_dotenv

def authenticate():
    
    load_dotenv(find_dotenv())
    
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env-sample")
    load_dotenv(dotenv_path)
    
    username = "usertest04"
    password = "#Abc1234"
    
    client = boto3.client("cognito-idp", region_name="us-east-1")
     # Autenticarse con codigo enviado al smartphone
    response = client.respond_to_auth_challenge(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
        ChallengeName='SMS_MFA',
        ChallengeResponses = {'USERNAME':username, 'SMS_MFA_CODE':'314343'},
        Session = "AYABeF_y3cO2o7EktNyOir5x1QAAHQABAAdTZXJ2aWNlABBDb2duaXRvVXNlclBvb2xzAAEAB2F3cy1rbXMAS2Fybjphd3M6a21zOnVzLWVhc3QtMTo3NDU2MjM0Njc1NTU6a2V5L2IxNTVhZmNhLWJmMjktNGVlZC1hZmQ4LWE5ZTA5MzY1M2RiZQC4AQIBAHiG0oCCDoro3IaeecGyxCZJOVZkUqttbPnF4J7Ar-5byAGsRiyH2qbDOK4kF5VhOgN9AAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMxonJn_ZlW1tMWfw1AgEQgDuf2luvUAqZPpN2DnOAySB8Sqj40fmBOW0S5vjwmv6fceq36C2PQfiMVP7Fhks-MBhb1XUsakh-bEAIfQIAAAAADAAAEAAAAAAAAAAAAAAAAAByQPLwxaB8G7mHKvo1-5SE_____wAAAAEAAAAAAAAAAAAAAAEAAAHBNcxR8bCGCHY9ZOi9K_qxfhNvJxQctsyjCbMuts4GJScUhpeo5q-QSHFzi2DOWjU0S71Cy4XZPxormBN--Wu81gC-LZgXVHRkNrZi-S2hKGYO3yQuMIsxs1AHgZlp_Q22nhD7MsCrRhYIE5w01pVFBNbDsoIhcGbEx3LQ-irMNgvwV4sIXkgDdSJZTRhkUExSkK1JOUd-nACoz35pMlZ0roRAO6CqrdX5qGWcxVC6dxvZF7U2bNun7h6VQz9G19DCZvvew7ClgU6XVEnYy7-yYa-MObud1Sdm3l7P3nufaxfCcd_zWWE4P785w7tcVLDQF6HgSONI6HhduEQtuLEd5PC281NOerj_oXPGwEXi89LeaFL2xceByPUQeCksuUQLg8iDWZWL93PvtkKJjpy2FHsZXuF-ruDikLy-l0zmMuSdn3cjmQY7A_ETjS-bPhoFOrLmFmWExTVL7GgNAy41SlufyemBwedPLV1Y_ugSjVL8klwvtDaDSJ5_AZI0Boau778E_JDXCW6sqV4W3FOyNY1CLu1R2h6Gx1flJZBRMpW0OfmdyxDq4L4A1HY6y2SEqhcRqj_IlJ4qIkdg5uqSmBuHtQzNiNBDm917D2FOXv6T"
    )
    
    # Getting the user details.
    access_token = response["AuthenticationResult"]["AccessToken"]
    
    response = client.get_user(AccessToken=access_token)
    
    
    return response

def lambda_handler(event, context):
    # TODO implement
    return authenticate()