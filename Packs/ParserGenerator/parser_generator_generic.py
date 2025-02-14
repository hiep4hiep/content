import json
import csv
import argparse

def map_name_value(parent_field_name, object, key, value):
    parser = f'| alter {parent_field_name}_{object[key]} = arrayindex(arrayfilter(json_extract_array(to_json_string({parent_field_name}),"$"),"@element" contains "{object[key]}"),0) -> {str(value)}\n'
    return parser

def generate_parse_xql_msft(parent_field_name, parent_field_data):
    """
    args:
        - parent_field_name: name of the JSON key
        - parent_field_data: data/value of the JSON key
    """
    query = ""
    # Handle the key which holds a List
    if isinstance(parent_field_data,list):
        if len(parent_field_data) == 1:
            query += f'| alter {parent_field_name} = arrayindex(json_extract_array(to_json_string({parent_field_name}),"$."),0)\n'
        for item in parent_field_data:
            if "Name" in item and "Value" in item:
                rule = map_name_value(parent_field_name, item, "Name", "Value")
                if rule not in query: query += rule
            if "Type" in item and "ID" in item:
                rule = map_name_value(parent_field_name, item, "Type", "ID")
                if rule not in query: query += rule
            #query += f'| alter {parent_field_name}_{data_type_field} = arrayindex(arrayfilter(json_extract_array({parent_field_name},"$"),"@element" contains "{data_type}"),0)\n'
            
            if isinstance(item,dict):
                for sub_list_field in item:
                    #if sub_list_field != "@odata.type":
                    try:
                        if isinstance(item[sub_list_field],str):
                            query += f'| alter {parent_field_name}_{sub_list_field} = {parent_field_name} -> ["{sub_list_field}"]\n'
                        if isinstance(item[sub_list_field],int):
                            query += f'| alter {parent_field_name}_{sub_list_field} = {parent_field_name} -> {sub_list_field}\n'
                        elif isinstance(item[sub_list_field],list):
                            query += f'| alter {parent_field_name}_{sub_list_field} = {parent_field_name} -> {sub_list_field}[]\n'
                            query += generate_parse_xql_msft(f'{parent_field_name}_{sub_list_field}', item[sub_list_field])
                        elif isinstance(item[sub_list_field],dict):
                            query += f'| alter {parent_field_name}_{sub_list_field} = {parent_field_name} -> {sub_list_field}' + '{}\n'
                            nested_field_name = f'{parent_field_name}_{sub_list_field}'
                            nested_field_data = item[sub_list_field]
                            query += generate_parse_xql_msft(nested_field_name, nested_field_data)
                    except Exception:
                        print(item)
    
            
    # Handle the key which holds a Dict
    else:
        for field in parent_field_data:
            if isinstance(parent_field_data[field],str): 
                rule = f"| alter {parent_field_name}_{field} = {parent_field_name} -> {field}\n"
                if rule not in query: query += rule
            elif isinstance(parent_field_data[field],int): 
                rule = f"| alter {parent_field_name}_{field} = {parent_field_name} -> {field}\n"
                if rule not in query: query += rule
            elif isinstance(parent_field_data[field],list): 
                rule = f"| alter {parent_field_name}_{field} = {parent_field_name} -> {field}[]\n"
                if rule not in query: query += rule
                query += generate_parse_xql_msft(f'{parent_field_name}_{field}', parent_field_data[field])
            elif isinstance(parent_field_data[field],dict): 
                rule = f"| alter {parent_field_name}_{field} = {parent_field_name} -> {field}" + "{},\n"
                if rule not in query: query += rule
                nested_field_name = f"{parent_field_name}_{field}"
                nested_field_data = parent_field_data[field]
                rule = generate_parse_xql_msft(nested_field_name, nested_field_data)
                if rule not in query: query += rule
                
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

    return full_query # Remove '' and create parsing rules format                     


def remove_duplicates(input_list):
    seen = set()
    result = []
    for item in input_list:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return "\n".join(result)


arg_parser = argparse.ArgumentParser(description='Parse TSV result from XQL and generate parser')
arg_parser.add_argument('-i', '--input', type=str, help='The input file path', required=True)
arg_parser.add_argument('-o', '--output', type=str, help='The output file path', required=True)
arg_parser.add_argument('-v', '--vendor', type=str, help='The dataset vendor name', required=True)
arg_parser.add_argument('-p', '--product', type=str, help='The dataset product name', required=True)
args = arg_parser.parse_args()

if args.input:
    file_path = args.input
    output_file_path = args.output
    parsing_rules = remove_duplicates(parse_data().split("\n"))
    xql_parsing_rule = f"""
[INGEST: vendor={args.vendor}, product={args.product}, target_dataset={args.vendor}_{args.product}_raw, no_hit=keep]
{parsing_rules}
"""
with open(output_file_path, 'w') as file:
    file.write(xql_parsing_rule)