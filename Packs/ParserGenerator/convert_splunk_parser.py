import json
import csv
import argparse
import re


def generate_parse_xql(parsed_field):
    parent_field_list = parsed_field.replace('"','').replace("{}","").split(".")
    parent_field_name = parent_field_list[0]
    field_name = parsed_field.replace('"','').replace("{}","").replace(".","_")
    
    json_extract_str = parsed_field.replace("$","").replace(parent_field_name, "$").replace("{}","")
    if "{}" in field_name:
        field_name = field_name.replace("{}","")
        if not re.search("[\:\-\/]",field_name):
            rule = f'{field_name} = json_extract({parent_field_name}, "{json_extract_str}"),\n  '
        else:
            rule = f'{field_name} = json_extract({parent_field_name}, "[' + f"'{json_extract_str}'" + ']"),\n  '
    else:
        if not re.search("[\:\-\/]",field_name):
            field_name = field_name.replace(":","_").replace("--","").replace("-","_").replace("/","_").replace(" ","_")
            rule = f'{field_name} = json_extract_scalar({parent_field_name}, "{json_extract_str}"),\n  '
        else:
            field_name = field_name.replace(":","_").replace("--","").replace("-","_").replace("/","_").replace(" ","_")
            rule = f'{field_name} = json_extract_scalar({parent_field_name}, "[' + f"'{json_extract_str}'" + ']"),\n  '
    return rule



def main(file_path,output_file_path):
    parser_rule = "dataset = aws_guardduty_raw | alter\n  "
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if "." in row[0]: # and not re.search("[\:\-\/]",row[0]):
                parser_rule += generate_parse_xql(row[0])
    with open(output_file_path, 'w') as file:
        file.write(parser_rule)

main("aws_guardduty_field_names.csv","aws_guardduty_raw.txt")