
#from msal import authority
#from Base.Scripts.CommonServerPython.CommonServerPython import CommandResults, get_integration_context, handle_proxy, return_results, tableToMarkdown
#from Base.Scripts.CommonServerPython.CommonServerPython import set_integration_context
#import demistomock as demisto
#from CommonServerPython import *  # noqa # pylint: disable=unused-wildcard-import
#from CommonServerUserPython import *  # noqa

import requests
import traceback
from typing import Dict, Any
import sys
import json
import logging
import msal
import os

# Disable insecure warnings
requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

''' CONSTANTS '''

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'  # ISO8601 format with UTC, default in XSOAR

''' HELPER FUNCTIONS '''

# TODO: ADD HERE ANY HELPER FUNCTION YOU MIGHT NEED (if any)

''' COMMAND FUNCTIONS '''
def set_noproxy():
    os.environ['NO_PROXY'] = os.environ['no_proxy'] = '127.0.0.1,localhost,*.c0.dbs.com,*.sgp.dbs.com,*.uat.dbs.com,sts1.dbsbank.asia,sts.dbs.com'

def test_module() -> str:
    message: str = ''
    try:
        message = 'ok'
    except DemistoException as e:
        if 'Forbidden' in str(e) or 'Authorization' in str(e):  # TODO: make sure you capture authentication errors
            message = 'Authorization Error: make sure API Key is correctly set'
        else:
            raise e
    return message

def get_tokens(config: dict, proxies: dict, is_secure: bool):
    ''' MICROSOFT MSAL CLASS '''
    set_noproxy()
    app = msal.ClientApplication(
        client_id=config["client_id"],
        authority=config["authority"],
        proxies=proxies,
        verify=is_secure
        )
    result = None

    # Firstly, check the cache to see if this end user has signed in before
    accounts = app.get_accounts(username=config["username"])
    if accounts:
        logging.info("Account(s) exists in cache, probably with token too. Let's try.")
        result = app.acquire_token_silent(config["scope"], account=accounts[0])

    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
        # See this page for constraints of Username Password Flow.
        # https://github.com/AzureAD/microsoft-authentication-library-for-python/wiki/Username-Password-Authentication
        result = app.acquire_token_by_username_password(
            config["username"], config["password"], scopes=config["scope"])
    tokens = CommandResults(
        outputs=result,
        outputs_prefix="MSAL.Tokens",
        readable_output=tableToMarkdown("Your MSAL Tokens", result)
    )
    return(tokens)

def get_tokens_alternative(config: dict, proxies: dict, is_secure: bool):
    set_noproxy()
    url = config["authority"] + "/oauth2/v2.0/token"
    scope = config["scope"][0]
    client_id = config["client_id"]
    username = config["username"]
    password = config["password"]

    payload=f'grant_type=password&scope={scope}&client_id={client_id}&username={username}&password={password}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies, verify=False, allow_redirects=True)
    result = response.json()

    tokens = CommandResults(
        outputs=result,
        outputs_prefix="MSAL.Tokens",
        readable_output=tableToMarkdown("Your MSAL Tokens", result)
    )
    return(tokens)
    

''' MAIN FUNCTION '''


def main() -> None:
    """main function, parses params and runs command functions

    :return:
    :rtype:
    """
    # MSAL Authentication params
    tenant_id = demisto.params().get('tenant_id')
    authority = "https://login.microsoftonline.com/" + tenant_id
    client_id = demisto.params().get('client_id')
    username = demisto.params().get('credentials').get('identifier')
    password = demisto.params().get('credentials').get('password')
    api_permission = demisto.params().get('api_permission','User.Read')
    scope = []
    scope.append(api_permission)
    config = {
        "authority": authority,
        "client_id": client_id,
        "username": username,
        "password": password,
        "scope": scope
    }

    verify_certificate = not demisto.params().get('insecure', False)
    proxy = demisto.params().get('proxy', False)
    proxies = handle_proxy()

    demisto.debug(f'Command being called is {demisto.command()}')
    try:
        if demisto.command() == 'test-module':
            # This is the call made when pressing the integration Test button.
            result = test_module(client)
            return_results(result)

        
        elif demisto.command() == 'msal-get-tokens':
            print("Using these proxy settings: ", proxies)
            return_results(get_tokens(config=config,proxies=proxies,is_secure=verify_certificate))

        elif demisto.command() == 'msal-get-tokens-alt':
            print("Using these proxy settings: ", proxies)
            return_results(get_tokens_alternative(config=config,proxies=proxies,is_secure=verify_certificate))


    # Log exceptions and return errors
    except Exception as e:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute {demisto.command()} command.\nError:\n{str(e)}')
    


''' ENTRY POINT '''

if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
