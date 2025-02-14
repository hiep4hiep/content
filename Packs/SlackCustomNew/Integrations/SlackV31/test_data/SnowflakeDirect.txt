import snowflake.connector
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from datetime import date, timedelta, datetime
from datetime import time as dttime
from decimal import Decimal
import argparse

parser = argparse.ArgumentParser(description="SnowFlake query script")
parser.add_argument("--username", dest="username", type=str, required=False, default='SPLUNK_IDM_USER')
parser.add_argument("--password", dest="password", type=str, required=False)
parser.add_argument("--warehouse", dest="warehouse", type=str, required=False, default='compute_wh')
parser.add_argument("--database", dest="database", type=str, required=False, default='snowflake')
parser.add_argument("--schema", dest="schema", type=str, required=False, default='ACCOUNT_USAGE')
parser.add_argument("--role", dest="role", type=str, required=False, default='snowflake_monitoring')
args = parser.parse_args()

'''GLOBAL VARS'''
USER = args.username
PASSWORD = args.password
ACCOUNT = 'resolutionlife-minerva-prod.privatelink'
AUTHENTICATOR = ''
REGION = ''
WAREHOUSE = args.warehouse
DATABASE = args.database
SCHEMA = args.schema
ROLE = args.role
INSECURE = False
# How much time before the first fetch to retrieve incidents
IS_FETCH = False
FETCH_TIME = '1 hours'
FETCH_QUERY = "SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY WHERE QUERY_START_TIME > '2023-07-31 15:26:20.827' ORDER BY QUERY_START_TIME ASC"
DATETIME_COLUMN = 'QUERY_START_TIME'
INCIDENT_NAME_COLUMN = ''
MAX_ROWS = 1

TYPE_CODE_TO_DATATYPE = {
    0: 'number/int',
    1: 'real',
    2: 'varchar/string',
    3: 'date',
    4: 'timestamp',
    5: 'variant',
    6: 'timestamp_ltz',
    7: 'timestamp_tz',
    8: 'timestamp_tz',
    9: 'object',
    10: 'array',
    11: 'binary',
    12: 'time',
    13: 'boolean'
}
DT_NEEDS_CHECKING = {'date', 'timestamp', 'timestamp_ltz', 'timestamp_tz', 'time'}


'''HELPER FUNCTIONS'''
def set_provided(params, key, val1, val2=None):
    """
    If value is provided, set it in the dict
    """
    if val1:
        params[key] = val1
    elif val2:
        params[key] = val2


def get_connection_params(args):
    """
    Construct and return the connection parameters

    parameter: (dict) args
        The command arguments of the command function calling this helper function

    returns:
        Snowflake connection params
    """
    params: dict = {}
    set_provided(params, 'user', USER)
    set_provided(params, 'password', PASSWORD)
    set_provided(params, 'account', ACCOUNT)
    set_provided(params, 'authenticator', AUTHENTICATOR)
    set_provided(params, 'region', REGION)
    set_provided(params, 'insecure_mode', INSECURE)
    set_provided(params, 'warehouse', args.get('warehouse'), WAREHOUSE)
    set_provided(params, 'database', args.get('database'), DATABASE)
    set_provided(params, 'schema', args.get('schema'), SCHEMA)
    set_provided(params, 'role', args.get('role'), ROLE)
    
    return params


'''MAIN FUNCTIONS / API CALLS'''


def fetch_incidents():
    """
    Fetch events from this integration and return them as Demisto incidents

    returns:
        Demisto incidents
    """
   
    args = {'rows': MAX_ROWS, 'query': FETCH_QUERY}
    data = snowflake_query(args)
    print(data)


def snowflake_query(args):
    params = get_connection_params(args)
    query = args.get('query')
    limit = args.get('limit', '100')
    try:
        limit = int(limit)
    except ValueError:
        raise ValueError('The value for limit must be an integer.')
    if limit > MAX_ROWS:
        limit = MAX_ROWS
    
    with snowflake.connector.connect(**params) as connection:
        with connection.cursor(snowflake.connector.DictCursor) as cur:
            cur.execute(query)
            results = cur.fetchmany(limit)
            if results:
                return cur.description, results
            else:
                return [], []
    """
    conn = snowflake.connector.connect(**params)
    cur = conn.cursor(snowflake.connector.DictCursor).execute(query)
    results = cur.fetchmany(limit)
    if results:
        cur.close()
        conn.close()
        return cur.description, results
    else:
        cur.close()
        conn.close()
        return [], []
    """

try:
    fetch_incidents()
except Exception as e:
    print(str(e))