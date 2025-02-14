import urllib3
from collections.abc import Generator
import tempfile
import requests
import csv

from abc import ABC
from typing import Any, Callable, Optional




from enum import Enum
from pydantic import BaseConfig, BaseModel, AnyUrl, validator, Field
from requests.auth import HTTPBasicAuth


class Method(str, Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    HEAD = 'HEAD'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


def load_json(v: Any) -> dict:
    if not isinstance(v, (dict, str)):
        raise ValueError('headers are not dict or a valid json')
    if isinstance(v, str):
        try:
            v = json.loads(v)
            if not isinstance(v, dict):
                raise ValueError('headers are not from dict type')
        except json.decoder.JSONDecodeError as exc:
            raise ValueError('headers are not valid Json object') from exc
    if isinstance(v, dict):
        return v


class IntegrationHTTPRequest(BaseModel):
    method: Method
    url: AnyUrl
    verify: bool = True
    headers: dict = dict()  # type: ignore[type-arg]
    auth: Optional[HTTPBasicAuth]
    data: Any = None
    params: dict = dict()  # type: ignore[type-arg]

    class Config(BaseConfig):
        arbitrary_types_allowed = True

    _normalize_headers = validator('headers', pre=True, allow_reuse=True)(
        load_json
    )


class Credentials(BaseModel):
    identifier: Optional[str]
    password: str


def set_authorization(request: IntegrationHTTPRequest, auth_credendtials):
    """Automatic authorization.
    Supports {Authorization: Bearer __token__}
    or Basic Auth.
    """
    creds = Credentials.parse_obj(auth_credendtials)
    if creds.password and creds.identifier:
        request.auth = HTTPBasicAuth(creds.identifier, creds.password)
    auth = {'Authorization': f'Bearer {creds.password}'}
    if request.headers:
        request.headers |= auth  # type: ignore[assignment, operator]
    else:
        request.headers = auth  # type: ignore[assignment]


class IntegrationOptions(BaseModel):
    """Add here any option you need to add to the logic"""

    proxy: Optional[bool] = False
    limit: Optional[int] = Field(None, ge=1)


class IntegrationEventsClient(ABC):
    def __init__(
        self,
        request: IntegrationHTTPRequest,
        options: IntegrationOptions,
        session=requests.Session(),
    ):
        self.request = request
        self.options = options
        self.session = session
        self._set_proxy()
        self._skip_cert_verification()

    @abstractmethod
    def set_request_filter(self, after: Any):
        """TODO: set the next request's filter.
        Example:
        """
        self.request.headers['after'] = after

    def __del__(self):
        try:
            self.session.close()
        except AttributeError as err:
            demisto.debug(
                f'ignore exceptions raised due to session not used by the client. {err=}'
            )

    def call(self, request: IntegrationHTTPRequest) -> requests.Response:
        try:
            response = self.session.request(**request.dict())
            response.raise_for_status()
            return response
        except Exception as exc:
            msg = f'something went wrong with the http call {exc}'
            demisto.debug(msg)
            raise DemistoException(msg) from exc

    def _skip_cert_verification(
        self, skip_cert_verification: Callable = skip_cert_verification
    ):
        if not self.request.verify:
            skip_cert_verification()

    def _set_proxy(self):
        if self.options.proxy:
            ensure_proxy_has_http_prefix()
        else:
            skip_proxy()


class IntegrationGetEvents(ABC):
    def __init__(
        self, client: IntegrationEventsClient, options: IntegrationOptions
    ) -> None:
        self.client = client
        self.options = options

    def run(self):
        stored = []
        for logs in self._iter_events():
            stored.extend(logs)
            if self.options.limit:
                demisto.debug(
                    f'{self.options.limit=} reached. \
                    slicing from {len(logs)=}. \
                    limit must be presented ONLY in commands and not in fetch-events.'
                )
                if len(stored) >= self.options.limit:
                    return stored[: self.options.limit]
        return stored

    def call(self) -> requests.Response:
        return self.client.call(self.client.request)

    @staticmethod
    @abstractmethod
    def get_last_run(events: list) -> dict:
        """Logic to get the last run from the events
        Example:
        """
        return {'after': events[-1]['created']}

    @abstractmethod
    def _iter_events(self):
        """Create iterators with Yield"""
        pass

register_module_line('SiemApiModule', 'end', __line__(), wrapper=1)
### END GENERATED CODE ###

urllib3.disable_warnings()
VENDOR = "salesforce"
PRODUCT = 'event-audit'

class Client(BaseClient):
    def send_to_xsiam(self, events):
        if len(events) > 1:
            json_str = ""
            for event in events:
                json_str += json.dumps(event) + "\n"
            response = self._http_request('POST', '/logs/v1/event', data=json_str)
            return response
        elif len(events) == 1:
            json_str = json.dumps(events[0])
            return_error(len(events))
            response = self._http_request('POST', '/logs/v1/event', data=json_str)
            return response


class SalesforceClient(IntegrationEventsClient):
    def set_request_filter(self, after: str):
        return


class SalesforceGetEvents(IntegrationGetEvents):
    """
    A class to handle the flow of the integration
    """

    def __init__(self, client: SalesforceClient, options: IntegrationOptions,
                files_limit: int, query: str, after: str, last_id: str) -> None:
        self.client: SalesforceClient = client
        self.instance_url: str = ''
        self.query: str = query
        self.files_limit: int = files_limit
        self.after: str = after
        self.last_id: str = last_id
        self.last_file: dict = {}

        super().__init__(client, options)

    def get_token(self):
        res = self.client.call(self.client.request).json()
        self.client.request.headers = {'Authorization': f"Bearer {res.get('access_token')}"}
        self.instance_url = res.get('instance_url')

    def pull_log_files(self):
        query = f'{self.query}+and+CreatedDate+>+{self.after} limit {self.files_limit}'

        demisto.info('Searching files last modified from {}'.format(self.after))

        url = f'{self.instance_url}/services/data/v58.0/query?q={query}'

        self.client.request.url = url
        self.client.request.method = Method.GET
        res = self.client.call(self.client.request).json()
        return self.get_files_from_res(res)

    def get_files_from_res(self, query_res):
        files = query_res['records']
        done_status = query_res['done']

        while done_status is False:
            query = query_res['nextRecordsUrl']
            try:
                self.client.request.url = f'{self.instance_url}{query}'
                self.client.request.method = Method.GET
                query_res = self.client.call(self.client.request).json()
            except Exception as err:
                demisto.error(f'File list getting failed: {err}')

            done_status = query_res['done']
            for file in query_res['records']:
                files.append(file)

        demisto.info('Total number of files is {}.'.format(len(files)))

        # sort all files by date
        files.sort(key=lambda k: dateparser.parse(k.get('LogDate')))

        if not self.last_id:
            return files

        # filter only the files we already fetched to avoid duplicates
        last_id_found = False
        new_files = []
        for file in files:
            if last_id_found:
                new_files.append(file)

            if file['Id'] == self.last_id:
                last_id_found = True

        return new_files

    def get_file_raw_lines(self, file_url, file_in_tmp_path):
        url = f'{self.instance_url}{file_url}'
        try:
            r = requests.get(url, stream=True, headers=self.client.request.headers)
            if r.status_code == 401:
                self.get_token()
                r = requests.get(url, stream=True, headers=self.client.request.headers)

            with open(file_in_tmp_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            if r.status_code == 200:
                demisto.info(f'File successfully downloaded from url {url}')
            else:
                demisto.info(f'File downloading failed. {r.status_code} {r.text} {file_url}')
        except Exception as err:
            demisto.error(f'File downloading failed. {err} {file_url}')

    @staticmethod
    def gen_chunks_to_object(file_in_tmp_path, chunksize=100):
        field_names = [name.lower() for name in list(csv.reader(open(file_in_tmp_path)))[0]]
        field_names = [x if x != 'type' else 'type_' for x in field_names]
        reader = csv.DictReader(open(file_in_tmp_path), fieldnames=field_names)
        chunk: list = []
        next(reader)
        for index, line in enumerate(reader):
            if index % chunksize == 0 and index > 0:
                yield chunk
                del chunk[:]
            chunk.append(line)
        yield chunk

    def _iter_events(self) -> Generator:
        self.get_token()
        temp_dir = tempfile.TemporaryDirectory()
        log_files = self.pull_log_files()

        # save the last file to get the recent file id and the date we fetched
        # to filter the only the new files in the next run
        if log_files:
            self.last_file = log_files[-1]

        for line in log_files:
            events_list = []
            local_filename = line["LogFile"].replace('/', '_').replace(':', '_')
            file_in_tmp_path = "{}/{}".format(temp_dir.name, local_filename)
            self.get_file_raw_lines(line["LogFile"], file_in_tmp_path)

            for chunk in self.gen_chunks_to_object(file_in_tmp_path=file_in_tmp_path, chunksize=2000):
                events_list.extend(chunk)

            yield events_list

    def get_last_run_details(self) -> dict:
        """
        Get the log time and the file id to prevent duplications in the next run
        """
        last_file = self.last_file

        if last_file:
            last_timestamp = last_file['LogDate']
            timestamp = dateparser.parse(last_timestamp)
            if timestamp is None:
                raise TypeError('Failed to parse LogDate')
            return {'after': timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    'last_id': last_file['Id']}

        return {}

    @staticmethod
    def get_last_run(events: list) -> dict:
        return {}


def get_timestamp_format(value):
    timestamp: Optional[datetime]
    if isinstance(value, int):
        value = str(value)
    if not isinstance(value, datetime):
        timestamp = dateparser.parse(value)
    if timestamp is None:
        raise TypeError(f'after is not a valid time {value}')
    return timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    # Args is always stronger. Get last run even stronger
    demisto_params = demisto.params() | demisto.args() | demisto.getLastRun()

    demisto_params['client_id'] = demisto_params['client_id']['password']
    demisto_params['client_secret'] = demisto_params['client_secret']['password']

    files_limit = int(demisto_params.get('files_limit'))
    should_push_events = argToBoolean(demisto_params.get('should_push_events', 'false'))
    # Prepare XSIAM connection
    xsiam_url = demisto_params.get('xsiam_url')
    xsiam_api_key = demisto_params.get('xsiam_api_key')
    xsiam_headers = {
        'Content-Type': 'text/plain',
        'Authorization': f'{xsiam_api_key}'
        }
    xsiam_client = Client(base_url=xsiam_url, headers=xsiam_headers)

    demisto_params['method'] = Method.POST

    request = IntegrationHTTPRequest(**demisto_params)

    # add the params to the url in order to make the request without decoding the params
    url = urljoin(demisto_params.get("url"), 'services/oauth2/token')
    request.url = f'{url}?grant_type=client_credentials&' \
                  f'client_id={demisto_params.get("client_id")}&' \
                  f'client_secret={demisto_params.get("client_secret")}&'

    options = IntegrationOptions.parse_obj(demisto_params)
    client = SalesforceClient(request, options)

    after = get_timestamp_format(demisto_params.get('after'))

    get_events = SalesforceGetEvents(client, options, files_limit, demisto_params.get('query'),
                                    after, demisto_params.get('last_id'))

    command = demisto.command()
    if 1==1:
        if command == 'test-module':
            get_events.files_limit = 1
            events = get_events.run()
            return_results('ok')
        elif command in ('salesforce-get-events', 'fetch-events'):
            events = get_events.run()

            if command == 'fetch-events':
                xsiam_client.send_to_xsiam(events)
                #send_events_to_xsiam(events, vendor=VENDOR, product=PRODUCT)
                demisto.setLastRun(get_events.get_last_run_details())

            elif command == 'salesforce-get-events':
                command_results = CommandResults(
                    readable_output=tableToMarkdown('salesforce audit Logs', events, headerTransform=pascalToSpace),
                    raw_response=events,
                )
                return_results(command_results)
                if should_push_events:
                    xsiam_client.send_to_xsiam(events)

    #except Exception as e:
    #    return_error(str(e))


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
