import yaml
import sys

def convert_quiet_mode(mode):
    if mode == 0: return "On"
    elif mode == 1 or mode == 2: return "Off"


file_name = sys.argv[1] 
with open(file_name,"r") as f:
    data = yaml.safe_load(f)


doc = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sample HTML Document</title>
</head>
<body>
<table>
        
</table>

"""
doc += f"<h3>{data['name']}</h3>"

tasks = data['tasks']
for task_id in tasks.keys():
    doc += f"<h4>Task {task_id}:</h4><br>"
    
    task_data = tasks[task_id]
    doc += f"<strong>- Type: {task_data['type']}</strong><br>"
    for task_item in task_data.keys():
        # Produce Task data
        if task_item == "task":
            for task_item_params in task_data[task_item]:
                if task_item_params not in ("version","brand","id"):
                    if task_item_params == "iscommand": doc += f"<strong>- Integration Command/Builtin Script:</strong> {task_data[task_item][task_item_params]}<br>"
                    else: doc += f"<strong>- {task_item_params.title()}:</strong> {task_data[task_item][task_item_params]}<br>"
            
    # Produce script argument
    scripts = tasks[task_id].get('scriptarguments', None)
    if scripts:
        doc += f"<strong>- Script Arguments:</strong><br>"
        for arg in scripts.keys():
            if 'simple' in scripts[arg].keys():
                doc += f"&nbsp;&nbsp;{arg}: {str(scripts[arg].get('simple'))}<br>"
            else:
                doc += f"&nbsp;&nbsp;{arg}: {str(scripts[arg])}<br>"
    # Produce other params
    for other in tasks[task_id].keys():
        if other not in ("scriptarguments","continueonerrortype","task","isoversize","isautoswitchedtoquietmode","skipunavailable","ignoreworker","timertriggers","view","taskid","separatecontext","nexttasks"):        
            if other == "quietmode":
                doc += f"<strong>- Quiet Mode:</strong> {convert_quiet_mode(tasks[task_id][other])}<br>"
            else:
                doc += f"<strong>- {other.title()}:</strong> {tasks[task_id][other]}<br>"

doc += "</body></html>"

with open("generated_html.html","w") as f:
    f.write(doc)
