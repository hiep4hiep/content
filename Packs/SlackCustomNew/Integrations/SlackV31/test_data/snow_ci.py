#!/usr/bin/python3 -u

import requests as rq
import json, csv
from snowauth import user, passwd, ppasswd
import datetime as dt
import urllib3
urllib3.disable_warnings()

AllCriticalServers=[]

head={
'Accept' : 'application/json',
'Content-Type' : 'application/json'
}
doDebug = True

def debug(message):
    if doDebug:
        print(message)

def get_ag(link):
    ag=rq.get(link,auth=(user,ppasswd), headers=head,verify=False)
    if ag.status_code == 200:
        return json.loads(ag.content)['result']['name']
    
def get_ci(link):
        
    ci_param = { 'sysparm_fields' : 'name,sys_class_name,sys_id,ip_address,subcategory,assignment_group',
        'sysparm_exclude_reference_link' : 'true',
        'sysparm_display_value' : 'true',
       }
    child_ci=rq.get(link,auth=(user,ppasswd), headers=head,verify=False)

    if child_ci.status_code == 200:
        kid=json.loads(child_ci.content)['result']
        sys_class=kid['sys_class_name']
        if kid['install_status'] == "1" and 'storage' not in sys_class and 'ec2_instance' not in sys_class:
            if 'link' in kid['assignment_group']:
                assignment_group=kid['assignment_group']['link']
            else:
                assignment_group=''

            return {'name':kid['name'],'sys_class_name':sys_class,'sys_id':kid['sys_id'],'subcategory':kid['subcategory'],
                    'assignment_group' : assignment_group, 'ip_address': kid['ip_address']}
        else:
            return {}
    else:
        print("could not get ci status: ",child_ci.status_code)
        exit()

def get_hosts(sys_id, AppName, Level):
    rel_param={'sysparm_query' :'parent='+sys_id,
        #'sysparm_exclude_reference_link' : 'true',
        'sysparm_display_value' : 'true',
        }
    childrens=[]
    debug(Level)
    children=rq.get("https://ampau.service-now.com/api/now/table/cmdb_rel_ci",auth=(user,ppasswd),headers=head,params=rel_param,verify=False)
    child_data=json.loads(children.content)['result']
    debug("No of Kids "+str(len(child_data)))
    
    if children.status_code != 200:
        print("Could not get server list :",children.status_code)
        exit()

    for d in child_data:
        if 'child' in d:
            kidName=d['child']['display_value']
            if 'Jenkins' in kidName or 'ampcx' in kidName or \
               'vol' in kidName or 'logs' in kidName or \
               'lb' in kidName or 'LB' in kidName:
                continue
            
            node=get_ci(d['child']['link'])
            if 'name' in node:
                debug(node['name']+' sysclass:'+node['sys_class_name']+'subcategory '+node['subcategory'])
                if 'server' in node['sys_class_name']:
                    assignmentGroup=''
                    if node['assignment_group'] != '':
                        assignmentGroup=get_ag(node['assignment_group'])                    
                    AllCriticalServers.append([node['name'],node['ip_address'], assignmentGroup, AppName])

                    debug("adding "+node['name'])
                elif node['subcategory'] == 'Application' and Level == 'Top':
                    get_hosts(node['sys_id'], node['name'], 'Next')
                elif 'database' in node['sys_class_name']:
                    get_hosts(node['sys_id'], node['name'], 'Next')

        #childrens.append(d['child']['value'])
    return childrens

def get_nonCloudHosts():
    param={
        'sysparm_query' : 'install_status=1^u_cyber_risk_ratingSTARTSWITHCyber',
        'sysparm_fields' : 'name,install_type,number,sys_id,u_cyber_risk_rating',
        #'sysparm_exclude_reference_link' : 'true',
        'sysparm_display_value' : 'true',
        }
    instance="https://ampau.service-now.com/api/now/table/cmdb_ci_business_app"

    r=rq.get(instance, auth=(user,ppasswd), headers=head, params=param, verify=False)

    debug("Getting bus apps: "+str(r.status_code))

    if r.status_code == 200:
        data=json.loads(r.content)['result']
        print("No of BusApps:", len(data))
        for f in data:
            debug(f['name']+' : '+f['install_type'])

            if f['install_type'] == 'Bizcloud' or f['install_type'] == 'External' or 'On Prem' in f['install_type']:
                debug(f['name']+' '+f['install_type']+' '+f['number'])
                childrens=get_hosts(f['sys_id'],f['name'], 'Top')
    else:
        print('Getting Guid for busApps failed',r.content)
        exit()

