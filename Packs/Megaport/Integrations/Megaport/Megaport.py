from datetime import datetime, timedelta
import urllib3
import json
import requests
from requests.auth import HTTPBasicAuth
import calendar
import base64
from CommonServerPython import *
import demistomock as demisto

urllib3.disable_warnings()
MEGAPORT_OAUTH_EXT = 'https://auth-m2m.megaport.com/oauth2/token'
MEGAPORT_SEARCH_PREFIX = '/v2/activity'


class Client(BaseClient):
    def megaport_get_events(self, page=None):
        params = dict(
            #companyIdOrUid = "b724f03e-0ba1-46d9-8e83-ab006ab6669b",
            companyIdOrUid = 44237,
            page = page
        )
        response = self._http_request('GET', MEGAPORT_SEARCH_PREFIX, params=params, resp_type="response")

        return response.json().get('data') if response.json().get('data') else []


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
    time_string = calendar.timegm(timestamp.timetuple())
    return int(time_string)



def get_headers(username: str, password: str):
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    payload = 'grant_type=client_credentials'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}'
        #'Authorization': 'Basic M200Y2RycTJoN3FvMTM4c2kxcWoyb2djNTQ6YTc0ZDY2dGZ2ODVhbTZkdWhibnM4cTZtNnJ0cDQ2NW5uamRoZTBnYzVuZDZkbHRwcmQ5'
    }
    result = requests.request("POST", 'https://auth-m2m.megaport.com/oauth2/token', headers=headers, data=payload)
    
    if result.status_code == 200:
        token = result.json()['access_token']
        return {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        } 
    else:
        DemistoException(result.text)



def fetch_events(client: Client, previous_latest_eventdate):
    max_page_count = 10
    page = 0
    masterLogList = []
    while page < max_page_count:
        logList = client.megaport_get_events(page=page)
        if len(logList) == 0:
            break
        for item in logList:
            if item['eventDate'] <= previous_latest_eventdate:
                page = max_page_count
                break
            else:
                # item['sourcetype'] = 'amp:megaport:json'
                masterLogList.append(item)
        page += 1

    # Dummy data generated when no new logs available from the API source. This is prevent alerts by Splunk about silence on the line.            
    if len(masterLogList) == 0:
        ts=int(time.time()) * 1000
        dummy_data = dict(
            personName = 'dummy', 
            personId = 11111, 
            description = 'dummy',
            name = 'dummy',
            ipAddress = '0.0.0.0',
            eventDate = ts,
            systemActivity = False,
            activityId = None,
            index = None,
            megaportalNews = None,
            megasphereNews = None,
            style = {},
            data = {},
            # sourcetype = 'amp:megaport:json'
        )
        masterLogList = [{**dummy_data}]
        current_latest_eventdate = previous_latest_eventdate
    else:
        current_latest_eventdate = masterLogList[0]['eventDate']

    demisto.setLastRun({"latest_eventdate": current_latest_eventdate})

    return masterLogList


def main():
    params = demisto.params()
    args = demisto.args()
    should_push_events = argToBoolean(args.get('should_push_events', 'false'))

    megaport_url = params.get('megaport_url','https://api.megaport.com')
    username = params.get('credentials').get('identifier')
    password = params.get('credentials').get('password')
    
    megaport_headers = get_headers(username, password)
    megaport_client = Client(base_url=megaport_url, headers=megaport_headers)

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
            previous_latest_eventdate = timestamp_format(datetime.now()-timedelta(days=10))
            events = fetch_events(megaport_client, previous_latest_eventdate)
            if events:
                xsiam_client.send_to_xsiam(events)
            return_results('ok')

        elif command == 'fetch-events':
            last_run = demisto.getLastRun()
            if not last_run:
                last_run = {'latest_eventdate': timestamp_format(datetime.now()-timedelta(days=30))}
            previous_latest_eventdate = last_run.get('latest_eventdate')
            events = fetch_events(megaport_client, previous_latest_eventdate)
            if events:
                xsiam_client.send_to_xsiam(events)
                

        elif command == 'megaport-get-events':
            events = megaport_client.megaport_get_events(args.get('page'))
            command_results = CommandResults(
                readable_output=tableToMarkdown('Megaport Events', events, headerTransform=pascalToSpace),
                outputs_prefix='Megaport.Events',
                outputs=events,
                raw_response=events,
            )
            return_results(command_results)
            if should_push_events:
                xsiam_client.send_to_xsiam(events)


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
