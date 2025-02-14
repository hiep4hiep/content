from datetime import datetime, timedelta
import json
import requests
from requests.auth import HTTPBasicAuth
import calendar
import base64

def call(username,password):
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    print(encoded_credentials)
    """
    payload = 'grant_type=client_credentials'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}'
    }
    result = requests.request("POST", 'https://auth-m2m.megaport.com/oauth2/token', headers=headers, data=payload)

    if result.status_code == 200:
        token = result.json()['access_token']
        print(token)
        return {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
        
    else:
        print(result.text)
    """

call('3m4cdrq2h7qo138si1qj2ogc54','a74d66tfv85am6duhbns8q6m6rtp465nnjdhe0gc5nd6dltprd9')