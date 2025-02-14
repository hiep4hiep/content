data = {
                "endpoint_id": "0a1bfa94a47c4dc68a9738a47dc3f18a",
                "endpoint_name": "hiep-xsoar",
                "endpoint_type": "AGENT_TYPE_SERVER",
                "endpoint_status": "CONNECTED",
                "os_type": "AGENT_OS_LINUX",
                "os_version": "22.04.3",
                "ip": [
                    "10.0.0.4",
                    "172.17.0.1"
                ],
                "ipv6": [],
                "public_ip": "20.11.183.179",
                "users": [],
                "domain": "4lsdarchxc5e1b3ti0to0zdvjc.qx.internal.cloudapp.net",
                "alias": "",
                "first_seen": 1713771650561,
                "last_seen": 1715151800608,
                "content_version": "1340-81514",
                "installation_package": "Ubuntu",
                "active_directory": [],
                "install_date": 1713771650576,
                "endpoint_version": "8.3.0.121478",
                "is_isolated": "AGENT_UNISOLATED",
                "isolated_date": "null",
                "group_name": [],
                "operational_status": "PARTIALLY_PROTECTED",
                "operational_status_description": "[{\"name\": \"dseStatus\", \"error_code\": 20002, \"is_security_module\": true}, {\"name\": \"antimalwareStatus\", \"error_code\": 20002, \"is_security_module\": true}, {\"name\": \"antiLpeStatus\", \"error_code\": 20002, \"is_security_module\": true}]",
                "operational_status_details": [
                    {
                        "title": "BTP not working",
                        "reason": "Linux kernel module failed to load"
                    },
                    {
                        "title": "Antimalware flow is asynchronous",
                        "reason": "Linux kernel module failed to load"
                    },
                    {
                        "title": "Local privilege escalation",
                        "reason": "Linux kernel module failed to load"
                    }
                ],
                "scan_status": "SCAN_STATUS_NONE",
                "content_release_timestamp": 1714473739000,
                "last_content_update_time": 1714508689666,
                "operating_system": "Ubuntu 22.04",
                "mac_address": [
                    "00:0d:3a:e0:29:78",
                    "02:42:f3:8c:32:b0"
                ],
                "assigned_prevention_policy": "Linux Default",
                "assigned_extensions_policy": "",
                "token_hash": "null",
                "tags": {
                    "server_tags": [],
                    "endpoint_tags": []
                },
                "content_status": "UP_TO_DATE"
            }

for key in data.keys():
    print(key)