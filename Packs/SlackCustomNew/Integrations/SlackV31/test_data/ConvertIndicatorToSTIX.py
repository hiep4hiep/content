from CommonServerPython import *
import demistomock as demisto

import dateparser as dateparser

''' IMPORTS '''
import json
import uuid
from stix2 import Bundle, ExternalReference, Indicator, Vulnerability, MarkingDefinition, File
from stix2 import AttackPattern, Campaign, Malware, Infrastructure, IntrusionSet, Report, ThreatActor
from stix2 import Identity, Location, MalwareAnalysis, Note, ObservedData, Opinion, Vulnerability
from stix2 import Artifact, AutonomousSystem, Directory, EmailMessage, MACAddress, Mutex, NetworkTraffic,\
                    Process, Software, UserAccount, WindowsRegistryKey, X509Certificate
from stix2 import Tool, CourseOfAction
from typing import Any, Callable

SCOs: dict[str, str] = {  # pragma: no cover
    "md5": "file:hashes.md5",
    "sha1": "file:hashes.sha1",
    "sha256": "file:hashes.sha256",
    "ssdeep": "file:hashes.ssdeep",
    "ip": "ipv4-addr:value",
    "cidr": "ipv4-addr:value",
    "ipv6": "ipv6-addr:value",
    "ipv6cidr": "ipv6-addr:value",
    "url": "url:value",
    "email": "email-message:sender_ref.value",
    "account": "user-account:account_login",
    "domain": "domain-name:value",
    "host": "domain-name:value",
    "registry key": "windows-registry-key:key",
    "asn": "autonomous-system:name"
}

SDOs: dict[str, Callable] = {  # pragma: no cover
    "malware": Malware,
    "attack pattern": AttackPattern,
    "campaign": Campaign,
    "infrastructure": Infrastructure,
    "tool": Tool,
    "intrusion set": IntrusionSet,
    "report": Report,
    "threat actor": ThreatActor,
    "cve": Vulnerability,
    "course of action": CourseOfAction,
    "identity": Identity,
    "infrastructure": Infrastructure,
    "location": Location,
    "malware analysis": MalwareAnalysis,
    "note": Note,
    "observed data": ObservedData,
    "opinion": Opinion,
}

SCO_DET_ID_NAMESPACE = uuid.UUID('00abedb4-aa42-466c-9c01-fed23315a9b7')
PAWN_UUID = uuid.uuid5(uuid.NAMESPACE_URL, 'https://www.paloaltonetworks.com')

XSOAR_TYPES_TO_STIX_SCO = {   # pragma: no cover
    FeedIndicatorType.CIDR: 'ipv4-addr',
    FeedIndicatorType.DomainGlob: 'domain-name',
    FeedIndicatorType.IPv6: 'ipv6-addr',
    FeedIndicatorType.IPv6CIDR: 'ipv6-addr',
    FeedIndicatorType.Account: 'user-account',
    FeedIndicatorType.Domain: 'domain-name',
    FeedIndicatorType.Email: 'email-addr',
    FeedIndicatorType.IP: 'ipv4-addr',
    FeedIndicatorType.Registry: 'windows-registry-key',
    FeedIndicatorType.File: 'file',
    FeedIndicatorType.URL: 'url',
    FeedIndicatorType.Software: 'software',
    FeedIndicatorType.AS: 'autonomous-system',
    'Image': 'artifact',
    'X509 Certificate': 'x509-certificate',
}

XSOAR_TYPES_TO_STIX_SDO = {  # pragma: no cover
    ThreatIntel.ObjectsNames.ATTACK_PATTERN: 'attack-pattern',
    ThreatIntel.ObjectsNames.CAMPAIGN: 'campaign',
    ThreatIntel.ObjectsNames.COURSE_OF_ACTION: 'course-of-action',
    ThreatIntel.ObjectsNames.INFRASTRUCTURE: 'infrastructure',
    ThreatIntel.ObjectsNames.INTRUSION_SET: 'intrusion-set',
    ThreatIntel.ObjectsNames.REPORT: 'report',
    ThreatIntel.ObjectsNames.THREAT_ACTOR: 'threat-actor',
    ThreatIntel.ObjectsNames.TOOL: 'tool',
    ThreatIntel.ObjectsNames.MALWARE: 'malware',
    FeedIndicatorType.CVE: 'vulnerability',
    'Location': 'location',
    'Malware Analysis': 'malware-analysis',
    'Note': 'note',
    'Observed Data': 'observed-data',
    'Opinion': 'opinon',
    'Identity': 'identity'
}


