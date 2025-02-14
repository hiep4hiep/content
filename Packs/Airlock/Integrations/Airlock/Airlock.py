from datetime import datetime, timedelta
import urllib3
import json
import requests
from CommonServerPython import *
import demistomock as demisto

urllib3.disable_warnings()
AIRLOCK_OAUTH_EXT = '/accounts/api/v2/oauth2/token'
AIRLOCK_SRV_PREFIX = '/v1/logging/svractivities'
AIRLOCK_EXEC_PREFIX = '/v1/logging/exechistories'

class Client(BaseClient):
    def airlock_get_server_events(self, checkpoint):
        search_payload = {}
        if checkpoint:
            search_payload["checkpoint"] =  checkpoint
        
        response = self._http_request('POST', AIRLOCK_SRV_PREFIX, json_data=search_payload, resp_type="response")

        if response.status_code == 200:
            return response.json().get('response').get('svractivities')
        else:
            return []
        
    def airlock_get_exec_events(self, checkpoint):
        search_payload = {}
        if checkpoint:
            search_payload["checkpoint"] =  checkpoint
        
        response = self._http_request('POST', AIRLOCK_EXEC_PREFIX, json_data=search_payload, resp_type="response")

        if response.status_code == 200:
            return response.json().get('response').get('exechistories')
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
    last_checkpoint = events[-1]['checkpoint']
    return last_checkpoint


def fetch_events(client: Client, event_type, checkpoint):
    if event_type == 'server':
        events = client.airlock_get_server_events(checkpoint)
    elif event_type == 'exec':
        events = client.airlock_get_exec_events(checkpoint)
    return events


def main():
    params = demisto.params()
    args = demisto.args()
    airlock_url = params.get('airlock_url')

    # API Credentials
    airlock_api_key = params.get('api_key')
    airlock_headers = {
        'X-ApiKey': airlock_api_key,
        'Content-Type': 'application/json'
    }
    airlock_client = Client(base_url=airlock_url, headers=airlock_headers)

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
            events = airlock_client.airlock_get_server_events(checkpoint=None)
            json_str = ""
            for event in events:
                json_str += json.dumps(event) + "\n"
            print(json_str)
            return_results('ok')

        elif command == 'fetch-events':
            next_run = {}
            last_run = demisto.getLastRun()
            if not last_run:
                server_checkpoint = exec_checkpoint = None
            else:
                server_checkpoint = last_run.get('server_checkpoint')
                exec_checkpoint = last_run.get('exec_checkpoint')
            server_events = fetch_events(airlock_client, 'server', server_checkpoint)
            exec_events = fetch_events(airlock_client, 'exec', exec_checkpoint)
            if server_events:
                xsiam_client.send_to_xsiam(server_events)
                next_run['server_checkpoint'] = get_last_run(server_events)
            if exec_events:
                xsiam_client.send_to_xsiam(exec_events)
                next_run['exec_checkpoint'] = get_last_run(exec_events)
            demisto.updateModuleHealth('')
            demisto.setLastRun(next_run)

        elif command == 'airlock-get-events':
            events = airlock_client.airlock_get_events(args.get('since_datetime'))
            command_results = CommandResults(
                readable_output=tableToMarkdown('Mulesoft Events', events, headerTransform=pascalToSpace),
                outputs_prefix='Mulesoft.Events',
                outputs_key_field='@timestamp',
                outputs=events,
                raw_response=events,
            )
            return_results(command_results)


    except Exception as e:
        return_error(str(e))


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
