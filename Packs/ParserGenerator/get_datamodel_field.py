import re
import sys

custom_file_name = sys.argv[1] 
with open(custom_file_name,"r") as f:
    rules = f.read()

ootb_file_name = sys.argv[2] 
with open(ootb_file_name,"r") as f:
    ootb_rules = f.read()

def generate_query_fields(dataset, rule):
    dataset_name = re.findall("""dataset\s*=\s*["']?(\w+)?["']?""",dataset)[0]
    fields = list(set(re.findall("xdm\.[^\s=]+", rule)))
    fields.sort()
    fields_list = ",".join(fields)
    return f"datamodel dataset={dataset_name} | fields " + fields_list + "," + f"{dataset_name}._raw_log"

def generate_fields_list(dataset, rule):
    rule_type = []
    fields = list(set(re.findall("xdm\.[^\s=]+", rule)))
    fields.sort()
    for field in fields:
        rule_type.append(compare_ootb(field, rule, ootb_rules))
    fields_list = dataset + "\n" + "\n".join(fields)
    rule_type_list = dataset + "\n" + "\n".join(rule_type)
    return fields_list, rule_type_list


def compare_ootb(field, rule, ootb_rules):
    if re.findall(field.replace(".","\.") + "\s{0,2}=\s{0,1}.+", rule)[0] in ootb_rules:
        return "OOTB"
    else:
        return "Custom"


def generate_query_schema(dataset, rule):
    dataset_name = re.findall("""dataset\s*=\s*["']?(\w+)?["']?""",dataset)[0]
    fields = list(set(re.findall("xdm\.[^\s=,]+", rule)))
    fields.sort()
    comp_query = []
    for field in fields:
        comp_field = field.replace(".","_")
        if field[-1] == "s" \
            and not re.match(".*(?:address$|bytes$|packets$|details$|class$)",field):
            comp_query.append(f'    values(arraystring({field},",")) as {comp_field}')
        else:
            comp_query.append(f"    values({field}) as {comp_field}")
    comp_query_string = ",\n".join(comp_query)
    return f"datamodel dataset={dataset_name} \n| comp \n" + comp_query_string


def get_call_fields(rule, full_rule_set):
    call_rule_data = ""
    call_rules = re.findall("\| call (.+)", rule)
    if call_rules:
        for call_rule in set(call_rules):
            call_rule_data = re.findall(f"RULE.+{call_rule}?[^;]+",full_rule_set)[0]
        return call_rule_data
    else:
        return ""

def generate_model_query(rules):
    query_fields = ""
    query_schema = ""
    fields_list = ""
    rule_list = rules.split("[MODEL:")
    #rule_list = rules.split("datamodel ")
    for rule in rule_list:
        if "dataset" in rule:
            if "[RULE:" in rule:
                rule_data = rule.split("[RULE:")[0]
            else:
                rule_data = rule
            dataset = re.findall("(dataset.+)(?:\]|\s|\|)", rule_data)[0]
            if "content_id" in dataset: dataset = dataset.split(",")[0]
            
            query_fields += generate_query_fields(dataset, rule_data + get_call_fields(rule, rules)).replace('"','') + "\n\n\n"
            query_schema += generate_query_schema(dataset, rule_data + get_call_fields(rule, rules)) + "\n\n\n"
            #fields_list += generate_fields_list(dataset, rule_data + get_call_fields(rule, rules))[0] + "\n\n\n" + \
            #    generate_fields_list(dataset, rule_data + get_call_fields(rule, rules))[1]

    return query_fields, query_schema, fields_list

print("### DATA MODEL QUERY WITH MAPPED FIELDS ###\n\n")
print(generate_model_query(rules)[0])
print("### DATA MODEL QUERY WITH COMP VALUE EACH FIELDS ###\n\n")
print(generate_model_query(rules)[1])
#print("### DATA MODEL FIELDS LIST ###\n\n")
#print(generate_model_query(rules)[0])


