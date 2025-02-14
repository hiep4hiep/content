import demistomock as demisto
from CommonServerPython import *
import io
import math
import json
import pytz
from datetime import datetime, date
import urllib3.util
from AWSApiModule import *  # noqa: E402
from http import HTTPStatus

# Disable insecure warnings
urllib3.disable_warnings()

SERVICE = 's3'
TIME_ZONE = pytz.timezone('UTC')

class Client(BaseClient):
    def send_to_xsiam(self, events):
        response = self._http_request('POST', '/logs/v1/event', data=events)
        return response
    
"""HELPER FUNCTIONS"""


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


class DatetimeEncoder(json.JSONEncoder):
    # pylint: disable=method-hidden
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
    

def timestamp_format(original_datetime):
    time_string = original_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
    return time_string


def get_last_run(last_run) -> dict:
    """
    Get the info from the last run, it returns the time to query from
    """
    last_time = datetime.strptime(last_run.get('since_datetime'), "%Y-%m-%dT%H:%M:%SZ")
    next_fetch_time = last_time + timedelta(seconds=1)
    return next_fetch_time


def download_file(bucket, key, client):
    tmp_file_name = key.split("/")[-1]
    client.download_file(bucket, key, tmp_file_name)
    with open(tmp_file_name, 'r') as f:
        return f.read()


def fetch_events(args: Dict[str, Any], aws_client: AWSClient, fetch_timestamp):
    client = aws_client.aws_session(service=SERVICE, region=args.get('region'), role_arn=args.get('roleArn'),
                                    role_session_name=args.get('roleSessionName'),
                                    role_session_duration=args.get('roleSessionDuration'), )
    
    data = ""
    last_key = demisto.getLastRun().get('last_key', None)
    processed_timestamp = None
    
    kwargs = {'Bucket': args.get('bucket')}
    if args.get('delimiter') is not None:
        kwargs.update({'Delimiter': args.get('delimiter')})
    if args.get('prefix') is not None:
        kwargs.update({'Prefix': args.get('prefix')})

    raw_data = client.list_objects(**kwargs).get('Contents')

    if raw_data:
        for key_data in raw_data:
            if last_key:
                if key_data.get('LastModified') > TIME_ZONE.localize(fetch_timestamp) and key_data.get('Key') != last_key:
                    data += download_file(args.get('bucket'), key_data.get('Key'), client)
                    processed_timestamp = key_data.get('LastModified')
                    processed_key = key_data.get('Key')
                    break
            else:
                if key_data.get('LastModified') > TIME_ZONE.localize(fetch_timestamp):
                    data += download_file(args.get('bucket'), key_data.get('Key'), client)
                    processed_timestamp = key_data.get('LastModified')
                    processed_key = key_data.get('Key')
                    break
        
    # Store the max timestamp in the processed timestamp list as LastRun
    if processed_timestamp and processed_key:
        demisto.setLastRun(
            {
                'since_datetime': timestamp_format(processed_timestamp),
                'last_key': processed_key
            }
        )
    demisto.info(data)
    return data


def main():  # pragma: no cover
    params = demisto.params()

    # Prepare XSIAM Connection
    aws_default_region = params.get('defaultRegion')
    aws_role_arn = params.get('roleArn')
    aws_role_session_name = params.get('roleSessionName')
    aws_role_session_duration = params.get('sessionDuration')
    aws_role_policy = None
    aws_access_key_id = params.get('credentials', {}).get('identifier') or params.get('access_key')
    aws_secret_access_key = params.get('credentials', {}).get('password') or params.get('secret_key')
    verify_certificate = not params.get('insecure', True)
    timeout = params.get('timeout')
    retries = params.get('retries') or 5
    sts_endpoint_url = params.get('sts_endpoint_url') or None
    endpoint_url = params.get('endpoint_url') or None
    s3_args = {
                "bucket": params.get('bucket'),
                "prefix": params.get('prefix')     
            }
    first_fetch = int(params.get('first_fetch'))

    # Prepare XSIAM connection
    xsiam_url = params.get('xsiam_url')
    xsiam_api_key = params.get('xsiam_api_key')

    xsiam_headers = {
        'Content-Type': 'text/plain',
        'Authorization': f'{xsiam_api_key}'
        }
    xsiam_client = Client(base_url=xsiam_url, headers=xsiam_headers, verify=verify_certificate)

    if 1==1:
        command = demisto.command()
        validate_params(aws_default_region, aws_role_arn, aws_role_session_name, aws_access_key_id,
                        aws_secret_access_key)

        aws_client = AWSClient(aws_default_region, aws_role_arn, aws_role_session_name, aws_role_session_duration,
                               aws_role_policy, aws_access_key_id, aws_secret_access_key, verify_certificate, timeout,
                               retries, sts_endpoint_url=sts_endpoint_url, endpoint_url=endpoint_url)

        args = demisto.args()

        demisto.info(f'Command being called is {demisto.command()}')
        if command == 'test-module':
            fetch_timestamp = datetime.now() - timedelta(hours=first_fetch)
            events = fetch_events(s3_args, aws_client, fetch_timestamp)
            demisto.results('ok')
        
        elif command == 'fetch-events':
            # Get last run timestamp from cache
            last_run = demisto.getLastRun()
            if last_run:
                fetch_timestamp = get_last_run(last_run)
            else:
                fetch_timestamp = datetime.now() - timedelta(days=first_fetch)
            events = fetch_events(s3_args, aws_client, fetch_timestamp)
            if events:
                xsiam_client.send_to_xsiam(events)

        else:
            raise NotImplementedError(f'{command} command is not implemented.')

    #except Exception as e:
    #    return_error(f'Failed to execute {command} command.\nError:\n{str(e)}')


if __name__ in ('__builtin__', 'builtins', '__main__'):
    main()
