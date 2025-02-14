import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401


from CommonServerUserPython import *  # noqa

import urllib3
from typing import Dict, Any
from azure.identity import ClientSecretCredential
import requests
from datetime import datetime
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
# Disable insecure warnings
urllib3.disable_warnings()


def test_module(access_token) -> str:
    query_timestamp = datetime.now() - timedelta(hours=1)
    query_time = query_timestamp.strftime(DATE_FORMAT)
    message: str = ''
    try:
        url = f"https://graph.microsoft.com/v1.0/security/incidents?$filter=createdDateTime gt {query_time}"
        # Define headers with authorization
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code in (200,201):
            message = 'ok'
        else:
            message = response.text
    except DemistoException as e:
        if 'Forbidden' in str(e) or 'Authorization' in str(e):  # TODO: make sure you capture authentication errors
            message = 'Authorization Error: make sure API Key is correctly set'
        else:
            raise e
    return message


# Function to fetch incidents with filters
def fetch_incidents(access_token, fetch_ago):
    try:
        last_run = demisto.getLastRun()
        if last_run and 'query_time' in last_run:
            query_time = last_run.get('query_time')
            demisto.debug("## Last alert timestamp is " + last_run.get('query_time'))
        else:
            query_timestamp = datetime.now() - timedelta(days=int(fetch_ago))
            query_time = query_timestamp.strftime(DATE_FORMAT)
            demisto.debug("## First run timestamp is " + query_time)
        
        incidents = []
        filter_query = f"createdDateTime gt {query_time}"
        url = f"https://graph.microsoft.com/v1.0/security/incidents?$filter={filter_query}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        result = response.json().get('value')
        if result:
            for incident in result:
                incidents.append(
                    {
                        'name': incident.get('displayName'),    
                        'occurred': incident.get('createdDateTime'),
                        'rawJSON': json.dumps(incident)
                    }
                )
            demisto.setLastRun({
                'query_time': result[-1]['createdDateTime']
                })
        return incidents
    except Exception as e:
        return_error("Error fetching incidents:", e)



''' MAIN FUNCTION '''


def main() -> None:
    """main function, parses params and runs command functions

    :return:
    :rtype:
    """
    params = demisto.params()
    # Authentication credentials
    tenant_id = params.get('tenant_id')
    client_id = params.get('client_id')
    client_secret = params.get('credentials').get('password')
    # Integration params
    fetch_ago = params.get('fetch_ago')

    # Scopes needed for accessing incidents
    scopes = ['https://graph.microsoft.com/.default']
    # Initialize the authentication provider
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )
    # Initialize the GraphServiceClient
    access_token = credential.get_token("https://graph.microsoft.com/.default").token

    demisto.debug(f'Command being called is {demisto.command()}')
    try:
        if demisto.command() == 'test-module':
            # This is the call made when pressing the integration Test button.
            result = test_module(access_token)
            return_results(result)

        elif demisto.command() == 'fetch-incidents':
            incidents = fetch_incidents(access_token, fetch_ago)
            demisto.incidents(incidents)

    # Log exceptions and return errors
    except Exception as e:
        return_error(f'Failed to execute {demisto.command()} command.\nError:\n{str(e)}')


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