HASH_TYPE_TO_STIX_HASH_TYPE = {  # pragma: no cover
    'md5': 'MD5',
    'sha1': 'SHA-1',
    'sha256': 'SHA-256',
    'sha512': 'SHA-512',
}


CREDIBILITY_LABEL = {
    "Confirmed by other sources":["admiralty-scale:information-credibility=\"1\""],
    "Probably true": ["admiralty-scale:information-credibility=\"2\""],
    "Possibly true": ["admiralty-scale:information-credibility=\"3\""],
    "Doubtful":["admiralty-scale:information-credibility=\"4\""],
    "Improbable":["admiralty-scale:information-credibility=\"5\""],
    "Truth cannot be judged":["admiralty-scale:information-credibility=\"6\""]
}

TLP_MARKING = {
    "RED": ["marking-definition--5e57c739-391a-4eb3-b6be-7d15ca92d5ed"],
    "AMBER+STRICT": ["marking-definition--5e57c739-391a-4eb3-b6be-7d15ca92d5ed"],
    "AMBER": ["marking-definition--f88d31f6-486f-44da-b317-01333bde0b82"],
    "GREEN": ["marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da"],
    "WHITE": ["marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9"],
    "CLEAR": ["marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9"]
}


def hash_type(value: str) -> str:  # pragma: no cover
    length = len(value)
    if length == 32:
        return 'md5'
    if length == 40:
        return 'sha1'
    if length == 64 and ":" in value:
        return 'ssdeep'
    elif length == 64:
        return 'sha256'
    if length == 128:
        return 'sha512'
    return ''


def guess_indicator_type(type_: str, val: str) -> str:
    # try to guess by key
    for sco in SCOs:
        if sco in type_:
            return sco

    # try to auto_detect by value
    return (auto_detect_indicator_type(val) or type_).lower()


def create_sco_stix_uuid(xsoar_indicator: dict, stix_type: Optional[str], value: str) -> str:
    """
    Create uuid for SCO objects.
    Args:
        xsoar_indicator: dict - The XSOAR representation of the indicator.
        stix_type: Optional[str] - The indicator type according to STIX.
        value: str - The value of the indicator.
    Returns:
        The uuid that represents the indicator according to STIX.
    """
    if stixid := xsoar_indicator.get('CustomFields', {}).get('stixid'):
        return stixid
    if stix_type == 'user-account':
        account_type = xsoar_indicator.get('CustomFields', {}).get('accounttype')
        user_id = xsoar_indicator.get('CustomFields', {}).get('userid')
        unique_id = uuid.uuid5(SCO_DET_ID_NAMESPACE,
                               f'{{"account_login":"{value}","account_type":"{account_type}","user_id":"{user_id}"}}')
    elif stix_type == 'windows-registry-key':
        unique_id = uuid.uuid5(SCO_DET_ID_NAMESPACE, f'{{"key":"{value}"}}')
    elif stix_type == 'file':
        if 'md5' == get_hash_type(value):
            unique_id = uuid.uuid5(SCO_DET_ID_NAMESPACE, f'{{"hashes":{{"MD5":"{value}"}}}}')
        elif 'sha1' == get_hash_type(value):
            unique_id = uuid.uuid5(SCO_DET_ID_NAMESPACE, f'{{"hashes":{{"SHA-1":"{value}"}}}}')
        elif 'sha256' == get_hash_type(value):
            unique_id = uuid.uuid5(SCO_DET_ID_NAMESPACE, f'{{"hashes":{{"SHA-256":"{value}"}}}}')
        elif 'sha512' == get_hash_type(value):
            unique_id = uuid.uuid5(SCO_DET_ID_NAMESPACE, f'{{"hashes":{{"SHA-512":"{value}"}}}}')
        else:
            unique_id = uuid.uuid5(SCO_DET_ID_NAMESPACE, f'{{"value":"{value}"}}')
    else:
        unique_id = uuid.uuid5(SCO_DET_ID_NAMESPACE, f'{{"value":"{value}"}}')

    return f'{stix_type}--{unique_id}'


