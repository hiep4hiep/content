## MS Defender Collector Help

MGet a list of incident objects that Microsoft 365 Defender created to track attacks in an organization.

Attacks are typically inflicted on different types of entities, such as devices, users, and mailboxes, resulting in multiple alert objects. Microsoft 365 Defender correlates alerts with the same attack techniques or the same attacker into an incident.

This operation allows you to filter and sort through incidents to create an informed cyber security response. It exposes a collection of incidents that were flagged in your network, within the time range you specified in your environment retention policy. The most recent incidents are displayed at the top of the list.

### Permissions

Application - SecurityIncident.Read.All

### Configuration
Provide the Client Credential Flow information:
- Tenant ID
- Client ID
- Client Secret