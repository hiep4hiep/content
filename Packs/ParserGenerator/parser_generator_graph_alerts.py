import json
import csv
import argparse


def generate_parse_xql_msft(parent_field_name, parent_field_data):
    """
    args:
        - parent_field_name: name of the JSON key
        - parent_field_data: data/value of the JSON key
    """
    query = ""
    # Handle the key which holds a List
    if isinstance(parent_field_data,list):   
        for item in parent_field_data:
            data_type = item.get('@odata.type')
            data_type_field = data_type.replace(".","_").replace("#","")
            query += f'| alter {parent_field_name}_{data_type_field} = arrayindex(arrayfilter(json_extract_array({parent_field_name},"$"),"@element" contains "{data_type}"),0)\n'
            for sub_list_field in item:
                if sub_list_field != "@odata.type":
                    if isinstance(item[sub_list_field],str):
                        query += f'| alter {parent_field_name}_{sub_list_field} = {parent_field_name}_{data_type_field} -> ["{sub_list_field}"]\n'
                    if isinstance(item[sub_list_field],int):
                        query += f'| alter {parent_field_name}_{sub_list_field} = {parent_field_name}_{data_type_field} -> {sub_list_field}\n'
                    elif isinstance(item[sub_list_field],list):
                        query += f'| alter {parent_field_name}_{sub_list_field} = {parent_field_name}_{data_type_field} -> {sub_list_field}[]\n'
                    elif isinstance(item[sub_list_field],dict):
                        query += f'| alter {parent_field_name}_{sub_list_field} = {parent_field_name}_{data_type_field} -> {sub_list_field}' + '{}\n'
                        nested_field_name = f'{parent_field_name}_{sub_list_field}'
                        nested_field_data = item[sub_list_field]
                        query += generate_parse_xql_msft(nested_field_name, nested_field_data)

    # Handle the key which holds a Dict
    else:
        for field in parent_field_data:
            if isinstance(parent_field_data[field],str): query += f"| alter {parent_field_name}_{field} = {parent_field_name} -> {field}\n"
            elif isinstance(parent_field_data[field],int): query += f"| alter {parent_field_name}_{field} = {parent_field_name} -> {field}\n"
            elif isinstance(parent_field_data[field],list): query += f"| alter {parent_field_name}_{field} = {parent_field_name} -> {field}[]\n"
            elif isinstance(parent_field_data[field],dict): 
                query += f"| alter {parent_field_name}_{field} = {parent_field_name} -> {field}" + "{},\n"
                nested_field_name = f"{parent_field_name}_{field}"
                nested_field_data = parent_field_data[field]
                query += generate_parse_xql_msft(nested_field_name, nested_field_data)
                
    return query


def parse_data():
    full_query = ""
    title = []
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        for i, row in enumerate(reader):
            title = row
            break
        # Iterate over each row and column
        for row in reader:
            for j in range(0,len(row)):
                # Find the JSON fields and parse
                if isinstance(row[j],str):
                    if "{" in row[j] and "}" in row[j]:
                        data = json.loads(row[j])
                        full_query += generate_parse_xql_msft(title[j], data)
            break
    return full_query # Remove '' and create parsing rules format                     

arg_parser = argparse.ArgumentParser(description='Parse TSV result from XQL and generate parser')
arg_parser.add_argument('-i', '--input', type=str, help='The input file path', required=True)
arg_parser.add_argument('-o', '--output', type=str, help='The output file path', required=True)
arg_parser.add_argument('-v', '--vendor', type=str, help='The dataset vendor name', required=True)
arg_parser.add_argument('-p', '--product', type=str, help='The dataset product name', required=True)
args = arg_parser.parse_args()

if args.input:
    file_path = args.input
    output_file_path = args.output
    xql_parsing_rule = f"""
[INGEST: vendor={args.vendor}, product={args.product}, target_dataset={args.vendor}_{args.product}_raw, no_hit=keep]
{parse_data()}
"""
with open(output_file_path, 'w') as file:
    file.write(xql_parsing_rule)