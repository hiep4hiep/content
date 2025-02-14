from datetime import datetime, timedelta
import urllib3
import requests
import calendar

import demistomock as demisto
from CommonServerPython import *

urllib3.disable_warnings()

OAUTH_URL = "https://apigw-apacsouth.central.arubanetworks.com/oauth2/token"

class Client(BaseClient):
    def aruba_central_get_platform_events(self, since_datetime=None):
        params = {
            "start_time": int(since_datetime),
            "limit": 100
        }
        response = self._http_request('GET', '/platform/auditlogs/v1/logs', params=params, resp_type='response', timeout=60)
        demisto.debug(response.text)
        return response.json().get('audit_logs') if response.json().get('audit_logs') else []

    def aruba_central_get_audit_events(self, since_datetime=None):
        params = {
            "start_time": int(since_datetime),
            "limit": 100
        }
        response = self._http_request('GET', '/auditlogs/v1/events', params=params, resp_type='response', timeout=60)
        demisto.debug(response.text)
        return response.json().get('events') if response.json().get('events') else []
    
    def aruba_central_get_alerts(self, since_datetime=None):
        params = {
            "from_timestamp": int(since_datetime),
            "limit": 100
        }
        response = self._http_request('GET', '/central/v1/notifications', params=params, resp_type='response', timeout=60)
        demisto.debug(response.text)
        return response.json().get('notifications') if response.json().get('notifications') else []
    

    def send_to_xsiam(self, events):
        json_str = json.dumps(events)[1:-1].replace('}, {', '}\n{')
        response = self._http_request('POST', '/logs/v1/event', data=json_str)
        return response


def timestamp_format(timestamp):
    time_string = calendar.timegm(timestamp.timetuple())
    return int(time_string)


def get_last_run(events: list[dict], event_type: str) -> dict:
    """
    Get the info from the last run, it returns the time to query from
    """
    demisto.debug("Event batch" + str(events))
    last_timestamp = events[0]['ts']
    next_fetch_time =  last_timestamp + 1
    if event_type == 'platform':
        return next_fetch_time
    elif event_type == 'audit':
        return next_fetch_time
    elif event_type == 'alert':
        last_timestamp = events[0]['timestamp']
        next_fetch_time =  last_timestamp + 1
        return next_fetch_time


def get_token(client_id: str, client_secret: str, token: str):
    if demisto.getIntegrationContext().get('access_token'):
        demisto.debug("EXIST")
        demisto.debug(demisto.getIntegrationContext())
        if timestamp_format(datetime.now()) < demisto.getIntegrationContext().get('token_expire'):
            return demisto.getIntegrationContext()

    if demisto.getIntegrationContext().get('refresh_token'):
        demisto.debug("EXIST REFRESH")
        refresh_token = demisto.getIntegrationContext().get('refresh_token')
    else:
        refresh_token = token
    demisto.debug("THISSSS: ", refresh_token)
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    result = requests.request("POST", OAUTH_URL, params=params)
    demisto.debug("GET REFRESH")
    demisto.debug(result.json())
    if result.status_code == 200:
        access_token = result.json()['access_token']
        return {
            "refresh_token": result.json()['refresh_token'],
            "access_token": access_token,
            "token_expire": timestamp_format(datetime.now()+timedelta(minutes=90))}
    else:
        raise Exception(result.text)


def fetch_events(client: Client, last_run, event_type):
    if event_type == 'platform':
        since_datetime = last_run.get('since_datetime_platform', None)
        if not since_datetime:
            since_datetime = timestamp_format(datetime.now()-timedelta(days=3))
            demisto.debug("No since_datetime_platform, set to " + str(since_datetime))
        events = client.aruba_central_get_platform_events(since_datetime)
    elif event_type == 'audit':
        since_datetime = last_run.get('since_datetime_audit', None)
        if not since_datetime:
            since_datetime = timestamp_format(datetime.now()-timedelta(days=3))
            demisto.debug("No since_datetime_platform, set to " + str(since_datetime))
        events = client.aruba_central_get_audit_events(since_datetime)
    elif event_type == 'alert':
        since_datetime = last_run.get('since_datetime_alert', None)
        if not since_datetime:
            since_datetime = timestamp_format(datetime.now()-timedelta(days=3))
            demisto.debug("No since_datetime_alert, set to " + str(since_datetime))
        events = client.aruba_central_get_alerts(since_datetime)

    return events



def main():
    params = demisto.params()

    # Prepare aruba connection
    aruba_url = params.get('aruba_url','https://app1-apigw.central.arubanetworks.com/')
    client_id = params['client_id']
    client_secret = params['client_secret']
    api_token = params['api_token']
    token = get_token(client_id, client_secret, api_token)
    aruba_headers = {
            'Authorization': 'Bearer ' + token.get('access_token'),
            'Content-Type': 'application/json'
        }

    aruba_client = Client(base_url=aruba_url, headers=aruba_headers)
    demisto.debug(aruba_headers)
    # Prepare XSIAM connection
    xsiam_url = params.get('xsiam_url')
    xsiam_api_key = params.get('xsiam_api_key')

    xsiam_headers = {
        'Content-Type': 'text/plain',
        'Authorization': f'{xsiam_api_key}'
        }

    xsiam_client = Client(base_url=xsiam_url, headers=xsiam_headers)

    command = demisto.command()
    if True:
        if command == 'test-module':
            fetch_events(aruba_client, {}, 'platform')
            return_results('ok')

        elif command == 'fetch-events':
            ctx = demisto.getIntegrationContext()
            demisto.debug("Current last run " + str(ctx))
            if not ctx.get('since_datetime_platform'):
                demisto.debug("Last run Platform is not available")
                # update context
                token['since_datetime_platform'] = timestamp_format(datetime.now()-timedelta(hours=12))
            if not ctx.get('since_datetime_audit'):
                demisto.debug("Last run Audit is not available")
                token['since_datetime_audit'] = timestamp_format(datetime.now()-timedelta(hours=12))
            if not ctx.get('since_datetime_alert'):
                demisto.debug("Last run Alert is not available")
                token['since_datetime_alert'] = timestamp_format(datetime.now()-timedelta(hours=12))
            
            demisto.setIntegrationContext(token)

            ctx = demisto.getIntegrationContext()
            demisto.debug(ctx)

            platform_events =fetch_events(aruba_client, ctx, 'platform')
            audit_events = fetch_events(aruba_client, ctx, 'audit')
            alert_events = fetch_events(aruba_client, ctx, 'alert')
            if platform_events:
                xsiam_client.send_to_xsiam(platform_events)
                token['since_datetime_platform'] = get_last_run(platform_events,'platform')
            if audit_events:
                xsiam_client.send_to_xsiam(audit_events)
                token['since_datetime_audit'] = get_last_run(audit_events,'audit')
            if alert_events:
                xsiam_client.send_to_xsiam(alert_events)
                token['since_datetime_alert'] = get_last_run(alert_events,'alert')

            xsiam_client.send_to_xsiam([token])
            demisto.updateModuleHealth('')


    #except Exception as e:
    #    return_error(str(e))


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()