def create_sdo_stix_uuid(xsoar_indicator: dict, stix_type: Optional[str], value: str) -> str:
    """
    Create uuid for SDO objects.
    Args:
        xsoar_indicator: dict - The XSOAR representation of the indicator.
        stix_type: Optional[str] - The indicator type according to STIX.
        value: str - The value of the indicator.
    Returns:
        The uuid that represents the indicator according to STIX.
    """
    if stixid := xsoar_indicator.get('CustomFields', {}).get('stixid'):
        return stixid
    if stix_type == 'attack-pattern':
        if mitre_id := xsoar_indicator.get('CustomFields', {}).get('mitreid'):
            unique_id = uuid.uuid5(PAWN_UUID, f'{stix_type}:{mitre_id}')
        else:
            unique_id = uuid.uuid5(PAWN_UUID, f'{stix_type}:{value}')
    else:
        unique_id = uuid.uuid5(PAWN_UUID, f'{stix_type}:{value}')

    return f'{stix_type}--{unique_id}'


def add_file_fields_to_indicator(xsoar_indicator: Dict, value: str) -> Dict:
    """
    Create the hashes dictionary for the indicator object.
    Args:
        xsoar_indicator: Dict - The XSOAR representation of the indicator.
        value: str - The value of the indicator.
    Returns:
        The dictionary with the file hashes.
    """
    hashes_dict = {}
    for hash_kind in ['md5', 'sha1', 'sha256', 'sha512']:
        if get_hash_type(value) == hash_kind:
            hashes_dict[HASH_TYPE_TO_STIX_HASH_TYPE.get(hash_kind)] = value
        elif hash_kind in xsoar_indicator:
            hashes_dict[HASH_TYPE_TO_STIX_HASH_TYPE.get(hash_kind)] = xsoar_indicator.get(hash_kind, '')
    return hashes_dict


def create_stix_sco_indicator(stix_id: Optional[str], stix_type: Optional[str], value: str, xsoar_indicator: Dict) -> Dict:
    """
    Create stix sco indicator object.
    Args:
        stix_id: Optional[str] - The stix id of the indicator.
        stix_type: str - the stix type of the indicator.
        xsoar_indicator: Dict - The XSOAR representation of the indicator.
        value: str - The value of the indicator.
    Returns:
        The Dictionary representing the stix indicator.
    """
    stix_indicator: Dict[str, Any] = {
        "type": stix_type,
        "spec_version": "2.1",
        "id": stix_id
    }
    if stix_type == 'file':
        stix_indicator['hashes'] = add_file_fields_to_indicator(xsoar_indicator, value)
    elif stix_type == 'autonomous-system':
        stix_indicator['number'] = value
        stix_indicator['name'] = xsoar_indicator.get('name', '')
    else:
        stix_indicator['value'] = value
    stix_indicator["created"] = dateparser.parse(xsoar_indicator.get('timestamp', '')).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    stix_indicator["modified"] = dateparser.parse(xsoar_indicator.get('timestamp', '')).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    stix_indicator["labels"] = CREDIBILITY_LABEL.get(xsoar_indicator['CustomFields'].get('credibility', 'Truth cannot be judged'))
    stix_indicator["description"] = xsoar_indicator.get('description', '')
    stix_indicator["name"] = xsoar_indicator.get('value', '')
    stix_indicator["object_marking_refs"] = TLP_MARKING.get(xsoar_indicator['CustomFields'].get('trafficlightprotocol', 'GREEN'))
    return stix_indicator


def create_stix_sdo_indicator(xsoar_indicator: Dict, **kwargs) -> Dict:
    print("Processing SDO")
    kwargs["labels"] = CREDIBILITY_LABEL.get(xsoar_indicator['CustomFields'].get('credibility', 'Truth cannot be judged'))
    kwargs["description"] = xsoar_indicator.get('description', '')
    kwargs["name"] = xsoar_indicator.get('value', '')
    kwargs["object_marking_refs"] = TLP_MARKING.get(xsoar_indicator['CustomFields'].get('trafficlightprotocol', 'GREEN'))
    if xsoar_indicator.get('CustomFields',{}).get('mitreid'):
        kwargs["labels"] += [xsoar_indicator.get('CustomFields',{}).get('mitreid')]

    indicator_type = xsoar_indicator.get('indicator_type').lower()
    object = SDOs[indicator_type](
        **kwargs
        )
    print(object)
    return dict(object)
    


