from datetime import datetime, timedelta
import urllib3
import json
import requests
from CommonServerPython import *
import demistomock as demisto

urllib3.disable_warnings()
MULESOFT_OAUTH_EXT = '/accounts/api/v2/oauth2/token'
MULESOFT_SEARCH_PREFIX = '/audit/v2/organizations/125196b8-b30f-45fb-8c42-8ec36309a844/query'


class Client(BaseClient):
    def mulesoft_get_events(self, since_datetime):
        search_payload = {
            "startDate": since_datetime
        }
        response = self._http_request('POST', MULESOFT_SEARCH_PREFIX, json_data=search_payload, resp_type="response")

        if response.status_code == 200:
            return response.json().get('data')
        else:
            return []


    def send_to_xsiam(self, events):
        if len(events) > 1:
            json_str = ""
            for event in events:
                json_str += json.dumps(event) + "\n"
            response = self._http_request('POST', '/logs/v1/event', data=json_str)
            return response
        elif len(events) == 1:
            json_str = json.dumps(events[0])
            response = self._http_request('POST', '/logs/v1/event', data=json_str)
            return response


def timestamp_format(timestamp):
    time_string = timestamp.strftime("%Y-%m-%dT%H:%M:%S")
    return time_string


def get_last_run(events: list[dict]) -> dict:
    """
    Get the info from the last run, it returns the time to query from
    """
    last_timestamp = datetime.fromtimestamp(int(events[-1]['timestamp'])/1000)
    next_fetch_time = last_timestamp + timedelta(seconds=1)
    return {'since_datetime': timestamp_format(next_fetch_time)}


def get_headers(base_url: str, client_id: str, client_secret: str, grant_type: str):
    if base_url is None or client_id is None or client_secret is None:
        return None

    if grant_type is None:
        grant_type = 'client_credentials'

    payload = f'client_id={client_id}&client_secret={client_secret}&grant_type={grant_type}'

    request_headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    oauth_response = requests.request("POST", url=f'{base_url}{MULESOFT_OAUTH_EXT}', headers=request_headers, data=payload)
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
    events = client.mulesoft_get_events(since_datetime)
    return events


def main():
    params = demisto.params()
    args = demisto.args()
    should_push_events = argToBoolean(args.get('should_push_events', 'false'))

    mulesoft_url = params.get('mulesoft_url')

    # OAuth 2.0 Credentials
    client_id = params.get('client_id')
    client_secret = params.get('client_secret')
    grant_type = 'client_credentials'

    mulesoft_headers = get_headers(mulesoft_url, client_id, client_secret, grant_type)
    mulesoft_client = Client(base_url=mulesoft_url, headers=mulesoft_headers)

    # Prepare XSIAM connection
    xsiam_url = params.get('xsiam_url')
    xsiam_api_key = params.get('xsiam_api_key')
    xsiam_headers = {
        'Content-Type': 'text/plain',
        'Authorization': f'{xsiam_api_key}'
        }
    xsiam_client = Client(base_url=xsiam_url, headers=xsiam_headers)

    command = demisto.command()
    if 1==1:
        if command == 'test-module':
            events = mulesoft_client.mulesoft_get_events(timestamp_format(datetime.now()-timedelta(days=90)))
            json_str = ""
            for event in events:
                json_str += json.dumps(event) + "\n"
            print(json_str)
            return_results('ok')

        elif command == 'fetch-events':
            last_run = demisto.getLastRun()
            if not last_run:
                last_run = {'since_datetime': timestamp_format(datetime.now()-timedelta(days=90))}
            events = fetch_events(mulesoft_client, last_run)
            if events:
                xsiam_client.send_to_xsiam(events)
                demisto.setLastRun(get_last_run(events))

        elif command == 'mulesoft-get-events':
            events = mulesoft_client.mulesoft_get_events(args.get('since_datetime'))
            command_results = CommandResults(
                readable_output=tableToMarkdown('Mulesoft Events', events, headerTransform=pascalToSpace),
                outputs_prefix='Mulesoft.Events',
                outputs_key_field='@timestamp',
                outputs=events,
                raw_response=events,
            )
            return_results(command_results)
            if should_push_events:
                xsiam_client.send_to_xsiam(events)


    #except Exception as e:
    #    return_error(str(e))


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
