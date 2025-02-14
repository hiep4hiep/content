search_input = '''{\"id\": \"268a011b7058c2a9e0b0351317d1f632\", \"indicator_type\": \"IP\", \"score\": 3, \"value\": \"45.66.231.148\", \"verdict\": \"Bad\"}, {\"id\": \"8b38249291af1556a620aec459061e5d\", \"indicator_type\": \"IP\", \"score\": 3, \"value\": \"94.156.71.74\", \"verdict\": \"Bad\"}, {\"id\": \"9991d3590f6c908ca67a0bd17743d2e3\", \"indicator_type\": \"IP\", \"score\": 3, \"value\": \"93.123.39.87\", \"verdict\": \"Bad\"}'''
data = search_input.split("}, {")
search_output = ""
for indicator in data:
	if indicator[-1] != "}": indicator += "}"
	if indicator[0] != "{": indicator = "{" + indicator
	print(indicator)
	search_output += f'to_json_string("{indicator}"),'
	
print(search_output[0:-1])