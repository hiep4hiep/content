import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401


import urllib3
from typing import Dict, Any
import clickhouse_connect
from datetime import datetime
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

# Disable insecure warnings
urllib3.disable_warnings()


def run_select_query(client, query_str: str, parameters):
    """Returns a simple python dict with the information provided
    in the input (dummy).

    :type query_str: ``str``
    :param query_str: SQL SELECT query to run against ClickHouse DB

    :return: dict as {"dummy": dummy}
    """
    result = client.query(query_str, parameters=parameters)
    data = result.result_rows
    return data



def test_module(client, alert_table, alert_timestamp_field, fetch_ago) -> str:
    """Tests API connectivity and authentication'
    Returning 'ok' indicates that the integration works like it is supposed to.
    Connection to the service is successful.
    Raises exceptions if something goes wrong.
    """

    message: str = ''
    try:
        params = demisto.params()
        query_time = datetime.now() - timedelta(days=int(fetch_ago))
        parameters = {'timestamp': query_time}

        query = f'SELECT * FROM {alert_table} \
            WHERE {alert_timestamp_field} > %(timestamp)s \
            ORDER BY {alert_timestamp_field} \
            LIMIT 1'
        data = client.query(query,parameters=parameters)
        message = 'ok'
    except DemistoException as e:
        if 'Forbidden' in str(e) or 'Authorization' in str(e):  # TODO: make sure you capture authentication errors
            message = 'Authorization Error: make sure API Key is correctly set'
        else:
            raise e
    return message


def fetch_incidents(client, alert_table, alert_name_field, alert_timestamp_field, fetch_ago, max_alert):
    query_time = datetime.now() - timedelta(hours=int(fetch_ago))
    last_run = demisto.getLastRun()
    if last_run and 'query_time' in last_run:
        query_time = datetime.strptime(last_run.get('query_time'),DATE_FORMAT) + timedelta(seconds=1)
        demisto.debug("## Last alert timestamp is " + last_run.get('query_time'))
        demisto.debug("## Next alert run is " + query_time.strftime(DATE_FORMAT))
    parameters = {'timestamp': query_time}

    query = f'SELECT * FROM {alert_table} \
            WHERE {alert_timestamp_field} > %(timestamp)s \
            ORDER BY {alert_timestamp_field}'
    if max_alert > 0:
        query = query + f' LIMIT {str(max_alert)}'

     # Get Alert table timestamp fields
    #describe_query_timestamp_fields = f"SELECT column_name  FROM information_schema.columns WHERE table_catalog=(SELECT currentDatabase()) AND table_name ='{alert_table}' AND column_type like 'DateTime%'"
    #data = client.command(describe_query_timestamp_fields)
    timestamp_field_list = ["timestamp","timestamp_load","detected_time"]
     # Get Alert table fields
    describe_query = f"DESCRIBE TABLE {alert_table}"
    data = client.command(describe_query)
    table_fields_list = re.findall("([^$\s]+)\$\w", '$'.join(data))

    # Call the Client function and get the raw response
    result = run_select_query(client, query, parameters)
    if result:
        incidents = []
        alert_timestamp_index = 0
        alert_name_index = 0
        for alert in result:
            alert_data = {}
            # Map alert data to field in JSON
            for i, value in enumerate(table_fields_list):
                if value in timestamp_field_list:
                    alert_data[value] = alert[i].strftime(DATE_FORMAT)
                    if value == alert_timestamp_field:
                        alert_timestamp_index = i
                else:
                    alert_data[value] = str(alert[i])
                    if value == alert_name_field:
                        alert_name_index = i
            incidents.append(
                {
                    'name': alert[alert_name_index],
                    'occurred': alert[alert_timestamp_index].strftime(DATE_FORMAT),
                    #'occurred': datetime.now().strftime(DATE_FORMAT),
                    'rawJSON': json.dumps(alert_data)
                }
            )

        demisto.setLastRun({
            'query_time': result[-1][0].strftime(DATE_FORMAT)
        })

        return incidents


''' MAIN FUNCTION '''


def main() -> None:
    params = demisto.params()
    verify_certificate = not demisto.params().get('insecure', False)
    alert_table = params.get('alert_table')
    fetch_ago = params.get('fetch_ago')
    max_alert = int(params.get('query_limit',0))

    connection_params = {
        "interface": "https",
        "host": params.get('host'),
        "port": params.get('port'),
        "username": params.get('credentials').get('identifier'),
        "password": params.get('credentials').get('password'),
        "database": params.get('database'),
        "compress": params.get('compress'),
        "query_limit": params.get('query_limit'),
        "query_retries": params.get('query_retries'),
        "connect_timeout": params.get('connect_timeout'),
        "send_receive_timeout": params.get('send_receive_timeout'),
        "verify": verify_certificate
    }

    demisto.debug(f'Command being called is {demisto.command()}')
    # Update
    try:
        client = clickhouse_connect.get_client(**connection_params)

        if demisto.command() == 'test-module':
            result = test_module(client, params.get('database') + "." + alert_table,params.get('alert_timestamp_field','timestamp'), fetch_ago)
            return_results(result)

        elif demisto.command() == 'fetch-incidents':
            incidents = fetch_incidents(client, params.get('database') + "." + alert_table,params.get('alert_name_field'),params.get('alert_timestamp_field','timestamp'), fetch_ago, max_alert)
            demisto.incidents(incidents)

    # Log exceptions and return errors
    except Exception as e:
        return_error(f'Failed to execute {demisto.command()} command.\nError:\n{str(e)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()