def verify_mandatory_fields(xsoar_indicator):
    if isinstance(xsoar_indicator['CustomFields'],str):
        return f"TLP or Admiralty tag is missing for indicator {xsoar_indicator['value']}"
    elif not xsoar_indicator['CustomFields'].get('credibility'):
        return f"Admiralty tag is missing for indicator {xsoar_indicator['value']}"
    elif not xsoar_indicator['CustomFields'].get('trafficlightprotocol'):
        return f"TLP tag is missing for indicator {xsoar_indicator['value']}"
    else:
        return ""


def main(test_val):
    
    user_args = demisto.args().get('indicators', 'Unknown')
    doubleBackslash = demisto.args().get('doubleBackslash', True)
    is_sco = argToBoolean(demisto.args().get('sco_flag', False))
    """
    if isinstance(user_args, dict):
        all_args = user_args
    else:
        all_args = json.loads(user_args)

    if isinstance(all_args, dict):
        all_indicators = [all_args]
    else:
        all_indicators = all_args
    """
    all_indicators = test_val
    indicators = []

    for xsoar_indicator in all_indicators:
        kwargs: dict[str, Any] = {"allow_custom": True}

        demisto_indicator_type = xsoar_indicator.get('indicator_type', 'Unknown')
        validity_check = verify_mandatory_fields(xsoar_indicator)

        if validity_check == "":
            if doubleBackslash:
                value = xsoar_indicator.get('value', '').replace('\\', r'\\')
            else:
                value = xsoar_indicator.get('value', '')

            # Create SCO object
            if demisto_indicator_type in XSOAR_TYPES_TO_STIX_SCO and demisto_indicator_type != "File":#and is_sco:
                stix_type = XSOAR_TYPES_TO_STIX_SCO.get(demisto_indicator_type)
                stix_id = create_sco_stix_uuid(xsoar_indicator, stix_type, value)
                stix_indicator = create_stix_sco_indicator(stix_id, stix_type, value, xsoar_indicator)
                indicators.append(stix_indicator)
                print("Process SCO")

            elif demisto_indicator_type in XSOAR_TYPES_TO_STIX_SCO and demisto_indicator_type == "File":#and is_sco:
                try:
                    indicator_type = demisto_indicator_type.lower().replace("-", "")
                    if indicator_type == 'file':
                        indicator_type = hash_type(value)
                    if indicator_type not in SCOs and indicator_type not in SDOs:
                        indicator_type = guess_indicator_type(indicator_type, value)
                    if "file" in kwargs["id"]:
                        indicator = File(hashes={"SHA256": xsoar_indicator.get('value', '')},
                                          **kwargs)
                    else:
                        indicator = Indicator(pattern=f"[{SCOs[indicator_type]} = '{value}']",
                                              pattern_type='stix',
                                              **kwargs)
                    indicators.append(indicator)
                
                except KeyError:
                    demisto.debug(f"{demisto_indicator_type} isn't a SCO, checking other IOC types")
                    try:
                        indicator_type = demisto_indicator_type.lower()
                        if indicator_type == 'cve':
                            kwargs["external_references"] = [ExternalReference(source_name="cve", external_id=value)]
                        elif indicator_type == "attack pattern":
                            try:
                                mitreid = xsoar_indicator.get('mitreid', '')
                                if mitreid:
                                    kwargs["external_references"] = [
                                        ExternalReference(source_name="mitre", external_id=mitreid)]
                            except KeyError:
                                pass
                        elif indicator_type == 'malware':
                            kwargs['is_family'] = argToBoolean(xsoar_indicator.get('ismalwarefamily', 'False').lower())
                        indicator = SDOs[indicator_type](
                            name=value,
                            **kwargs
                        )            
                        indicators.append(indicator)
                    except (KeyError, TypeError) as e:
                        demisto.info(
                            "Indicator type: {}, with the value: {} is not STIX compatible".format(demisto_indicator_type,
                                                                                                   value))
                        demisto.info("Export failure excpetion: {}".format(e))
                        continue

            # Create SDO
            elif demisto_indicator_type in XSOAR_TYPES_TO_STIX_SDO:
                stix_type = XSOAR_TYPES_TO_STIX_SDO.get(demisto_indicator_type, 'indicator')
                if demisto_indicator_type == "Malware":
                    kwargs['is_family'] = True
                elif demisto_indicator_type == "Location":
                    kwargs['country'] = xsoar_indicator.get('CustomFields').get('countryname','N/A')
                elif demisto_indicator_type == "Malware Analysis":
                    kwargs['product'] = xsoar_indicator.get('CustomFields').get('product','N/A')
                    kwargs['result'] = xsoar_indicator.get('CustomFields').get('analysisresult','N/A')
                elif demisto_indicator_type == "Note":
                    kwargs['content'] = xsoar_indicator.get('CustomFields').get('notecontent','N/A')
                    kwargs['object_refs'] = xsoar_indicator.get('CustomFields').get('targetobjectid','N/A')
                elif demisto_indicator_type == "Observed Data":
                    kwargs['first_observed'] = dateparser.parse(xsoar_indicator.get('firstseen','2023-10-13T00:51:31.868755Z')).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    kwargs['last_observed'] = dateparser.parse(xsoar_indicator.get('lastseen','2023-10-13T00:51:31.868755Z')).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    kwargs['number_observed'] = xsoar_indicator.get('CustomFields').get('numberobserved', 1)
                    kwargs['object_refs'] = xsoar_indicator.get('CustomFields').get('targetobjectid','N/A')
                elif demisto_indicator_type == "Opinion":
                    kwargs['opinion'] = xsoar_indicator.get('CustomFields').get('opinion', 'strongly-agree')
                    kwargs['object_refs'] = xsoar_indicator.get('CustomFields').get('targetobjectid','N/A')
                elif demisto_indicator_type == "Report":
                    kwargs['published'] = dateparser.parse(xsoar_indicator.get('CustomFields').get('published','2023-10-13T00:51:31.868755Z')).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    kwargs['object_refs'] = xsoar_indicator.get('CustomFields').get('targetobjectid','N/A')

                stix_indicator = create_stix_sdo_indicator(xsoar_indicator,**kwargs)
                indicators.append(stix_indicator)
                print("Process SDO new")

                
    print(indicators)
    
    if len(indicators) > 1:
        bundle = Bundle(indicators, allow_custom=True)
        context = {
            'StixExportedIndicators(val.pattern && val.pattern == obj.pattern)': json.loads(str(bundle))
        }
        res = (CommandResults(readable_output="",
                              outputs=context,
                              raw_response=str(bundle)))

    elif len(indicators) == 1:
        bundle = Bundle(indicators, allow_custom=True)
        bundle_obj = bundle.get('objects', [])[0]
        context = {
            'StixExportedIndicators(val.pattern && val.pattern == obj.pattern)': json.loads(str(bundle_obj))
        }
        res = (CommandResults(readable_output="",
                              outputs=context,
                              raw_response=str(bundle_obj)))
    else:
        if validity_check == "":
            context = {
                'StixExportedIndicators': {}
            }
            res = CommandResults(readable_output="",
                                 outputs=context,
                                 raw_response={})
        else:
            context = {
                'StixExportedIndicators': {'error': validity_check}
            }
            res = CommandResults(readable_output="",
                                 outputs=context,
                                 raw_response={})
   
    return_results(res)


