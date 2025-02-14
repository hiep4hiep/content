from datetime import datetime, timedelta
import urllib3
import json
import requests

urllib3.disable_warnings()
# API Endpoint for Authentication and Search
OAUTH_PREFIX = '/something/oauth/token'
SEARCH_PREFIX = '/something/search'

# Use BaseClient class for main API function like search/get events because it wraps HTTP request with granular error handing
class Client(BaseClient):
    def solution_get_events(self, environment, since_datetime):
        '''
        This method call the API endpoint to get events
        '''
        query_params = {
        }

        response = self._http_request('GET', SEARCH_PREFIX, params=query_params, resp_type="response")
        if response.status_code == 200:
            raw_data = response.json()
            if raw_data.get('items'):
                return raw_data.get('items')
        else:
            return []


    def send_to_xsiam(self, events: list[dict]):
        '''
        This method send the processes event to XSIAM HTTP Collector
        '''
        if len(events) > 1:
            json_str = json.dumps(events)[1:-1].replace('}, {', '}\n{')
            response = self._http_request('POST', '/logs/v1/event', data=json_str)
            return response
        elif len(events) == 1:
            json_str = json.dumps(events)[1:-1]
            response = self._http_request('POST', '/logs/v1/event', data=json_str)
            return response


def timestamp_format(timestamp):
    time_string = timestamp.strftime("%Y-%m-%dT%H:%M:%S")
    return time_string



def get_last_run(events: list[dict]) -> dict:
    """
    Get the info from the last run, it returns the time to query from
    """
    last_timestamp = events[-1]['entry_dttm']
    # response timestring format 16JUN2023:05:03:14.325000
    last_time = datetime.strptime(last_timestamp, "%d%b%Y:%H:%M:%S.%f")
    next_fetch_time = last_time + timedelta(seconds=1)
    return {'since_datetime': timestamp_format(next_fetch_time)}


def get_headers(base_url: str, client_id: str, client_secret: str, grant_type: str, username: str, password: str):
    if base_url is None or client_id is None or client_secret is None:
        return None

    if grant_type is None:
        grant_type = 'password'

    payload = f'grant_type={grant_type}&username={username}&password={password}&client_id={client_id}&client_secret='

    request_headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
    oauth_response = requests.request("POST", url=f'{base_url}{OAUTH_PREFIX}', headers=request_headers, data=payload)

    if oauth_response is not None and 200 <= oauth_response.status_code < 300:
        return {
            'Authorization': 'Bearer %s' % oauth_response.json().get('access_token', None),
            'Content-Type': 'application/json'
        }
    elif oauth_response.json().get('error_description'):
        raise DemistoException(oauth_response.json().get('error_description'))
    else:
        raise DemistoException('Unable to fetch headers from Zencos!')


def fetch_events(client, last_run, environment):
    since_datetime = last_run.get('since_datetime', None)
    if not since_datetime:
        since_datetime = timestamp_format(datetime.now()-timedelta(minutes=60))
    events = client.zencos_get_events(environment, since_datetime)
    return events


def main():
    params = demisto.params()
    args = demisto.args()
    should_push_events = argToBoolean(args.get('should_push_events', 'false'))

    # Zencos API Base URL)
    zencos_url = params.get('zencos_url')

    # OAuth 2.0 Credentials
    client_id = params.get('client_id')
    client_secret = params.get('client_secret')
    grant_type = 'password'
    username = params.get('username')
    password = params.get('password')

    zencos_header = get_headers(zencos_url, client_id, client_secret, grant_type, username, password)
    zencos_client = Client(base_url=zencos_url, headers=zencos_header)
    environment = params.get('environment')

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
            events = zencos_client.zencos_get_events(environment,timestamp_format(datetime.now()-timedelta(hours=1)))
            return_results('ok')

        elif command == 'fetch-events':
            last_run = demisto.getLastRun()
            if not last_run:
                last_run = {'since_datetime': timestamp_format(datetime.now()-timedelta(hours=1))}
            events = fetch_events(zencos_client, last_run, environment)
            if events:
                xsiam_client.send_to_xsiam(events)
                demisto.setLastRun(get_last_run(events))

        elif command == 'zencos-get-events':
            events = zencos_client.zencos_get_events(environment,args.get('since_datetime'))
            command_results = CommandResults(
                readable_output=tableToMarkdown('Zencos Events', events, headerTransform=pascalToSpace),
                outputs_prefix='Zencos.Events',
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
