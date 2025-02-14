import random
import string
from typing import Dict

import dateparser
import chardet
import sys
import traceback
import json
import os
import hashlib
from io import StringIO
import logging
import warnings
import email
from requests.exceptions import ConnectionError

from multiprocessing import Process
import exchangelib
from exchangelib.errors import (
    ErrorItemNotFound,
    ResponseMessageError,
    RateLimitError,
    ErrorInvalidIdMalformed,
    ErrorFolderNotFound,
    ErrorMailboxStoreUnavailable,
    ErrorMailboxMoveInProgress,
    ErrorNameResolutionNoResults,
    MalformedResponseError,
)
from exchangelib.items import Item, Message, Contact
from exchangelib.services.common import EWSService, EWSAccountService
from exchangelib.util import create_element, add_xml_child, MNS, TNS
from exchangelib import (
    IMPERSONATION,
    Account,
    EWSDateTime,
    EWSTimeZone,
    Configuration,
    FileAttachment,
    Version,
    Folder,
    HTMLBody,
    Body,
    ItemAttachment,
    OAUTH2,
    OAuth2AuthorizationCodeCredentials,
    Identity,
    ExtendedProperty
)
from oauthlib.oauth2 import OAuth2Token
from exchangelib.version import EXCHANGE_O365
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter

#from msal import authority
#from Base.Scripts.CommonServerPython.CommonServerPython import CommandResults, get_integration_context, handle_proxy, return_results, tableToMarkdown
#from Base.Scripts.CommonServerPython.CommonServerPython import set_integration_context
#
#
#

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

# Ignore warnings print to stdout
warnings.filterwarnings("ignore")
''' CONSTANTS '''

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'  # ISO8601 format with UTC, default in XSOAR

''' HELPER FUNCTIONS '''

# TODO: ADD HERE ANY HELPER FUNCTION YOU MIGHT NEED (if any)

''' COMMAND FUNCTIONS '''
def set_noproxy():
    proxies = handle_proxy() # Get system proxies setting

    os.environ['NO_PROXY'] = os.environ['no_proxy'] = '127.0.0.1,localhost,*.c0.dbs.com,*.sgp.dbs.com,*.uat.dbs.com,sts1.dbsbank.asia,sts.dbs.com,c0.dbs.com,sgp.dbs.com'
    os.environ['HTTP_PROXY'] = os.environ['http_proxy'] = proxies.get('http', None)
    os.environ['HTTPS_PROXY'] = os.environ['https_proxy'] = proxies.get('https', None)

    print("System proxies settings: \
    \n- http: " + os.environ.get('HTTP_PROXY') + \
    "\n- https: " + os.environ.get('HTTPS_PROXY') + \
    "\n- no proxy: " + os.environ.get('NO_PROXY'))

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

def get_tokens(config: dict, is_secure: bool):
    ''' MICROSOFT MSAL CLASS '''
    app = msal.ClientApplication(
        client_id=config["client_id"],
        authority=config["authority"],
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

def get_tokens_device_flow(config: dict, is_secure: bool):

    # Create a preferably long-lived app instance which maintains a token cache.
    app = msal.PublicClientApplication(
        config["client_id"],
        authority=config["authority"],
        verify=is_secure
        )

    result = None
    accounts = app.get_accounts()
    if accounts:
        logging.info("Account(s) exists in cache, probably with token too. Let's try.")
        print("Pick the account you want to use to proceed:")
        for a in accounts:
            print(a["username"])
        chosen = accounts[0]
        result = app.acquire_token_silent(config["scope"], account=chosen)

    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")

        flow = app.initiate_device_flow(scopes=config["scope"])
        if "user_code" not in flow:
            raise ValueError(
                "Fail to create device flow. Err: %s" % json.dumps(flow, indent=4))
        context = {"flow": flow}
        set_integration_context(context)
        return(flow["message"])

def acquire_token(config: dict, is_secure: bool):
    app = msal.PublicClientApplication(
        client_id=config["client_id"],
        authority=config["authority"],
        verify=is_secure
        )
    context = get_integration_context()
    flow = context["flow"]
    
    result = app.acquire_token_by_device_flow(flow)  # By default it will block
    tokens = CommandResults(
        outputs=result,
        outputs_prefix="MSAL.Tokens",
        readable_output=tableToMarkdown("Your MSAL Tokens", result)
    )
    return(tokens)
    #return(result)    


def get_tokens_alternative(config: dict, is_secure: bool):
    url = config["authority"] + "/oauth2/v2.0/token"
    scope = config["scope"][0]
    client_id = config["client_id"]
    username = config["username"]
    password = config["password"]

    payload=f'grant_type=password&scope={scope}&client_id={client_id}&username={username}&password={password}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False, allow_redirects=True)
    result = response.json()

    tokens = CommandResults(
        outputs=result,
        outputs_prefix="MSAL.Tokens",
        readable_output=tableToMarkdown("Your MSAL Tokens", result)
    )
    return(tokens)

def get_accesstoken_from_refreshtoken(config: dict, is_secure: bool):
    refresh_token = demisto.args().get('refresh_token')
    url = config["authority"] + "/oauth2/v2.0/token"
    scope = config["scope"][0]
    client_id = config["client_id"]
    redirect_url = config["redirect_url"]

    payload=f'grant_type=refresh_token&client_id={client_id}&redirect_uri={redirect_url}&scope={scope}&refresh_token={refresh_token}'
    
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'), verify=False, allow_redirects=True)
    result = response.json()
    print(result)

    tokens = CommandResults(
        outputs=result,
        outputs_prefix="MSAL.NewTokens",
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
    redirect_url = demisto.params().get('redirect_url')
    scope = []
    scope.append(api_permission)
    config = {
        "authority": authority,
        "client_id": client_id,
        "username": username,
        "password": password,
        "scope": scope,
        "redirect_url": redirect_url
    }
    
    verify_certificate = not demisto.params().get('insecure', False)
    proxy = demisto.params().get('proxy', False)
    proxies = handle_proxy()
    set_noproxy()
    # Initiate PCA App
    

    demisto.debug(f'Command being called is {demisto.command()}')
    try:
        if demisto.command() == 'test-module':
            # This is the call made when pressing the integration Test button.
            result = test_module(client)
            return_results(result)


        elif demisto.command() == 'msal-get-tokens':
            return_results(get_tokens(config=config,is_secure=verify_certificate))

        elif demisto.command() == 'msal-get-tokens-alt':
            return_results(get_tokens_alternative(config=config,is_secure=verify_certificate))

        elif demisto.command() == 'msal-get-tokens-pkce':
            return_results(get_tokens_device_flow(config=config,is_secure=verify_certificate))

        elif demisto.command() == 'msal-acquire-tokens-pkce':
            return_results(acquire_token(config=config,is_secure=verify_certificate))

        elif demisto.command() == 'msal-get-accesstoken-from-refresh-token':
            return_results(get_accesstoken_from_refreshtoken(config=config,is_secure=verify_certificate))


    # Log exceptions and return errors
    except Exception as e:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute {demisto.command()} command.\nError:\n{str(e)}')


''' ENTRY POINT '''

if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