if __name__ in ('__builtin__', 'builtins', '__main__'):
    test_val = [
        {
            "sortValues": [
                "1696907896222",
                "d1d2fc142d3076424f3c25d764b1cb32"
            ],
            "expirationStatus": "active",
            "isDetectable": False,
            "isPreventable": False,
            "modified": "2023-10-13T03:10:18.674081125Z",
            "CustomFields": {
                "credibility": "Doubtful",
                "ctissubmitted": False,
                "description": "n/a",
                "tags": [
                    "admiralty-scale:information-credibility=\"4\""
                ],
                "trafficlightprotocol": "AMBER+STRICT"
            },
            "sequenceNumber": 610416,
            "indicator_type": "URL",
            "expirationSource": {
                "brand": "TAXII 2 Feed",
                "expirationInterval": 43200,
                "expirationPolicy": "indicatorType",
                "instance": "TAXII2_CTIS_1",
                "moduleId": "90df870e-dbd9-4327-82b4-07d9278a6964",
                "setTime": "2023-10-10T04:15:19.717537732Z",
                "source": "indicatorType",
                "user": ""
            },
            "firstSeen": "2023-10-09T23:31:28.589380256Z",
            "calculatedTime": "2023-10-10T03:18:16.222654697Z",
            "primaryTerm": 1,
            "value": "https://dpc12.crtx.au.paloaltonetwork2s.com/dashboard?id=7",
            "lastSeen": "2023-10-10T03:18:16.222654697Z",
            "score": 0,
            "comments": [
                {
                    "created": "2023-10-09T23:31:28.579738787Z",
                    "modified": "0001-01-01T00:00:00Z",
                    "user": "DBot",
                    "entryId": "4673415f-5531-41c1-8511-7863da856f3f@1189",
                    "version": 0,
                    "content": "Created",
                    "type": "IndicatorCommentTimeLine",
                    "source": "4673415f-5531-41c1-8511-7863da856f3f@1189",
                    "id": "d10ad424-71f5-4e2c-89b1-238a244ee1ec",
                    "cacheVersn": 0,
                    "category": "Sighting"
                },
                {
                    "created": "2023-10-09T23:33:57.014920809Z",
                    "modified": "0001-01-01T00:00:00Z",
                    "user": "hnguyen@paloaltonetworks.com",
                    "entryId": "",
                    "version": 0,
                    "content": "The value of field Traffic Light Protocol changed to AMBER+STRICT",
                    "type": "IndicatorCommentTimeLine",
                    "source": "hnguyen@paloaltonetworks.com",
                    "id": "8a6b8576-bbf0-4a90-8e05-081ea7e01d0f",
                    "cacheVersn": 0,
                    "category": "Indicator Update"
                },
                {
                    "created": "2023-10-09T23:33:57.143016925Z",
                    "modified": "0001-01-01T00:00:00Z",
                    "user": "hnguyen@paloaltonetworks.com",
                    "entryId": "",
                    "version": 0,
                    "content": "The value of field Credibility changed to Possibly true",
                    "type": "IndicatorCommentTimeLine",
                    "source": "hnguyen@paloaltonetworks.com",
                    "id": "4f8bfb9f-b0d4-45f1-821f-41c21a272e4d",
                    "cacheVersn": 0,
                    "category": "Indicator Update"
                },
                {
                    "created": "2023-10-10T02:35:42.702090526Z",
                    "modified": "0001-01-01T00:00:00Z",
                    "user": "DBot",
                    "entryId": "3411477e-9068-44a4-8fb3-e4853b2ec0e5@1192",
                    "version": 0,
                    "content": "Sighted",
                    "type": "IndicatorCommentTimeLine",
                    "source": "3411477e-9068-44a4-8fb3-e4853b2ec0e5@1192",
                    "id": "dd7bc99c-520a-47f7-8a26-27790b777631",
                    "cacheVersn": 0,
                    "category": "Sighting"
                },
                {
                    "created": "2023-10-10T02:36:14.537875978Z",
                    "modified": "0001-01-01T00:00:00Z",
                    "user": "hnguyen@paloaltonetworks.com",
                    "entryId": "",
                    "version": 0,
                    "content": "The value of field Credibility changed from Possibly true to Doubtful",
                    "type": "IndicatorCommentTimeLine",
                    "source": "hnguyen@paloaltonetworks.com",
                    "id": "1cefe7de-b62f-45de-858e-2a40951bfe05",
                    "cacheVersn": 0,
                    "category": "Indicator Update"
                },
                {
                    "created": "2023-10-10T02:38:59.69817475Z",
                    "modified": "0001-01-01T00:00:00Z",
                    "user": "DBot",
                    "entryId": "",
                    "version": 0,
                    "content": "The value of field CTIS Submitted changed to true",
                    "type": "IndicatorCommentTimeLine",
                    "source": "DBot",
                    "id": "28970864-102b-489a-8c14-6578a68d5968",
                    "cacheVersn": 0,
                    "category": "Indicator Update"
                },
                {
                    "created": "2023-10-10T03:18:16.213026285Z",
                    "modified": "0001-01-01T00:00:00Z",
                    "user": "DBot",
                    "entryId": "7bfa3aa3-c0b0-44de-86ee-136f63419d07@1194",
                    "version": 0,
                    "content": "Sighted",
                    "type": "IndicatorCommentTimeLine",
                    "source": "7bfa3aa3-c0b0-44de-86ee-136f63419d07@1194",
                    "id": "966b5a0c-c3da-44c1-8dee-8daa6685df73",
                    "cacheVersn": 0,
                    "category": "Sighting"
                },
                {
                    "created": "2023-10-10T04:15:19.71754286Z",
                    "modified": "0001-01-01T00:00:00Z",
                    "user": "DBot",
                    "entryId": "",
                    "version": 0,
                    "content": "Sighted",
                    "type": "IndicatorCommentTimeLine",
                    "source": "TAXII 2 Feed.TAXII2_CTIS_1",
                    "id": "7913a174-0315-4718-836b-05fe66b92b38",
                    "cacheVersn": 0,
                    "category": "Sighting"
                },
                {
                    "created": "2023-10-10T04:15:19.723323211Z",
                    "modified": "0001-01-01T00:00:00Z",
                    "user": "DBot",
                    "entryId": "",
                    "version": 0,
                    "content": "The value of field Description changed to n/a",
                    "type": "IndicatorCommentTimeLine",
                    "source": "TAXII 2 Feed.TAXII2_CTIS_1",
                    "id": "27bc4ffe-b1e0-43d2-8b4e-58868f211c76",
                    "cacheVersn": 0,
                    "category": "Indicator Update"
                },
                {
                    "created": "2023-10-10T04:15:19.723347471Z",
                    "modified": "0001-01-01T00:00:00Z",
                    "user": "DBot",
                    "entryId": "",
                    "version": 0,
                    "content": "The value admiralty-scale:information-credibility=\"4\" was added to field Tags",
                    "type": "IndicatorCommentTimeLine",
                    "source": "TAXII 2 Feed.TAXII2_CTIS_1",
                    "id": "671fd71a-796b-4311-8a6b-a09a6e24e1fd",
                    "cacheVersn": 0,
                    "category": "Indicator Update"
                },
                {
                    "created": "2023-10-10T04:15:19.723369362Z",
                    "modified": "0001-01-01T00:00:00Z",
                    "user": "DBot",
                    "entryId": "",
                    "version": 0,
                    "content": "The value of field Traffic Light Protocol changed from AMBER+STRICT to WHITE",
                    "type": "IndicatorCommentTimeLine",
                    "source": "TAXII 2 Feed.TAXII2_CTIS_1",
                    "id": "61fe84c9-72ca-4bad-8848-811c83b69adf",
                    "cacheVersn": 0,
                    "category": "Indicator Update"
                },
                {
                    "created": "2023-10-10T07:27:40.791584636Z",
                    "modified": "0001-01-01T00:00:00Z",
                    "user": "hnguyen@paloaltonetworks.com",
                    "entryId": "",
                    "version": 0,
                    "content": "The value of field Traffic Light Protocol changed from WHITE to AMBER+STRICT",
                    "type": "IndicatorCommentTimeLine",
                    "source": "hnguyen@paloaltonetworks.com",
                    "id": "3622af2a-288e-4d77-8b8e-644467a5ced6",
                    "cacheVersn": 0,
                    "category": "Indicator Update"
                },
                {
                    "created": "2023-10-10T08:16:21.020011875Z",
                    "modified": "0001-01-01T00:00:00Z",
                    "user": "DBot",
                    "entryId": "",
                    "version": 0,
                    "content": "New relationship indicated-by created to Campaign: Malware test",
                    "type": "IndicatorCommentTimeLine",
                    "source": "TAXII2_CTIS_1 (TAXII 2 Feed)",
                    "id": "0a83b542-7548-455e-87d5-d46c9b70fb12",
                    "cacheVersn": 0,
                    "category": "Indicator Update"
                },
                {
                    "created": "2023-10-10T08:16:21.020022534Z",
                    "modified": "0001-01-01T00:00:00Z",
                    "user": "DBot",
                    "entryId": "",
                    "version": 0,
                    "content": "New relationship indicated-by created to Campaign: Indicator submission from incident 1189",
                    "type": "IndicatorCommentTimeLine",
                    "source": "TAXII2_CTIS_1 (TAXII 2 Feed)",
                    "id": "c759ddf2-38ca-4f9d-8f78-e815b7103de4",
                    "cacheVersn": 0,
                    "category": "Indicator Update"
                }
            ],
            "timestamp": "2023-10-09T23:31:28.590067524Z",
            "version": 41,
            "verdict": "Unknown",
            "source": "DBot",
            "id": "d1d2fc142d3076424f3c25d764b1cb32",
            "lastReputationRun": "2023-10-10T03:18:14.546562538Z",
            "lastSeenEntryID": "7bfa3aa3-c0b0-44de-86ee-136f63419d07@1194",
            "description": "n/a"
        }
    ]
    main(test_val)
