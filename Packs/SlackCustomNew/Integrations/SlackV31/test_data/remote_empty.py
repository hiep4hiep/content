#data = '["mu00217227","mu00178692","dyn-49-127-103-82","vpn-130-194-237-103"],MU00178692.com.au'
data = 'rwortley,testngu,renn.wortley@monash.edu,rngudot,ren.ngudot@gmail.com,5f637f71886a052d6832974d'

current_list = data.lower().replace('"','').replace('[','').replace(']','').replace(' ','').split(',')
# Remove '' item
non_empty_list = [i for i in current_list if i]

# Remove item with fqdn such as MU001XXXXX.com.au
non_fqdn_list = []
for i in non_empty_list:
    if "@" in i:
        non_fqdn_list.append(i)
    elif "." not in i:
        non_fqdn_list.append(i.lower())
    else:
        non_fqdn_list.append(i.split('.')[0].lower())

# Remove duplicated item
non_duplicate_list = list(set(non_fqdn_list))

# Remove short username in UPN
new_list = []
temp_list = non_duplicate_list # Create a temp list to compare

for left in non_duplicate_list:
    for right in temp_list:
        if "@" in right:
            if "@" not in left \
            and left[1:-1] in right \
            and left[1:-1] != right:
                new_list.append(left)

final_list = list(set(non_duplicate_list) - set(new_list))
#final_list = list(set(new_list))

print(final_list)
