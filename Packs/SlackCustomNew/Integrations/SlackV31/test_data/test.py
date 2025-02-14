from datetime import date, timedelta, datetime
from datetime import time as dttime

def convert_datetime_to_string(v):
    """
    Parses date, time, timedelta, or datetime object into string

    parameter: (datetime/date/time/timedelta) v
        The datetime/date/time/timedelta object to convert

    returns:
        Formatted string of the object
    """
    if isinstance(v, datetime):
        return v.strftime('%Y-%m-%d %H:%M:%S.%f').strip()
    elif isinstance(v, date):
        return v.strftime('%Y-%m-%d').strip()
    elif isinstance(v, dttime):
        return v.strftime('%H:%M:%S.%f').strip()
    elif isinstance(v, int):
        return datetime.fromtimestamp(v/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
    return v


data = [
    {
   "QUERY_ID":"01ae315c-0000-dd0c-0000-42811b5300ee",
   "QUERY_TEXT":"PUT 'file:///tmp/snowflake/stage/CURR_CONTRACT_E374SU/INSERT/20230809_131503_851_E374SU_1/stream_20230809_131503_8513.gz' '@~/CURR_CONTRACT_E374SU/INSERT/20230809_131503_851_E374SU_1' parallel=10 overwrite=true auto_compress=false SOURCE_COMPRESSION=gzip",
   "DATABASE_ID":17,
   "DATABASE_NAME":"MDW",
   "SCHEMA_ID":670,
   "SCHEMA_NAME":"MRVCONS_CURRENT",
   "QUERY_TYPE":"PUT_FILES",
   "SESSION_ID":73121943211186,
   "USER_NAME":"IICS_PRD_USER",
   "ROLE_NAME":"IICS_USER_PRD_ROLE",
   "WAREHOUSE_ID":7,
   "WAREHOUSE_NAME":"IICS_PRD_USER_XS_WH",
   "WAREHOUSE_SIZE":"None",
   "WAREHOUSE_TYPE":"STANDARD",
   "CLUSTER_NUMBER":"None",
   "QUERY_TAG":"",
   "EXECUTION_STATUS":"SUCCESS",
   "ERROR_CODE":"None",
   "ERROR_MESSAGE":"None",
   "START_TIME":datetime(2023,
   8,
   9,
   23,
   16,
   3,
   417000),
   "END_TIME":datetime(2023,
   8,
   9,
   23,
   16,
   3,
   449000),
   "TOTAL_ELAPSED_TIME":32,
   "BYTES_SCANNED":0,
   "PERCENTAGE_SCANNED_FROM_CACHE":0.0,
   "BYTES_WRITTEN":0,
   "BYTES_WRITTEN_TO_RESULT":0,
   "BYTES_READ_FROM_RESULT":0,
   "ROWS_PRODUCED":"None",
   "ROWS_INSERTED":0,
   "ROWS_UPDATED":0,
   "ROWS_DELETED":0,
   "ROWS_UNLOADED":0,
   "BYTES_DELETED":0,
   "PARTITIONS_SCANNED":0,
   "PARTITIONS_TOTAL":0,
   "BYTES_SPILLED_TO_LOCAL_STORAGE":0,
   "BYTES_SPILLED_TO_REMOTE_STORAGE":0,
   "BYTES_SENT_OVER_THE_NETWORK":0,
   "COMPILATION_TIME":31,
   "EXECUTION_TIME":1,
   "QUEUED_PROVISIONING_TIME":0,
   "QUEUED_REPAIR_TIME":0,
   "QUEUED_OVERLOAD_TIME":0,
   "TRANSACTION_BLOCKED_TIME":0,
   "OUTBOUND_DATA_TRANSFER_CLOUD":"None",
   "OUTBOUND_DATA_TRANSFER_REGION":"None",
   "OUTBOUND_DATA_TRANSFER_BYTES":0,
   "INBOUND_DATA_TRANSFER_CLOUD":"None",
   "INBOUND_DATA_TRANSFER_REGION":"None",
   "INBOUND_DATA_TRANSFER_BYTES":0,
   "LIST_EXTERNAL_FILES_TIME":0,
   "CREDITS_USED_CLOUD_SERVICES":5e-06,
   "RELEASE_VERSION":"7.27.1",
   "EXTERNAL_FUNCTION_TOTAL_INVOCATIONS":0,
   "EXTERNAL_FUNCTION_TOTAL_SENT_ROWS":0,
   "EXTERNAL_FUNCTION_TOTAL_RECEIVED_ROWS":0,
   "EXTERNAL_FUNCTION_TOTAL_SENT_BYTES":0,
   "EXTERNAL_FUNCTION_TOTAL_RECEIVED_BYTES":0,
   "QUERY_LOAD_PERCENT":"None",
   "IS_CLIENT_GENERATED_STATEMENT":False,
   "QUERY_ACCELERATION_BYTES_SCANNED":0,
   "QUERY_ACCELERATION_PARTITIONS_SCANNED":0,
   "QUERY_ACCELERATION_UPPER_LIMIT_SCALE_FACTOR":0,
   "TRANSACTION_ID":0,
   "CHILD_QUERIES_WAIT_TIME":0,
   "ROLE_TYPE":"ROLE"
}
]
formatted_data = []
if data:
    for r in data:
        r['TIMESTAMP'] = convert_datetime_to_string(r['START_TIME'])
        r.pop('START_TIME')
        if 'END_TIME' in r:
            end_timestamp = convert_datetime_to_string(r.get('END_TIME'))
            r['END_TIMESTAMP'] = end_timestamp
            r.pop['END_TIME']
        formatted_data.append(r)
print(formatted_data[0])