from datetime import datetime, timedelta
import urllib3
import csv
import base64
import demistomock as demisto
import requests

urllib3.disable_warnings()


class Client(BaseClient):
    def qualys_vmdr_get_events(self, since_datetime=None, until_datetime=None):
        params = {
            "action": "list"
        }
        if since_datetime:
            params["since_datetime"] = since_datetime
        if until_datetime:
            params["until_datetime"] = until_datetime

        response = self._http_request('GET', 'api/2.0/fo/activity_log/', params=params, resp_type='text', timeout=60)
        trimmed_response = response.replace('----BEGIN_RESPONSE_BODY_CSV\n','').replace('----END_RESPONSE_BODY_CSV\n','')
        events = csv_to_dict(trimmed_response)
        if events:
            return events
        else:
            return []


    def send_to_xsiam(self, events):
        json_str = json.dumps(events)[1:-1].replace('}, {', '}\n{')
        response = self._http_request('POST', '/logs/v1/event', data=json_str)
        return response



def csv_to_dict(raw_data):
    with open('tempdata.csv', 'w') as csv_file:
        csv_data = csv_file.write(raw_data)

    with open('tempdata.csv', 'r') as csv_file:
        csv_data = csv.DictReader(csv_file)
        return list(csv_data)


def timestamp_format(original_datetime):
    time_string = original_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
    return time_string


def get_last_run(events: list[dict]) -> dict:
    """
    Get the info from the last run, it returns the time to query from
    """
    last_timestamp = events[0]['Date']
    last_time = datetime.strptime(last_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    next_fetch_time = last_time + timedelta(seconds=1)
    return {'since_datetime': timestamp_format(next_fetch_time)}


def fetch_events(client, last_run):
    since_datetime = last_run.get('since_datetime', None)
    if not since_datetime:
        since_datetime = timestamp_format(datetime.now()-timedelta(hours=12))
    events = client.qualys_vmdr_get_events(since_datetime)
    return events


def main():
    params = demisto.params()
    args = demisto.args()
    should_push_events = argToBoolean(args.get('should_push_events', 'false'))

    # Prepare Qualys connection
    qualys_url = params.get('qualys_url')
    username = params['qualys_authentication']['identifier']
    password = params['qualys_authentication']['password']
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    qualys_headers = {
        'X-Requested-With': 'xsiam',
        'Authorization': f'Basic {encoded_credentials}'
    }
    qualys_client = Client(base_url=qualys_url, headers=qualys_headers)

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
            events = qualys_client.qualys_vmdr_get_events(timestamp_format(datetime.now()-timedelta(hours=12)))
            return_results('ok')

        elif command == 'fetch-events':
            last_run = demisto.getLastRun()
            if not last_run:
                last_run = {'since_datetime': timestamp_format(datetime.now()-timedelta(hours=12))}
            events = fetch_events(qualys_client, last_run)
            if events:
                xsiam_client.send_to_xsiam(events)
                demisto.setLastRun(get_last_run(events))


        elif command == 'qualys-vmdr-get-events':
            events = qualys_client.qualys_vmdr_get_events(args.get('since_datetime'),args.get('until_datetime'))
            command_results = CommandResults(
                readable_output=tableToMarkdown('Qualys VMDR Logs', events, headerTransform=pascalToSpace),
                outputs_prefix='Qualys.Logs',
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