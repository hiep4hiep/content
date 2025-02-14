data = """
Run2Zero2
Name: MU00220534
Newest MAC: 70-cd-0d-96-6c-f7
MAC Addresses: 00-05-9a-3c-7a-00
IP Address: 49.127.58.95

Crowdstrike
Crowdstrike Address: 
Crowdstrike Hostname: 
"""

import re

data1 = re.sub("[ \w]+: [\n]", "", data)
catch = re.findall("^\w+", data1)
data2 = re.sub("^\w+","", data1)

print(data1)
print("######")
print(catch)