from datetime import datetime, timedelta
import urllib3
import json
import requests
import demistomock as demisto
from CommonServerPython import *

urllib3.disable_warnings()
IDN_OAUTH_EXT = '/oauth/token'
IDN_SEARCH_PREFIX = '/v3/search/events'


class Client(BaseClient):
    def sailpoint_get_events(self, since_datetime, until_datetime):
        since_datetime_formatted = since_datetime.replace('-', '\\-').replace('.', '\\.').replace(':', '\\:')
        until_datetime_formatted = until_datetime.replace('-', '\\-').replace('.', '\\.').replace(':', '\\:')
        query_params = {
            "count": True,
            "offset": 0,
            "limit": 10000
        }
        # Search criteria - retrieve all audit events since the checkpoint time, sorted by created date
        search_payload = {
            "queryType": "SAILPOINT",
            "query": {
                "query": f"created:>{since_datetime_formatted} AND created:<{until_datetime_formatted}"
            },
            "queryResultFilter": {},
            "sort": ["created"],
            "searchAfter": []
        }

        response = self._http_request('POST', IDN_SEARCH_PREFIX, params=query_params, json_data=search_payload, resp_type="response")

        if response.status_code == 200:
            return response.json()
        else:
            return []


    def send_to_xsiam(self, events):
        if len(events) > 1:
            json_str = json.dumps(events)[1:-1].replace('}, {', '}\n{')
            response = self._http_request('POST', '/logs/v1/event', data=json_str)
            return response
        elif len(events) == 1:
            json_str = json.dumps(events)[1:-1]
            response = self._http_request('POST', '/logs/v1/event', data=json_str)
            return response


def timestamp_format(timestamp):
    time_string = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    return time_string


def get_last_run(events: list[dict]) -> dict:
    """
    Get the info from the last run, it returns the time to query from
    """
    last_timestamp = events[-1]['created']
    if "." in last_timestamp:
        last_time = datetime.strptime(last_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        last_time = datetime.strptime(last_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    next_fetch_time = last_time + timedelta(seconds=1)
    return {'since_datetime': timestamp_format(next_fetch_time)}


def get_headers(base_url: str, client_id: str, client_secret: str, grant_type: str):
    if base_url is None or client_id is None or client_secret is None:
        return None

    if grant_type is None:
        grant_type = 'client_credentials'

    params = {
        'grant_type': grant_type,
        'client_id': client_id,
        'client_secret': client_secret
    }
    oauth_response = requests.request("POST", url=f'{base_url}{IDN_OAUTH_EXT}', params=params)
    if oauth_response is not None and 200 <= oauth_response.status_code < 300:
        return {
            'Authorization': 'Bearer %s' % oauth_response.json().get('access_token', None),
            'Content-Type': 'application/json'
        }
    elif oauth_response.json().get('error_description'):
        raise DemistoException(oauth_response.json().get('error_description'))
    else:
        raise DemistoException('Unable to fetch headers from IdentityNow!')


def fetch_events(client, last_run):
    since_datetime = last_run.get('since_datetime', None)
    if not since_datetime:
        since_datetime = timestamp_format(datetime.now()-timedelta(minutes=60))
    util_datetime = timestamp_format(datetime.now())
    events = client.sailpoint_get_events(since_datetime, util_datetime)
    return events


def main():
    params = demisto.params()
    args = demisto.args()
    should_push_events = argToBoolean(args.get('should_push_events', 'false'))

    # IdentityNow API Base URL (https://org.api.identitynow.com)
    sailpoint_url = params.get('identitynow_url')

    # OAuth 2.0 Credentials
    client_id = params.get('client_id')
    client_secret = params.get('client_secret')
    grant_type = 'client_credentials'

    sailpoint_headers = get_headers(sailpoint_url, client_id, client_secret, grant_type)
    sailpoint_client = Client(base_url=sailpoint_url, headers=sailpoint_headers)

    # Prepare XSIAM connection
    xsiam_url = params.get('xsiam_url')
    xsiam_api_key = params.get('xsiam_api_key')
    xsiam_headers = {
        'Content-Type': 'text/plain',
        'Authorization': f'{xsiam_api_key}'
        }
    xsiam_client = Client(base_url=xsiam_url, headers=xsiam_headers)

    command = demisto.command()
    try:
        if command == 'test-module':
            sailpoint_client.sailpoint_get_events(timestamp_format(datetime.now()-timedelta(hours=1)),timestamp_format(datetime.now()))
            return_results('ok')

        elif command == 'fetch-events':
            last_run = demisto.getLastRun()
            if not last_run:
                last_run = {'since_datetime': timestamp_format(datetime.now()-timedelta(hours=1))}
            events = fetch_events(sailpoint_client, last_run)
            if events:
                xsiam_client.send_to_xsiam(events)
                demisto.setLastRun(get_last_run(events))

        elif command == 'sailpoint-get-events':
            events = sailpoint_client.sailpoint_get_events(args.get('since_datetime'),args.get('until_datetime'))
            command_results = CommandResults(
                readable_output=tableToMarkdown('Sailpoint Identity Now Events', events, headerTransform=pascalToSpace),
                outputs_prefix='Sailpoint.Events',
                outputs_key_field='@timestamp',
                outputs=events,
                raw_response=events,
            )
            return_results(command_results)
            if should_push_events:
                xsiam_client.send_to_xsiam(events)


    except Exception as e:
        return_error(str(e))


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
