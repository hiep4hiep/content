import re
import sys

custom_file_name = sys.argv[1] 
with open(custom_file_name,"r") as f:
    rules = f.read()

query = "comp "
field_list = rules.split("\t")
for field in field_list:
    if not re.match("^_",field):
        query += f"values({field}) as {field},"
query += "\n\n|alter "
for field in field_list:
    if not re.match("^_",field):
        query += f"{field} = arrayindex({field},0),"
print(query)