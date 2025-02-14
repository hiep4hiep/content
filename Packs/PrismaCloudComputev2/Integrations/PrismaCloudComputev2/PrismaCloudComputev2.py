import demistomock as demisto
from CommonServerPython import *  # noqa # pylint: disable=unused-wildcard-import
from CommonServerUserPython import *  # noqa

import urllib3
from typing import Dict, Any
from datetime import datetime, timedelta

# Disable insecure warnings
urllib3.disable_warnings()


''' CONSTANTS '''

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'  # ISO8601 format with UTC, default in XSOAR


class Client(BaseClient):

    def __init__(self, base_url: str, key_id: str, key_secret: str, proxy: bool, verify: bool):
        self.base_url = base_url
        self.headers = {'Content-Type': 'application/json'}
        self.key_id = key_id
        self.key_secret = key_secret
        super().__init__(base_url=base_url, verify=verify, headers=self.headers, proxy=proxy)
    
    
    def authenticate(self):
        url_suffix = "/authenticate"
        data = {
            "username": self.key_id,
            "password": self.key_secret
        }
        token = self._http_request('POST', url_suffix=url_suffix, json_data=data)
        return token.get('token')

    def get_alerts(self, start_time: str, end_time: str, alert_source: str, type: str = None) -> Dict[str, str]:
        url_suffix = f"/audits/firewall/app/{alert_source}"
        params = {
            "from": start_time,
            "to": end_time
        }
        if type:
            params["type"] = type
        token = self.authenticate()
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        response = self._http_request('GET', url_suffix=url_suffix, params=params, headers=headers)
        return response


def test_module(client: Client) -> str:
    message: str = ''
    try:
        test_token = client.authenticate()
        if test_token:
            message = 'ok'
        else:
            return "Cannot authenticate"

    except DemistoException as e:
        if 'Forbidden' in str(e) or 'Authorization' in str(e):  # TODO: make sure you capture authentication errors
            message = 'Authorization Error: make sure API Key is correctly set'
        else:
            raise e
    return message


def fetch_incidents(client: Client, fetch_days: int, alert_source: str = 'host') -> CommandResults:
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    day_ago = datetime.now() - timedelta(days=fetch_days)
    start_time = day_ago.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    last_run = demisto.getLastRun()
    if last_run and 'start_time' in last_run:
        start_time = last_run.get('start_time')
    
    alerts = client.get_alerts(start_time=start_time, end_time=current_time, alert_source=alert_source)
    # Create incidents
    incidents = []
    if alerts:
        for alert in alerts:
            incident = {
                "name": alert["msg"],
                "occurred": alert["time"],
                "rawJSON": json.dumps(alert)
            }
            incidents.append(incident)
    
    if incidents:
        demisto.setLastRun({
            'start_time': incidents[-1]['occurred']
        })
    
    demisto.incidents(incidents)


def main() -> None:

    access_key = demisto.params().get('access_key')
    key_id = access_key.get('identifier')
    key_secret = access_key.get('password')
    base_url = urljoin(demisto.params()['url'], '/api/v1')
    verify_certificate = not demisto.params().get('insecure', False)
    proxy = demisto.params().get('proxy', False)
    fetch_days = int(demisto.params().get('fetch_days'))
    alert_source = demisto.params().get('alert_source')
    demisto.debug(f'Command being called is {demisto.command()}')
    if 1==1:
        client = Client(
            key_id=key_id,
            key_secret=key_secret,
            base_url=base_url,
            verify=verify_certificate,
            proxy=proxy)

        if demisto.command() == 'test-module':
            result = test_module(client)
            return_results(result)

        elif demisto.command() == 'fetch-incidents':
            fetch_incidents(client, fetch_days, alert_source)

    #except Exception as e:
    #    return_error(f'Failed to execute {demisto.command()} command.\nError:\n{str(e)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
