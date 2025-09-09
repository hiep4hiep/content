This is the Airlock event collector integration for XSIAM.

This is the default integration for this content pack when configured by the Data Onboarder in Cortex XSIAM.

## Configure Airlock Event Collector on Cortex XSOAR

1. Navigate to **Settings** > **Integrations** > **Servers & Services**.
2. Search for Airlock Event Collector.
3. Click **Add instance** to create and configure a new integration instance.

    | **Parameter** | **Required** |
    | --- | --- |
    | Server URL | True |
    | API Key | False |

4. Click **Test** to validate the URLs, token, and connection.

## Commands

You can execute these commands from the Cortex XSOAR CLI, as part of an automation, or in a playbook.
After you successfully execute a command, a DBot message appears in the War Room with the command details.

### airlock-get-events

***
Gets events from Airlock.

#### Base Command

airlock-get-events`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| should_push_events | If true, the command will create events, otherwise it will only display them. Possible values are: true, false. Default is false. | Required |
| status | Filter by alert status. Possible values are: ACTIVE, CLOSED. | Optional |
| limit | Maximum number of results to return. | Required |
| from_date | Date from which to get events. | Optional |

#### Context Output

There is no context output for this command.
