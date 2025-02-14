from netaddr import IPSet, IPNetwork
import ipaddress



def is_valid_cidr(cidr: str) -> bool:
    """
    Args:
        cidr: CIDR string
    Returns: True if the string represents an IPv4 network or an IPv6 network, false otherwise.
    """
    if '/' not in cidr:
        return False
    try:
        ipaddress.IPv4Network(cidr, strict=False)
        return True
    except ValueError:
        try:
            ipaddress.IPv6Network(cidr, strict=False)
            return True
        except ValueError:
            return False

def is_valid_ip(ip: str) -> bool:
    """
    Args:
        ip: IP address
    Returns: True if the string represents an IPv4 or an IPv6 address, false otherwise.
    """
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ValueError:
        try:
            ipaddress.IPv6Address(ip)
            return True
        except ValueError:
            return False

def ip_groups_to_cidrs(ip_range_groups):
    """Collapse ip groups list to CIDRs

    Args:
        ip_range_groups (Iterable): an Iterable of lists containing connected IPs

    Returns:
        Set. a set of CIDRs.
    """
    ip_ranges = set()
    for cidr in ip_range_groups:
        # handle single ips
        #if len(cidr) == 1:
        if "/32" in str(cidr) or "/128" in str(cidr):
            # CIDR with a single IP appears with "/32" or "/128" suffix so handle them differently
            ip_ranges.add(str(cidr[0]))
            continue
        ip_ranges.add(str(cidr))

    return ip_ranges


def ips_to_ranges(ips):
    invalid_ips = []
    valid_ips = []

    for ip_or_cidr in ips:
        if is_valid_cidr(ip_or_cidr) or is_valid_ip(ip_or_cidr):
            valid_ips.append(ip_or_cidr)
        else:
            invalid_ips.append(ip_or_cidr)

    cidrs = IPSet(valid_ips).iter_cidrs()
    
    collapsed_list = ip_groups_to_cidrs(cidrs)
    collapsed_list.update(invalid_ips)
    return collapsed_list
    
    
"""
with open('/Users/hnguyen/Google_Drive/XSOAR-Dev/local-dev/content/Packs/SlackCustomNew/Integrations/SlackV31/test_data/ipv4_list.txt', 'r') as f:
    data = f.read()
    original_ips_list4 = data.split("\n")

with open('/Users/hnguyen/Google_Drive/XSOAR-Dev/local-dev/content/Packs/SlackCustomNew/Integrations/SlackV31/test_data/ipv6_list.txt', 'r') as f:
    data = f.read()
    original_ips_list6 = data.split("\n")

original_ips_list = ['10.1.1.0/24','10.1.2.0/24','10.1.0.0/24','10.1.3.5/32']
ipv4_formatted_indicators = ips_to_ranges(original_ips_list4)

for indicator in ipv4_formatted_indicators:
     if ("/32" in indicator and ":" not in indicator) or ("/" not in indicator and ":" not in indicator):
        print(indicator)
"""

list1 = [1,2,3,4,5]
list2 = [1,2,6,7]

list3 = set(list1) - set(list2)
print(list3)