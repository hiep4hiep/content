import json
import sys

file_name = sys.argv[1] 

def generate_rule_doc(rule):
    doc = f"\nRULE - {rule['name']}:\n"
    for k in rule.keys():
        if k != "name" and rule[k]:
            item_name = k.title()
            if k == "xql_query":
                value = "\n" + str(rule[k])
            else:
                value = str(rule[k])
            doc += f"\t{item_name}: {value}\n"
    return doc

with open(file_name,"r") as f:
    data = json.load(f)

as_built = ""
for rule in data:
    as_built += generate_rule_doc(rule)
print(as_built)


