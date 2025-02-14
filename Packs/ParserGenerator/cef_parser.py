import json
import csv
import argparse
import re

"""
Sep 12 17:02:13 dsmprdappls201.sg.singtelgroup.net CEF: 0|Trend Micro|Deep Security Agent|20.0.913|4000000|Possible_SCRDL|6|cn1=12341 cn1Label=Host ID dvc=10.148.81.188 TrendMicroDsTenant=Primary TrendMicroDsTenantId=0 filePath=D:\\Temp\\Ad-hoc_Scan\\frms-fraud\\.git\\objects\\d2\\5aa3038c8b291c088b3c2e5535b841d71f5991(\\\\?\\D:\\Temp\\Ad-hoc_Scan\\frms-fraud\\.git\\objects\\d2\\5aa3038c8b291c088b3c2e5535b841d71f5991) act=Pass result=Passed msg=Realtime TrendMicroDsFileSHA1=7286D3A7C3640623AAD2373741B7E976247DA0B5
"""


def generate_parse_xql(raw_log):
    query = ""
    # Handle timestamp
    
    #fields_list = re.findall("([^=|\s]+)=",raw_log)
    fields_list = re.findall("([^= |]+)=", raw_log)
    for field in fields_list:
        if "," not in field and "@" not in field:
            query += f'  {field} = arrayindex(regextract(_raw_log,"{field}=([^\s=]+)"),0),\n'
    return query

# 


def main(file_path,output_file_path):
     
#    parser_rule = """
#alter
#    event_time = parse_timestamp("%b %d %Y %H:%M:%S", arrayindex(regextract(_raw_log,"(\w{3} \d{2} \d{4} \d{2}\:\d{2}\:\d{2})"),0),"Australia/Sydney")
#| alter 
#  _time = if(event_time != null, event_time, _insert_time),
#  cef_version = arrayindex(regextract(_raw_log,"CEF\:(\d)"),0),
#  clearpass_device_ip = arrayindex(regextract(_raw_log,"\w{3} \d{2} \d{4} \d{2}\:\d{2}\:\d{2} (\d+\.\d+\.\d+\.\d+)"),0),\n
#"""

    rules = ""
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            print("Processing row ", row[0])
            if "_raw_log" not in row[0]:
            #    event_type = re.findall("\+0000 (\w+)", row[0])[0]
                rules += generate_parse_xql(row[0])
             
    with open(output_file_path, 'w') as file:
        base_query = """
alter
    event_year = format_timestamp("%Y", _insert_time)
| alter    
    log_timestamp = parse_timestamp("%Y %b %d %H:%M:%S",concat(event_year," ",arrayindex(regextract(_raw_log,"(\w{3}\ \d{2}\ \d{2}\:\d{2}\:\d{2})"),0)),"Australia/Sydney")
| alter
    _time = if(log_timestamp != null, log_timestamp, _insert_time),
    cefHostName = arrayindex(split(_raw_log," "),3),
    cefVersion = arrayindex(regextract(_raw_log,"CEF: (\d)"),0),
    cefDeviceVendor = arrayindex(split(_raw_log,"|"),1),
    cefDeviceProduct = arrayindex(split(_raw_log,"|"),2),
    cefDeviceVersion = arrayindex(split(_raw_log,"|"),3),
    cefDeviceEventClassId = arrayindex(split(_raw_log,"|"),4),
    cefName = arrayindex(split(_raw_log,"|"),5),
    cefSeverity = arrayindex(split(_raw_log,"|"),6),
"""
        full_query_set = list(set(rules.split("\n")))
        #return "  " + "\n  ".join(sorted(list(filter(None,full_query_set)))) + "\n;" # Remove '' and create parsing rules format
        # Remove '' and create parsing rules format    
        file.write(base_query + "\n" + "\n ".join(full_query_set))
        #file.write(full_query_set)
        #file.write(rules)
main("input.csv","output.txt")
