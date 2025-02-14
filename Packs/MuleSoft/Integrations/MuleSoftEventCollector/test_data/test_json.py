import json
from datetime import datetime

data = {'platform': 'API Designer xAPI', 'action': 'Save Branch', 'timestamp': 1681349558329, 'userId': '0b4adab7-6ddc-48d5-a6e3-2728ba88d702', 'userName': 'raiju.mathew@resolutionlife.com.au', 'clientId': None, 'clientName': None, 'clientIP': '127.0.0.1', 'payload': {'orgID': '125196b8-b30f-45fb-8c42-8ec36309a844', 'projectID': 'b0df89c2-4b33-47ed-b0ea-0753a02e31b0', 'user': '0b4adab7-6ddc-48d5-a6e3-2728ba88d702', 'action': 'Save Branch', 'detail': 'RLANMCMS-4821-trauma-payment-modification-raiju', 'platform': 'API Designer xAPI'}, 'failed': False, 'failedCause': None, 'objects': [{'objectType': 'Project', 'objectId': 'b0df89c2-4b33-47ed-b0ea-0753a02e31b0', 'objectName': 'b0df89c2-4b33-47ed-b0ea-0753a02e31b0', 'parentId': 'sapi-claimdb', 'parentType': 'Projects', 'environmentId': None, 'environmentName': None}]}
data_str = json.dumps(data)
last_timestamp = datetime.fromtimestamp(1681349558329/1000)
print(last_timestamp)