def get_guid(link):
    #Returns GUID of the Mapped Application Service
    #
    ci_param = {'sysparm_exclude_reference_link' : 'true', 'sysparm_display_value' : 'true',}
    child_ci=rq.get(link,auth=(user,ppasswd), headers=head,verify=False)

    if child_ci.status_code == 200:
        kid=json.loads(child_ci.content)['result']
        #print(dta['name'],dta['install_status']
        return [kid['name'],kid['u_number']]
    else:
        print("CI retrieval failed ",child_ci.status_code)
        exit()
       
def getMasList(sys_id):
    #Returns Mapped Application Service List
    #for the given Business Applicatino sys_id
    rel_param={'sysparm_query' :'parent='+sys_id,
        #'sysparm_exclude_reference_link' : 'true',
        'sysparm_display_value' : 'true',
        }
    debug('getting MAS List')
    instance="https://ampau.service-now.com/api/now/table/cmdb_rel_ci"
    children=rq.get(instance,auth=(user,ppasswd),headers=head,params=rel_param,verify=False)
    if children.status_code != 200:
        print("Error getting Applist ", children.status_code)
        exit()
    
    child_data=json.loads(children.content)['result']   
    guidList={}
    for d in child_data:
        if 'child' in d:
            app_values=get_guid(d['child']['link'])
            guidList[app_values[1]]=app_values[0]
            debug(app_values[0])
    return guidList

def getGuidList():
    #Returns All GUIDs of the Mapped Application Services
    #For all the Business Application which has a 
    #Cyber Risk rating of "Cyber Critical"
    param={
        'sysparm_query' : 'install_status=1^u_cyber_risk_ratingSTARTSWITHCyber',
        'sysparm_fields' : 'sys_id'
        #'sysparm_exclude_reference_link' : 'true',
        #'sysparm_display_value' : 'true',
        }
    debug('getting GuidList')
    instance="https://ampau.service-now.com/api/now/table/cmdb_ci_business_app"

    r=rq.get(instance, auth=(user,ppasswd), headers=head, params=param, verify=False)

    #count=0
    AllGuids={}
    if r.status_code == 200:
        data=json.loads(r.content)['result']
        for f in data:
            maslist=getMasList(f['sys_id'])
            for d in maslist.keys():
                #print(maslist[d])
                AllGuids[d]=maslist[d]
            #AllGuids += getMasList(f['sys_id'])
    else:
        print("error getting GuidList :",r.content)
        exit()

    return AllGuids

def get_CloudHosts(AllGuids):
    param={
    'sysparm_query': 'nameISNOTEMPTY^state!=terminated',
    'sysparm_fields' : 'name,ip_address,assignment_group,correlation_id,u_platform_type',
    #'sysparm_exclude_reference_link' : 'true',
    #'sysparm_display_value' : 'true',
    }

    instance="https://ampau.service-now.com/api/now/table/cmdb_ci_ec2_instance"

    debug('Getting ccsList')
    ec2List=rq.get(instance, auth=(user,ppasswd), headers=head, params=param, verify=False)
    debug("done"+ str(ec2List.status_code))
    #json.dump(AllGuids,open("test_dump.json","w"),indent=4)
    #open("ec2list.txt","w").write(str(ec2List.content))

    if ec2List.status_code == 200:# and 'result' in ec2List.content:
        try:
            ec2listing=json.loads(ec2List.content)['result']
        except:
            print("error in getting ec2listing")
            exit()
        AppGuids = AllGuids.keys()
        AppNames = AllGuids.values()

        for e in ec2listing:
            if e['u_platform_type'] == 'Linux/UNIX':
                continue
            if e['correlation_id'] in AppGuids:
                AllCriticalServers.append([e['name'],e['ip_address'], get_ag(e['assignment_group']['link']),AllGuids[e['correlation_id']]])
            elif e['correlation_id'] in AppNames:
                AllCriticalServers.append([e['name'],e['ip_address'], get_ag(e['assignment_group']['link']),e['correlation_id']])
    else:
        debug('ec2 list retreival failed d'+str(ec2List.status_code))
        return

def get_critical_hosts():
    get_CloudHosts(getGuidList())
    get_nonCloudHosts()    
    #json.dump(AllCriticalServers,open("allcs.txt","w"),indent=4)
    return AllCriticalServers

if __name__ == '__main__':
    get_critical_hosts()
    fname="critical_hosts.csv"
    csvHeader=['Hostname','IP Address','Assignment Group','Application']
    with open(fname,"w",newline='') as c:
        write = csv.writer(c)
        write.writerow(csvHeader)
        write.writerows(AllCriticalServers)
    # Output CSV as a file to war-room
    demisto.results(fileResult(out_filename, csv_string))
    print("All done...")
#EOS