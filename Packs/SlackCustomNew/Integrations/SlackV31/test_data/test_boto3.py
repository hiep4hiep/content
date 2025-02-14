import ipaddress
ip = "2001:db8:85a3::8a2e:370:7334"
network = "2001:db8:85a3::/64"
test = ipaddress.ip_address(ip) in ipaddress.IPv6Network(network)
print(test)