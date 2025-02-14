import re
import sys

custom_file_name = sys.argv[1] 
with open(custom_file_name,"r") as f:
    rules = f.read()


def generate_fields(rule):
    fields = re.findall("([^\s]+)\s?=\s?.+", rule)
    parse_statement = re.findall("[^\s]+\s?=\s?(.+)", rule)
    pair = "Field Name\tParse statement\tDescription\tSample value from Log\n"
    for i in range(0,len(fields)-1):
        if "INGEST" in fields[i]: 
            pass
        else:
            pair += f"{fields[i]}\t{parse_statement[i][0:-1]}\t\n"
    return pair

def generate_value_query(rule):
    query = "comp "
    field_list =  set(re.findall("([^\s]+)\s?=\s?.+", rule))
    for field in list(field_list):
        if not re.match("^_",field):
            query += f"values({field}) as {field},"
    query = query[0:-1]
    query += "\n\n|alter "
    for field in field_list:
        if not re.match("^_",field):
            query += f"{field} = arrayindex({field},0),"
    query = query[0:-1]
    return query


def generate_value_query_from_tsv(rule):
    query = "comp "
    field_list =  rule.split("\t")
    for field in field_list:
        if not re.match("^_",field):
            query += f"values({field}) as {field},"
    query = query[0:-1]
    query += "\n\n|alter "
    for field in field_list:
        if not re.match("^_",field):
            query += f"{field} = arrayindex({field},0),"
    query = query[0:-1]
    return query


if ".tsv" in custom_file_name:
    with open(f"./{custom_file_name}_query.txt","w") as f:
        f.write(generate_value_query_from_tsv(rules))

else:
    with open(f"./{custom_file_name}.tsv","w") as f:
        f.write(generate_fields(rules))

    with open(f"./{custom_file_name}_query.txt","w") as f:
        f.write(generate_value_query(rules))


