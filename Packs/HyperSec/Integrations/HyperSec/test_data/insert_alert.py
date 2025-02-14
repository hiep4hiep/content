import clickhouse_connect
from datetime import datetime, timedelta
import time
import re

#client = clickhouse_connect.get_client(host='qkiyoiudvh.ap-southeast-2.aws.clickhouse.cloud', port=8443, username='heip_xsoar', password='12Xsoar123$#')
client = clickhouse_connect.get_client(host='pki3smqcch.ap-southeast-2.aws.clickhouse.cloud', port=8443, username='default', password='j71W8~pzUmaX~')
#query = "INSERT INTO workshop.alert (timestamp, org_id, detection_time, alert_name, alert_severity, alert_type, confidence_level, condidence_score, remediation_steps, rule_id, source_table, tactics, techniques) VALUES \
#        (now(), 'test_org', now(), 'New Alert Name here', 'high', 'scheduled alert', 'High', 100, 'Remediation steps', 'c5b20776-639a-49bf-94c7-84f912b91c15', 'logs_nxlog_windows', 'command_and_control', 'T1095')"
query = "SHOW DATABASES;"
data = client.command(query)

print(data)
#extracted_fields = re.findall("([^$\s]+)\$\w", '$'.join(data))
#print(extracted_fields)


"""
query_time = datetime.now() - timedelta(days=int(1))
parameters = {'timestamp': query_time}

select_query = "SELECT * FROM workshop.alert WHERE timestamp > %(timestamp)s ORDER BY timestamp"
result = client.query(select_query,parameters=parameters)
print(result.result_rows)
"""