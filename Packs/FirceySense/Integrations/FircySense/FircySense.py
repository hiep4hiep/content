register_module_line('FircySense', 'start', __line__())

from CommonServerPython import *
import demistomock as demisto

import urllib3
import traceback
from typing import Dict, Any

# Disable insecure warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BRAND_NAME = "Fircey"  # matches context output path for faster caching


class Client(BaseClient):
    def __init__(self, base_url: str, verify_certificate: bool, proxy: bool, reliability: str, headers: dict):
        """
        Client to use in the IPinfo integration. Uses BaseClient
        """
        super().__init__(base_url=base_url, proxy=proxy, verify=verify_certificate, headers=headers)
        self.reliability = reliability

    def fircey_ip(self, ip: str) -> Dict[str, Any]:
        return self.http_request(ip)

    def http_request(self, ip: str) -> Dict[str, Any]:
        return self._http_request(method='GET',
                                  url_suffix=f'/v1/ip/full?ip={ip}',
                                  timeout=20)


def test_module(client: Client) -> str:
    """Tests IPinfo by sending a query on 8.8.8.8"""
    client.fircey_ip('8.8.8.8')
    return 'ok'  # on any failure, an exception is raised


def fircey_ip_command(client: Client, ip: str) -> List[List[CommandResults]]:
    response = client.fircey_ip(ip)
    ip_result = parse_results(ip, response, client.reliability)
    return ip_result


def parse_results(ip: str, raw_result: Dict[str, Any], reliability: str) -> List[CommandResults]:
    command_results: List[CommandResults] = []
    if raw_result:
        entry_context = raw_result[0]
        if entry_context.get('owner'):
            asn = entry_context.get('owner').get('asn', None)
            organization_name = entry_context.get('owner').get('org-name', None)
            geo_country = entry_context.get('owner').get('country-name', None)
            description = entry_context.get('target-locations', None)
            tags = entry_context.get('target-tags').get('client-type',[])
        outputs_key_field = 'ip'  # marks the ip address

        if DBotScoreReliability.is_valid_type(reliability):
            dbot_reliability = DBotScoreReliability.get_dbot_score_reliability_from_str(reliability)
        else:
            raise Exception("Please provide a valid value for the Source Reliability parameter.")

        indicator = Common.IP(
            ip=ip,
            dbot_score=Common.DBotScore(indicator=ip,
                                        indicator_type=DBotScoreType.IP,
                                        reliability=dbot_reliability,
                                        integration_name=BRAND_NAME,
                                        score=Common.DBotScore.NONE),
            asn=asn,
            geo_country=geo_country,
            tags=','.join(tags),
            organization_name=organization_name,
            description=description
            )
    else:
        if DBotScoreReliability.is_valid_type(reliability):
            dbot_reliability = DBotScoreReliability.get_dbot_score_reliability_from_str(reliability)
        else:
            raise Exception("Please provide a valid value for the Source Reliability parameter.")

        indicator = Common.IP(
            ip=ip,
            dbot_score=Common.DBotScore(indicator=ip,
                                        indicator_type=DBotScoreType.IP,
                                        reliability=dbot_reliability,
                                        integration_name=BRAND_NAME,
                                        score=Common.DBotScore.NONE)
            )

    # do not change the order of the calls for CommandResults due to an issue where the ip command would not
    # present all of the information returned from the API.
    command_results.append(
        CommandResults(readable_output="No result found from Fircy",
                       indicator=indicator)
    )

    return command_results


def main() -> None:
    """main function, parses params and runs command functions"""

    params = demisto.params()
    args = demisto.args()
    command = demisto.command()

    proxy = params.get('proxy') or False
    api_key = demisto.get(params, 'credentials.password') or ''
    insecure = params.get('insecure') or False
    base_url = params.get('base_url') or "https://sense.api.fircy.com"
    reliability = params.get('integrationReliability')
    headers = {
        "x-api-key":api_key
    }
    demisto.debug(f'Command being called is {command}')

    try:
        client = Client(headers=headers,
                        verify_certificate=not insecure,
                        proxy=proxy,
                        base_url=base_url,
                        reliability=reliability)

        if command == 'test-module':
            return_results(test_module(client))

        elif command == 'ip':
            ip_command = fircey_ip_command(client, **args)
            return_results(ip_command)
        else:
            raise NotImplementedError(f"command {command} is not supported")

    # Log exceptions and return errors
    except Exception as e:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute {command} command.'
                     f'\nError:\n{str(e)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()

register_module_line('FircySense', 'end', __line__())
