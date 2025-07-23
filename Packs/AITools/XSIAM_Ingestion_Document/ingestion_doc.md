## Ingest network connection logs

Abstract

Cortex XSIAM can ingest network connection logs from different third-party sources.

You can ingest network connection logs from different third-party sources.

### Ingest network flow logs from Amazon S3

Abstract

Take advantage of Cortex XSIAM investigation capabilities and set up network flow log ingestion for your Amazon S3 logs using an AWS CloudFormation Script.

You can forward network flow logs to Cortex XSIAM from Amazon Simple Storage Service (Amazon S3).

To receive network flow logs from Amazon S3, you must first configure data collection from Amazon S3. You can then configure the Data Sources settings in Cortex XSIAM for Amazon S3. After you set up collection integration, Cortex XSIAM begins receiving new logs and data from the source.

You can either configure Amazon S3 with SQS notification manually on your own or use the AWS CloudFormation Script that we have created for you to make the process easier. The instructions below explain how to configure Cortex XSIAM to receive network flow logs from Amazon S3 using SQS. To perform these steps manually, see Configure Data Collection from Amazon S3 Manually.

For more information on configuring data collection from Amazon S3, see the Amazon S3 Documentation.

As soon as Cortex XSIAM begins receiving logs, the app automatically creates an Amazon S3 Cortex Query Language (XQL) dataset (`aws_s3_raw`). This enables you to search the logs with XQL Search using the dataset. For example, queries refer to the in-app XQL Library. For enhanced cloud protection, you can also configure Cortex XSIAM to ingest network flow logs as Cortex XSIAM network connection stories, which you can query with XQL Search using the `xdr_data` dataset with the preset called `network_story`. Cortex XSIAM can also raise Cortex XSIAM alerts (Analytics, Correlation Rules, IOC, and BIOC) when relevant from Amazon S3 logs. While Correlation Rules alerts are raised on non-normalized and normalized logs, Analytics, IOC, and BIOC alerts are only raised on normalized logs.

Enhanced cloud protection provides the following:

* Normalization of cloud logs  
* Cloud logs stitching  
* Enrichment with cloud data  
* Detection based on cloud analytics  
* Cloud-tailored investigations

Be sure you do the following tasks before you begin configuring data collection from Amazon S3 using the AWS CloudFormation Script.

* Ensure that you have the proper permissions to run AWS CloudFormation with the script provided in Cortex XSIAM. You need at a minimum the following permissions in AWS for an Amazon S3 bucket and Amazon Simple Queue Service (SQS):  
  * **Amazon S3 bucket**: `GetObject`  
  * **SQS**: `ChangeMessageVisibility`, `ReceiveMessage`, and `DeleteMessage`.  
* Ensure that you can access your Amazon Virtual Private Cloud (VPC) and have the necessary permissions to create flow logs.  
* Determine how you want to provide access to Cortex XSIAM to your logs and perform API operations. You have the following options:  
  * Designate an AWS IAM user, where you will need to know the Account ID for the user and have the relevant permissions to create an access key/id for the relevant IAM user. This is the default option as explained in Configure the Amazon S3 Collection in Cortex XSIAM by selecting Access Key.  
  * Create an assumed role in AWS to delegate permissions to a Cortex XSIAM AWS service. This role grants Cortex XSIAM access to your flow logs. For more information, see [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html). This is the Assumed Role option as described in the Configure the Amazon S3 collection in Cortex XSIAM. For more information on creating an assumed role for Cortex XSIAM, see [Create an assumed role](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-wPcVj~5r_xRuS_NmMalnOQ).  
* To collect Amazon S3 logs that use server-side encryption (SSE), the user role must have an IAM policy that states that Cortex XSIAM has kms:Decrypt permissions. With this permission, Amazon S3 automatically detects if a bucket is encrypted and decrypts it. If you want to collect encrypted logs from different accounts, you must have the decrypt permissions for the user role also in the key policy for the master account Key Management Service (KMS). For more information, see [Allowing users in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html).

Configure Cortex XSIAM to receive network flow logs from Amazon S3 using the CloudFormation Script.

1. Download the CloudFormation Script in Cortex XSIAM .  
   1. Select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select Amazon S3, and click Connect.  
   3. To provide access to Cortex XSIAM to your logs and to perform API operations using a designated AWS IAM user, leave the Access Key option selected. Otherwise, select Assumed Role, and ensure that you Create an Assumed Role for before continuing with these instructions.  
   4. For the Log Type, select Flow Logs to configure your log collection to receive network flow logs from Amazon S3, and the following text is displayed under the field Download CloudFormation Script. See instructions here.  
   5. Click the Download CloudFormation Script. link to download the script to your computer.  
2. Create a new Stack in the CloudFormation Console with the script you downloaded from Cortex XSIAM.  
   For more information on creating a Stack, see [Creating a stack on the AWS CloudFormation console](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-create-stack.html).  
   1. Log in to the [CloudFormation Console](https://console.aws.amazon.com/cloudformation/).  
   2. From the CloudFormation → Stacks page, ensure that you have selected the correct region for your configuration.  
   3. Select Create Stack → With new resources (standard).  
   4. Specify the template that you want AWS CloudFormation to use to create your stack. This template is the script that you downloaded from Cortex XSIAM , which will create an Amazon S3 bucket, Amazon Simple Queue Service (SQS) queue, and Queue Policy. Configure the following settings in the Specify template page.  
      * Prerequisite \- Prepare template → Prepare template: Select Template is ready.  
      * Specify Template  
        * Template source: Select Upload a template file.  
        * Upload a template file: Choose file, and select the `cortex-xdr-create-s3-with-sqs-flow-logs.json` file that you downloaded from Cortex XDR.  
          ![create-stack.png][image2]  
   5. Click Next.  
   6. In the Specify stack details page, configure the following stack details.  
      * Stack name: Specify a descriptive name for your stack.  
      * Parameters → Cortex XDR Flow Logs Integration  
        * Bucket Name: Specify the name of the S3 bucket to create, where you can leave the default populated name as xdr-flow-logs or create a new one. The name must be unique.  
        * Publisher Account ID: Specify the AWS IAM user account ID with whom you are sharing access.  
        * Queue Name: Specify the name for your Amazon SQS queue to create, where you can leave the default populated name as xdr-flow or create a new one. The name must be unique.  
          ![specify-stack-details.png][image3]  
   7. Click Next.  
   8. In the Configure stack options page, there is nothing to configure, so click Next.  
   9. In the Review page, look over the stack configurations settings that you have configured and if they are correct, click Create stack. If you need to make a change, click Edit beside the particular step that you want to update.  
      The stack is created and is opened with the Events tab displayed. It can take a few minutes for the new Amazon S3 bucket, SQS queue, and Queue Policy to be created. Click Refresh to get updates. Once everything is created, leave the stack opened in the current browser, because you will need to access information in the stack for other steps detailed below.  
      For the Amazon S3 bucket created using CloudFormation, it is the customer’s responsibility to define a retention policy by creating a Lifecycle rule in the Management tab. We recommend setting the retention policy to at least 7 days to ensure that the data is retrieved under all circumstances.  
3. Configure your Amazon Virtual Private Cloud (VPC) with flow logs:  
   1. Open the [Amazon VPC Console](https://console.aws.amazon.com/vpc/), and in the Resources by Region listed, select VPCs to view the VPCs configured for the current region selected. To select another VPC from another region, select See all regions, and select one of them.  
      To create a new VPC, click Launch VPC Wizard. For more information, see [AWS VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html).  
   2. From the list of Your VPCs, select the checkbox beside the VPC that you want to configure to create flow logs, and then select Actions → Create flow log.  
      ![your-vpcs.png][image4]  
   3. Configure the following Flow log settings:  
      * Name \- optional: (Optional) Specify a descriptive name for your VPC flow log.  
      * Filter: Select All types of traffic to capture.  
      * Maximum aggregation interval: If you anticipate a heavy flow of traffic, select 1 minute. Otherwise, leave the default setting as 10 minutes.  
      * Destination: Select Send to an Amazon S3 bucket as the destination to publish the flow log data.  
      * S3 bucket ARN:Specify the Amazon Resource Name (ARN) for your Amazon S3 bucket.  
        You can retrieve your bucket’s ARN by opening another instance of the AWS Management Console in a browser window and opening the [Amazon S3 console](https://console.aws.amazon.com/s3/). In the Buckets section, select the bucket that you created for collecting the Amazon S3 flow logs when you created your stack, click Copy ARN, and paste the ARN in this field.  
        ![bucket-copy-arn.png][image5]  
      * Log record format: Select Custom Format, and in the Log Format field, specify the following fields to include in the flow log record, which you can select from the list displayed:  
        * account-id  
        * action  
        * az-id  
        * bytes  
        * dstaddr  
        * dstport  
        * end  
        * flow-direction  
        * instance-id  
        * interface-id  
        * packets  
        * log-status  
        * pkt-srcaddr  
        * pkt-dstaddr  
        * protocol  
        * region  
        * srcaddr  
        * srcport  
        * start  
        * sublocation-id  
        * sublocation-type  
        * subnet-id  
        * tcp-flags  
        * type  
        * vpc-id  
        * version  
   4. Click Create flow log.  
      Once the flow log is created, a message indicating that the flow log was successfully created is displayed at the top of the Your VPCs page.  
      In addition, if you open your Amazon S3 bucket configurations, by selecting the bucket from the [Amazon S3 console](https://console.aws.amazon.com/s3/), the Objects tab contains a folder called `AWSLogs/` to collect the flow logs.  
4. Configure access keys for the AWS IAM user that Cortex XSIAM uses for API operations.  
   1. It is the responsibility of the customer’s organization to ensure that the user who performs this task of creating the access key is designated with the relevant permissions. Otherwise, this can cause the process to fail with errors.  
   2. Skip this step if you are using an Assumed Role for Cortex XSIAM.  
   3. Open the [AWS IAM Console](https://console.aws.amazon.com/iam/), and in the navigation pane, select Access management → Users.  
   4. Select the User name of the AWS IAM user.  
   5. Select the Security credentials tab, scroll down to the Access keys section, and click Create access key.  
   6. Click the copy icon next to the Access key ID and Secret access key keys, where you must click Show secret access key to see the secret key and record them somewhere safe before closing the window. You will need to provide these keys when you edit the Access policy of the SQS queue and when setting the AWS Client ID and AWS Client Secret in Cortex XSIAM. If you forget to record the keys and close the window, you will need to generate new keys and repeat this process.  
5. For more information, see [Managing access keys for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).  
6. When you create an Assumed Role in Cortex XSIAM, ensure that you edit the policy that defines the permissions for the role with the S3 Bucket ARN and SQS ARN, which is taken from the Stack you created.  
   Skip this step if you are using an Access Key to provide access to Cortex XSIAM.  
7. Configure the Amazon S3 collection in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. In the Amazon S3 configuration, click Add Instance to begin a new configuration.  
   3. Set these parameters, where the parameters change depending on whether you configured an Access Key or Assumed Role.  
      * SQS URL: Specify the SQS URL, which is taken from the stack you created. In the browser you left open after creating the stack, open the Outputs tab, copy the Value of the QueueURL and paste it in this field.  
      * Name: Specify a descriptive name for your log collection configuration.  
      * When setting an Access Key, set these parameters.  
        * AWS Client ID: Specify the Access key ID, which you received when you created access keys for the AWS IAM user in AWS.  
        * AWS Client Secret: Specify the Secret access key you received when you created access keys for the AWS IAM user in AWS.  
      * When setting an Assumed Role, set these parameters.  
        * Role ARN: Specify the Role ARN for the Assumed Role you created for in AWS.  
        * External Id:Specify the External Id for the Assumed Role you created for in AWS.  
      * Log Type: Select Flow Logs to configure your log collection to receive network flow logs from Amazon S3. When configuring network flow log collection, the following additional field is displayed for Enhanced Cloud Protection.  
        You can Normalize and enrich flow logs by selecting the checkbox. If selected, Cortex XSIAM ingests the network flow logs as XDR network connection stories, which you can query using XQL Search from the `xdr_data` dataset using the preset called `network_story`.  
   4. Click Test to validate access, and then click Enable.  
      Once events start to come in, a green check mark appears underneath the Amazon S3 configuration with the number of logs received.

#### Create an assumed role

Abstract

Learn about creating an AWS Assumed Role for Cortex XSIAM.

If you do not designate a separate AWS IAM user to provide access to Cortex XSIAM to your logs and to perform API operations, you can create an assumed role in AWS to delegate permissions to a Cortex XSIAM AWS service. This role grants Cortex XSIAM access to your logs. For more information, see [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).

When setting up any type of Amazon S3 Collector in Cortex XSIAM, these instructions explain setting up an Assumed Role.

1. Log in to the AWS Management Console to create a role for Cortex XSIAM.  
   Refer to the [AWS instructions](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html) for guidance.  
   * Create the role in the same region as your AWS account, and use the following values and options when creating the role.  
     * Type of Trusted → Another AWS Account, and specify the Account ID as `006742885340`. When using a Cortex XSIAM FedRAMP environment, specify the Account ID as `685269782068`.  
     * Select Options for the Require external ID, which is a unique alphanumeric string, and generate a secure UUIDv4 using an [Online UUID Generator](https://www.uuidgenerator.net/version4). Copy the External ID as you will use this when configuring the Amazon S3 Collector in Cortex XSIAM .  
       In AWS this is an optional field to configure, but this must be configured to set up the Amazon S3 Collector in Cortex XSIAM .  
     * Do not enable MFA. Verify that Require MFA is not selected.  
   * ![create-a-role-assumed-role.png][image6]  
   * Click Next and add the AWS Managed Policy for Security Audit.  
     ![create-a-role-security-audit.png][image7]  
     Then, add a role name and create the role. In this workflow, later, you will create the granular policies and edit the role to attach the additional policies.  
2. Create the policy that defines the permissions for the Cortex XSIAM role.  
   * Select IAM on the AWS Management Console.  
   * In the navigation pane on the left, select Access Management → Policies → Create Policy.

Select the JSON tab.  
Copy the following JSON policy and paste it within the editor window.  
The **`<s3-arn>`** and **`<sqs-arn>`** placeholders. These will be filled out later depending on which Amazon S3 logs you are configuring, including network flow logs, audit logs, or generic logs.  
{  
    "Version": "2012-10-17",  
    "Statement": \[  
        {  
            "Effect": "Allow",  
            "Action": "s3:GetObject",  
            "Resource": "\<s3-arn\>/\*"  
        },  
        {  
            "Effect": "Allow",  
             "Action": \[  
                "sqs:ReceiveMessage",  
                "sqs:DeleteMessage",  
                "sqs:ChangeMessageVisibility"  
            \],  
            "Resource": "\<sqs-arn\>"  
        }  
    \]

* }  
  * Review and create the policy.  
3. Edit the role you created in Step 1 and attach the policy to the role.  
4. Copy the Role ARN.  
   ![arn-assumed-role.png][image8]  
5. Continue with the task for the applicable Amazon S3 logs you want to configure.  
   The following type of logs are available.  
   * [Ingest network flow logs from Amazon S3](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-qKFK6yq1eVkew5N~bvw1uQ).  
   * [Ingest Network Route 53 Logs from Amazon S3](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-DfGZMD~U12PiGvZ9m2ukcw)  
   * [Ingest audit logs from AWS Cloud Trail](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-UrS7g7kH8TkS1D7qXJmSfg).  
   * [Ingest generic logs from Amazon S3](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-7GfGi4BtWsa7fe23UhBbMQ).

#### Configure data collection from Amazon S3 manually

Abstract

Set up network flow log ingestion for your Amazon S3 logs manually (without a script).

There are various reasons why you may need to configure data collection from Amazon S3 manually, as opposed to using the CloudFormation Script provided in Cortex XSIAM. For example, if your organization does not use CloudFormation scripts, you will need to follow the instructions below, which explain at a high-level how to perform these steps manually with a link to the relevant topic in the Amazon S3 documentation with the detailed steps to follow.

As soon as Cortex XSIAM begins receiving logs, the app automatically creates an Amazon S3 Cortex Query Language (XQL) dataset (`aws_s3_raw`). This enables you to search the logs with XQL Search using the dataset. For example queries, refer to the in-app XQL Library. For enhanced cloud protection, you can also configure Cortex XSIAM to ingest network flow logs as Cortex XSIAM network connection stories, which you can query with XQL Search using the `xdr_dataset` dataset with the preset called `network_story`. Cortex XSIAM can also raise Cortex XSIAM alerts (Analytics, Correlations, IOC, and BIOC) when relevant from Amazon S3 logs. While Correlation Rules alerts are raised on non-normalized and normalized logs, Analytics, IOC, and BIOC alerts are only raised on normalized logs.

Enhanced cloud protection provides:

* Normalization of cloud logs  
* Cloud logs stitching  
* Enrichment with cloud data  
* Detection based on cloud analytics  
* Cloud-tailored investigations

Be sure you do the following tasks before you begin configuring data collection manually from Amazon CloudWatch to Amazon S3.

If you already have an Amazon S3 bucket configured with VPC flow logs that you want to use for this configuration, you do not need to perform the prerequisite steps detailed in the first two bullets.

* Ensure that you have at a minimum the following permissions in AWS for an Amazon S3 bucket and Amazon Simple Queue Service (SQS).  
  * **Amazon S3 bucket**: `GetObject`  
  * **SQS**: `ChangeMessageVisibility`, `ReceiveMessage`, and `DeleteMessage`.  
* Create a dedicated Amazon S3 bucket for collecting network flow logs with the default settings. For more information, see [Creating a bucket using the Amazon S3 Console](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html).  
  It is your responsibility to define a retention policy for your Amazon S3 bucket by creating a Lifecycle rule in the Management tab. We recommend setting the retention policy to at least 7 days to ensure that the data is retrieved under all circumstances.  
* Ensure that you can access your Amazon Virtual Private Cloud (VPC) and have the necessary permissions to create flow logs.  
* Determine how you want to provide access to Cortex XSIAM to your logs and perform API operations. You have the following options.  
  * Designate an AWS IAM user, where you will need to know the Account ID for the user and have the relevant permissions to create an access key/id for the relevant IAM user. This is the default option as explained in Configure the Amazon S3 collection by selecting Access Key.  
  * Create an assumed role in AWS to delegate permissions to a Cortex XSIAM AWS service. This role grants Cortex XSIAM access to your flow logs. For more information, see [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html). This is the Assumed Role option as described in the Configure the Amazon S3 collection. For more information on creating an assumed role for Cortex XSIAM , see [Create an assumed role](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-wPcVj~5r_xRuS_NmMalnOQ).  
* To collect Amazon S3 logs that use server-side encryption (SSE), the user role must have an IAM policy that states that Cortex XSIAM has kms:Decrypt permissions. With this permission, Amazon S3 automatically detects if a bucket is encrypted and decrypts it. If you want to collect encrypted logs from different accounts, you must have the decrypt permissions for the user role also in the key policy for the master account Key Management Service (KMS). For more information, see [Allowing users in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html).

Configure Cortex XSIAM to receive network flow logs from Amazon S3 manually.

1. Log in to the [AWS Management Console](https://console.aws.amazon.com/).  
2. From the menu bar, ensure that you have selected the correct region for your configuration.  
3. Configure your Amazon Virtual Private Cloud (VPC) with flow logs. For more information, see [AWS VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html).  
   If you already have an Amazon S3 bucket configured with VPC flow logs, skip this step and go to Configure an Amazon Simple Queue Service (SQS).  
4. Configure an Amazon Simple Queue Service (SQS). For more information, see [Configuring Amazon SQS queues (console)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configuring.html).  
   Ensure that you create your Amazon S3 bucket and Amazon SQS queue in the same region.  
5. Configure an event notification to your Amazon SQS whenever a file is written to your Amazon S3 bucket. For more information, see [Amazon S3 Event Notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/NotificationHowTo.html).  
6. Configure access keys for the AWS IAM user that Cortex XSIAM uses for API operations. For more information, see [Managing access keys for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).  
   1. It is the responsibility of the customer’s organization to ensure that the user who performs this task of creating the access key is designated with the relevant permissions. Otherwise, this can cause the process to fail with errors.  
   2. Skip this step if you are using an Assumed Role for Cortex XSIAM.  
7. Update the Access Policy of your SQS queue and grant the required permissions mentioned above to the relevant IAM user. For more information, see [Granting permissions to publish event notification messages to a destination](https://docs.aws.amazon.com/AmazonS3/latest/userguide/grant-destinations-permissions-to-s3.html).  
   Skip this step if you are using an Assumed Role for Cortex XSIAM.  
8. Configure the Amazon S3 collection in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select Amazon S3, and click Connect.  
   3. Set these parameters, where the parameters change depending on whether you configured an Access Key or Assumed Role.  
      * To provide access to Cortex XSIAM to your logs and perform API operations using a designated AWS IAM user, leave the Access Key option selected. Otherwise, select Assumed Role, and ensure that you Create an Assumed Role for Cortex XSIAM before continuing with these instructions. In addition, when you create an Assumed Role for Cortex XSIAM, ensure that you edit the policy that defines the permissions for the role with the Amazon S3 Bucket ARN and SQS ARN.  
      * SQS URL: Specify the SQS URL, which is the ARN of the Amazon SQS that you configured in the AWS Management Console. For more information on how to retrieve your Amazon SQS ARN, see the Specify SQS queue field when you configure an event notification to your Amazon SQS whenever a file is written to your Amazon S3 bucket.  
      * Name: Specify a descriptive name for your log collection configuration.  
      * When setting an Access Key, set these parameters.  
        * AWS Client ID: Specify the Access key ID, which you received when you created access keys for the AWS IAM user in AWS.  
        * AWS Client Secret: Specify the Secret access key you received when you created access keys for the AWS IAM user in AWS.  
      * When setting an Assumed Role, set these parameters.  
        * Role ARN: Specify the Role ARN for the Assumed Role for Cortex XSIAM in AWS.  
        * External Id: Specify the External Id for the Assumed Role for Cortex XSIAM in AWS.  
      * Log Type: Select Flow Logs to configure your log collection to receive network flow logs from Amazon S3. When configuring network flow log collection, the following additional field is displayed for Enhanced Cloud Protection.  
        You can Normalize and enrich flow logs by selecting the checkbox. When selected, Cortex XSIAM ingests the network flow logs as Cortex XSIAM network connection stories, which you can query using XQL Search from the `xdr_dataset` dataset using the preset called `network_story`.  
   4. Click Test to validate access, and then click Enable.  
      Once events start to come in, a green check mark appears underneath the Amazon S3 configuration with the number of logs received.

### Ingest Network Route 53 Logs from Amazon S3

Abstract

Take advantage of Cortex XSIAM investigation capabilities and set up network Route 53 ingestion for your Amazon S3 logs using an AWS CloudFormation Script.

You can forward network AWS Route 53 DNS logs to Cortex XSIAM from Amazon Simple Storage Service (Amazon S3).

To receive network Route 53 DNS logs from Amazon S3, you must first configure data collection from Amazon S3. You can then configure the Collection Integrations settings in Cortex XSIAM for Amazon S3. After you set up collection integration, Cortex XSIAM begins receiving new logs and data from the source.

You can configure Amazon S3 with SQS notification using the AWS CloudFormation Script that we have created for you to make the process easier. The instructions below explain how to configure Cortex XSIAM to receive network Route 53 DNS logs from Amazon S3 using SQS.

For more information on configuring data collection from Amazon S3 for Route 53 DNS logs, see the [AWS Documentation](https://aws.amazon.com/blogs/aws/log-your-vpc-dns-queries-with-route-53-resolver-query-logs/).

As soon as Cortex XSIAM begins receiving logs, the app automatically creates an Amazon Route 53 Cortex Query Language (XQL) dataset (`amazon_route53_raw`). This enables you to search the logs with XQL Search using the dataset. For example, queries refer to the in-app XQL Library. For enhanced cloud protection, you can also configure Cortex XSIAM to ingest network Route 53 DNS logs as Cortex XSIAM network connection stories, which you can query with XQL Search using the `xdr_data` dataset with the preset called `network_story`. Cortex XSIAM can also raise Cortex XSIAM alerts (Analytics, Correlation Rules, IOC, and BIOC) when relevant from Amazon Route 53 DNS logs. While Correlation Rules alerts are raised on non-normalized and normalized logs, Analytics, IOC, and BIOC alerts are only raised on normalized logs.

Enhanced cloud protection provides:

* Normalization of cloud logs  
* Cloud logs stitching  
* Enrichment with cloud data  
* Detection based on cloud analytics  
* Cloud-tailored investigations

Be sure you do the following tasks before you begin configuring data collection from Amazon S3 using the AWS CloudFormation Script.

* Ensure that you have the proper permissions to run AWS CloudFormation with the script provided in Cortex XSIAM. You need at a minimum the following permissions in AWS for an Amazon S3 bucket and Amazon Simple Queue Service (SQS):  
  * **Amazon S3 bucket**: `GetObject`  
  * **SQS**: `ChangeMessageVisibility`, `ReceiveMessage`, and `DeleteMessage`.  
* Ensure that you can access your Amazon Virtual Private Cloud (VPC) and have the necessary permissions to create Route 53 Resolver Query logs.  
* Determine how you want to provide access to Cortex XSIAM to your logs and perform API operations. You have the following options.  
  * Designate an AWS IAM user, where you will need to know the Account ID for the user and have the relevant permissions to create an access key/id for the relevant IAM user. This is the default option when you configure the Amazon S3 collection by selecting Access Key.  
  * Create an assumed role in AWS to delegate permissions to a Cortex XSIAM AWS service. This role grants Cortex XSIAM access to your flow logs. For more information, see [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html). This is the Assumed Role option when you configure the Amazon S3 collection in Cortex XSIAM. For more information on creating an assumed role for Cortex XSIAM, see [Create an assumed role](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-wPcVj~5r_xRuS_NmMalnOQ).  
* To collect Amazon S3 logs that use server-side encryption (SSE), the user role must have an IAM policy that states that Cortex XSIAM has kms:Decrypt permissions. With this permission, Amazon S3 automatically detects if a bucket is encrypted and decrypts it. If you want to collect encrypted logs from different accounts, you must have the decrypt permissions for the user role also in the key policy for the master account Key Management Service (KMS). For more information, see [Allowing users in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html).

Configure Cortex XSIAM to receive network Route 53 DNS logs from Amazon S3 using the CloudFormation Script.

1. Download the CloudFormation Script in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select Amazon S3, and click Connect.  
   3. To provide access to Cortex XSIAM to your logs and to perform API operations using a designated AWS IAM user, leave the Access Key option selected. Otherwise, select Assumed Role, and ensure that you Create an Assumed Role for before continuing with these instructions.  
   4. For the Log Type, select Route 53 to configure your log collection to receive network Route 53 DNS logs from Amazon S3, and the following text is displayed under the field Download CloudFormation Script. See instructions here.  
   5. Click the Download CloudFormation Script. link to download the script to your computer.  
2. Create a new Stack in the CloudFormation Console with the script you downloaded from Cortex XSIAM.  
   For more information on creating a Stack, see [Creating a stack on the AWS CloudFormation console](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-create-stack.html).  
   1. Log in to the [CloudFormation Console](https://console.aws.amazon.com/cloudformation/).  
   2. From the CloudFormation → Stacks page, ensure that you have selected the correct region for your configuration.  
   3. Select Create Slack → With new resources (standard).  
   4. Specify the template that you want AWS CloudFormation to use to create your stack. This template is the script that you downloaded from Cortex XSIAM , which will create an Amazon S3 bucket, Amazon Simple Queue Service (SQS) queue, and Queue Policy. Configure the following settings in the Specify template page.  
      * Prerequisite \- Prepare template → Prepare template: Select Template is ready.  
      * Specify Template  
        * Template source: Select Upload a template file.  
        * Upload a template file: Choose file, and select the `CloudFormation-Script.json` file that you downloaded.  
   5. Click Next.  
   6. In the Specify stack details page, configure the following stack details.  
      * Stack name: Specify a descriptive name for your stack.  
      * Parameters → Cortex XDR Flow Logs Integration  
        * Bucket Name: Specify the name of the S3 bucket to create, where you can leave the default populated name as xdr-route53-logs or create a new one. The name must be unique.  
        * Publisher Account ID: Specify the AWS IAM user account ID with whom you are sharing access.  
        * Queue Name: Specify the name for your Amazon SQS queue to create, where you can leave the default populated name as xdr-route53 or create a new one. The name must be unique.  
   7. Click Next.  
   8. In the Configure stack options page, there is nothing to configure, so click Next.  
   9. In the Review page, look over the stack configurations settings that you have configured and if they are correct, click Create stack. If you need to make a change, click Edit beside the particular step that you want to update.  
      The stack is created and is opened with the Events tab displayed. It can take a few minutes for the new Amazon S3 bucket, SQS queue, and Queue Policy to be created. Click Refresh to get updates. Once everything is created, leave the stack opened in the current browser as you will need to access information in the stack for other steps detailed below.  
      For the Amazon S3 bucket created using CloudFormation, it is the customer’s responsibility to define a retention policy by creating a Lifecycle rule in the Management tab. We recommend setting the retention policy to at least 7 days to ensure that the data is retrieved under all circumstances.  
3. Configure Route 53 Query Logging in AWS.  
   1. Log in to the [AWS Management Console](https://console.aws.amazon.com/).  
   2. From the menu bar, ensure that you have selected the correct region for your configuration.  
   3. Search for Route 53 and select Resolver → Query Logging.  
   4. Configure query logging.  
   5. Set the following parameters in the different sections on the Configure query logging page.  
      * Query logging configuration name  
        * Name: Specify a name for your Resolver query logging configuration.  
      * Query logs destination  
        * Destination for query logs: Select S3 bucket as the place where you want Resolver to publish query logs.  
        * Amazon S3 bucket: Browse S3 to select the Amazon S3 bucket created after running the CloudFormation script, which is by default called xdr-route53-logs or select the one that you created.  
      * VPCs to log queries for  
        * Add VPC: Clicking the Add VPC button opens the Add VPC page, where you can choose the VPCs that you want to log queries for. When you are done, click Add.  
   6. Click Configure query logging.  
4. Configure access keys for the AWS IAM user that Cortex XSIAM uses for API operations.  
   1. It is the responsibility of the customer’s organization to ensure that the user who performs this task of creating the access key is designated with the relevant permissions. Otherwise, this can cause the process to fail with errors.  
   2. Skip this step if you are using an Assumed Role for Cortex XSIAM.  
   3. Open the [AWS IAM Console](https://console.aws.amazon.com/iam/), and in the navigation pane, select Access management → Users.  
   4. Select the User name of the AWS IAM user.  
   5. Select the Security credentials tab, scroll down to the Access keys section, and click Create access key.  
   6. Click the copy icon next to the Access key ID and Secret access key keys, where you must click Show secret access key to see the secret key and record them somewhere safe before closing the window. You will need to provide these keys when you edit the Access policy of the SQS queue and when setting the AWS Client ID and AWS Client Secret in Cortex XSIAM. If you forget to record the keys and close the window, you will need to generate new keys and repeat this process.  
      For more information, see [Managing access keys for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).  
5. When you create an Assumed Role, ensure that you edit the policy that defines the permissions for the role with the S3 Bucket ARN and SQS ARN, which is taken from the stack you created.  
   Skip this step if you are using an Access Key to provide access to Cortex XSIAM.  
6. Configure the Amazon S3 collection in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. In the Amazon S3 configuration, click Add Instance to begin a new configuration.  
   3. Set these parameters, where the parameters change depending on whether you configured an Access Key or Assumed Role.  
      * SQS URL: Specify the SQS URL, which is taken from the stack you created. In the browser you left open after creating the stack, open the Outputs tab, copy the Value of the QueueURL and paste it in this field.  
      * Name: Specify a descriptive name for your log collection configuration.  
      * When setting an Access Key, set these parameters.  
        * AWS Client ID: Specify the Access key ID, which you received when you created access keys for the AWS IAM user in AWS.  
        * AWS Client Secret: Specify the Secret access key you received when you created access keys for the AWS IAM user in AWS.  
      * When setting an Assumed Role, set these parameters.  
        * Role ARN: Specify the Role ARN for the Assumed Role you created for Cortex XSIAMin AWS.  
        * External Id: Specify the External Id for the Assumed Role you created for Cortex XSIAM in AWS.  
      * Log Type: Select Route 53 to configure your log collection to receive network Route 53 DNS logs from Amazon S3. When configuring network Route 53 log collection, the following additional field is displayed for Enhanced Cloud Protection.  
        You can Normalize DNS logs by selecting the checkbox (default configuration). When selected, Cortex XSIAM ingests the network Route 53 DNS logs as XDR network connection stories, which you can query using XQL Search from the `xdr_data` dataset using the preset called `network_story`.  
   4. Click Test to validate access, and then click Enable.  
      Once events start to come in, a green check mark appears underneath the Amazon S3 configuration with the number of logs received.

### Ingest logs from Check Point firewalls

Abstract

To take advantage of Cortex XSIAM investigation and detection capabilities while using Check Point firewalls, forward your firewall logs to Cortex XSIAM.

If you use Check Point FW1/VPN1 firewalls, you can still take advantage of Cortex XSIAM investigation and detection capabilities by forwarding your Check Point firewall logs to Cortex XSIAM. Check Point firewall logs can be used as the sole data source, however, you can also use Check Point firewall logs in conjunction with Palo Alto Networks firewall logs and additional data sources.

Cortex XSIAM can stitch data from Check Point firewalls with other logs to make up network stories searchable in the Query Builder and in Cortex Query Language (XQL) queries. Cortex XSIAM can also return raw data from Check Point firewalls in XQL queries.

* Logs with `sessionid = 0` are dropped.  
* Destination Port data is available only in the raw logs.

In terms of alerts, Cortex XSIAM can both surface native Check Point firewall alerts and raise its own alerts on network activity. Alerts are displayed throughout Cortex XSIAM alert, incident, and investigation views.

To integrate your logs, you first need to set up an applet in a Broker VM within your network to act as a Syslog Collector. You then configure your Check Point firewall policy to log all traffic and set up the Log Exporter on your Check Point Log Server to forward logs to the Syslog Collector in a CEF format.

As soon as Cortex XSIAM starts to receive logs, the app can begin stitching network connection logs with other logs to form network stories. Cortex XSIAM can also analyze your logs to raise Analytics alerts and can apply IOC, BIOC, and Correlation Rule matching. You can also use queries to search your network connection logs.

1. Ensure that your Check Point firewalls meet the following requirements.  
   Check Point software version: R77.30, R80.10, R80.20, R80.30, or R80.40  
2. Increase log storage for Check Point firewall logs.  
   As an estimate for initial sizing, note that the average Check Point log size is roughly 700 bytes. For proper sizing calculations, test the log sizes and log rates produced by your Check Point firewalls. For more information, see Manage Your Log Storage within Cortex XSIAM.  
3. Activate the Syslog Collector.  
4. Configure the Check Point firewall to forward Syslog events in CEF format to the Syslog Collector.  
   Configure your firewall policy to log all traffic and set up the Log Exporter to forward logs to the Syslog Collector. For more information on setting up Log Exporter, see the Check Point documentation.

### Ingest logs from Cisco ASA firewalls and AnyConnect

Abstract

Extend Cortex XSIAM visibility into logs from Cisco ASA firewalls and Cisco AnyConnect VPN.

If you use Cisco ASA firewalls or Cisco AnyConnect VPN, you can take advantage of Cortex XSIAM investigation and detection capabilities by forwarding your firewall and AnyConnect VPN logs to Cortex XSIAM. This enables Cortex XSIAM to examine your network traffic to detect anomalous behavior. Cortex XSIAM can use Cisco ASA firewall logs and AnyConnect VPN logs as the sole data source, but can also use Cisco ASA firewall logs in conjunction with Palo Alto Networks firewall logs. For additional endpoint context, you can also use Cortex XSIAM to collect and alert on endpoint data.

As soon as Cortex XSIAM starts to receive logs, the app can begin stitching network connection logs with other logs to form network stories. Cortex XSIAM can also analyze your logs to raise Analytics alerts and can apply IOC, BIOC, and Correlation Rules matching. You can also use queries to search your network connection logs using the Cisco Cortex Query Language (XQL) dataset (`cisco_asa_raw`).

To integrate your logs, you first need to set up an applet in a Broker VM within your network to act as a Syslog Collector. You then configure forwarding on your log devices to send logs to the Syslog Collector in a CISCO format.

1. Verify that your Cisco ASA firewall and Cisco AnyConnect VPN logs meet the following requirements.  
   * Syslog in Cisco-ASA format  
   * Must include `timestamps`  
   * Only supports the following messages.  
     * For Cisco ASA firewall: 302013, 302014, 302015, 302016  
     * For Cisco AnyConnect VPN: 113039, 716001, 722022, 722033, 722034, 722051, 722055, 722053, 113019, 716002, 722023, 722037  
2. Activate the Syslog Collector.  
3. Increase log storage for Cisco ASA firewall and Cisco AnyConnect VPN logs.  
   As an estimate for initial sizing, note that the average Cisco ASA log size is roughly 180 bytes. For proper sizing calculations, test the log sizes and log rates produced by your Cisco ASA firewalls and Cisco AnyConnect VPN logs. For more information, see Manage Your Log Storage within Cortex XSIAM.  
4. Configure the Cisco ASA firewall and Cisco AnyConnect VPN, or the log devices forwarding logs from Cisco, to log to the Syslog Collector in a CISCO format.  
   Configure your firewall and AnyConnect VPN policies to log all traffic and forward the traffic logs to the Syslog Collector in a CISCO format. By logging all traffic, you enable Cortex XSIAM to detect anomalous behavior from Cisco ASA firewall logs and Cisco AnyConnect VPN logs. For more information on setting up Log Forwarding on Cisco ASA firewalls or Cisco AnyConnect VPN, see the Cisco ASA Series documentation.

### Ingest logs from Corelight Zeek

Abstract

Extend Cortex XSIAM visibility into logs from Corelight Zeek.

If you use Corelight Zeek sensors for network monitoring, you can still take advantage of Cortex XSIAM investigation and detection capabilities by forwarding your network connection logs to Cortex XSIAM . This enables Cortex XSIAM to examine your network traffic to detect anomalous behavior. Cortex XSIAM can use Corelight Zeek logs as the sole data source, but can also use logs in conjunction with Palo Alto Networks or third-party firewall logs. For additional endpoint context, you can also use Cortex XSIAM to collect and alert on endpoint data.

As soon as Cortex XSIAM starts to receive logs, the app can begin stitching network connection logs with other logs to form network stories. Cortex XSIAM can also analyze your logs to raise Analytics alerts and can apply IOC, BIOC, and Correlation Rule matching. You can also use queries to search your network connection logs.

To integrate your logs, you first need to set up an applet in a Broker VM within your network to act as a Syslog Collector. You then configure forwarding on your Corelight Zeek sensors (using the default Syslog export option of RFC5424 over TCP) to send logs to the Syslog Collector.

1. Activate the Syslog Collector.  
   During activation, you define the Listening Port over which you want the Syslog Collector to receive logs. You must also set TCP as the transport Protocol and Corelight as the Syslog Format.  
2. Increase log storage for Corelight Zeek logs.  
   For proper sizing calculations, test the log sizes and log rates produced by your Corelight Zeek Sensors. Then adjust your Cortex XSIAM log storage. For more information, see Manage Your Log Storage within Cortex XSIAM.  
3. Forward logs to the Syslog Collector.  
   Cortex XSIAM can receive logs from Corelight Zeek sensors that use the Syslog export option of RFC5424 over TCP.  
   1. In the Syslog configuration of Corelight Zeek (Sensor → Export), specify the details for your Syslog Collector including the hostname or IP address of the Broker VM and corresponding listening port that you defined during activation of the Syslog Collector, default Syslog format (RFC5424), and any log exclusions or filters.  
   2. Save your Syslog configuration to apply the configuration to your Corelight Zeek Sensors.  
4. For full setup instructions, see the Corelight Zeek documentation.

### Ingest logs from Fortinet Fortigate firewalls

Abstract

Extend Cortex XSIAM visibility into logs from Fortinet Fortigate firewalls.

If you use Fortinet Fortigate firewalls, you can still take advantage of Cortex XSIAM investigation and detection capabilities by forwarding your firewall logs to Cortex XSIAM . This enables Cortex XSIAM to examine your network traffic to detect anomalous behavior. Cortex XSIAM can use Fortinet Fortigate firewall logs as the sole data source, but can also use Fortinet Fortigate firewall logs in conjunction with Palo Alto Networks firewall logs. For additional endpoint context, you can also use Cortex XSIAM to collect and alert on endpoint data.

As soon as Cortex XSIAM starts to receive logs, the app can begin stitching network connection logs with other logs to form network stories. Cortex XSIAM can also analyze your logs to raise Analytics alerts and can apply IOC, BIOC, and Correlation Rule matching. You can also use queries to search your network connection logs.

To integrate your logs, you first need to set up an applet in a Broker VM within your network to act as a Syslog collector. You then configure forwarding on your log devices to send logs to the Syslog collector in a CEF format.

1. Verify that your Fortinet Fortigate firewalls meet the following requirements.  
   * Must use FortiOS 6.2.1 or a later release  
   * `timestamp` must be in nanoseconds  
2. Activate the Syslog Collector.  
3. Increase log storage for Fortinet Fortigate firewall logs.  
   As an estimate for initial sizing, note that the average Fortinet Fortigate log size is roughly 1,070 bytes. For proper sizing calculations, test the log sizes and log rates produced by your Fortinet Fortigate firewalls. For more information, see Manage Your Log Storage within Cortex XSIAM.  
4. Configure the log device that receives Fortinet Fortigate firewall logs to forward Syslog events to the Syslog collector in a CEF format.  
   Configure your firewall policy to log all traffic and forward the traffic logs to the Syslog collector in a CEF format. By logging all traffic, you enable Cortex XSIAM to detect anomalous behavior from Fortinet Fortigate firewall logs. For more information on setting up Log Forwarding on Fortinet Fortigate firewalls, see the Fortinet FortiOS documentation.

### Ingest Logs from Microsoft Azure Event Hub

Abstract

Ingest logs from Microsoft Azure Event Hub with an option to ingest audit logs to use in Cortex XSIAM authentication stories.

Cortex XSIAM can ingest different types of data from Microsoft Azure Event Hub using the Microsoft Azure Event Hub data collector. To receive logs from Azure Event Hub, you must configure the Data Sources settings in Cortex XSIAM based on your Microsoft Azure Event Hub configuration. After you set up data collection, Cortex XSIAM begins receiving new logs and data from the source.

When Cortex XSIAM begins receiving logs, the app creates a new dataset (`MSFT_Azure_raw`) that you can use to initiate XQL Search queries. For example, queries refer to the in-app XQL Library. For enhanced cloud protection, you can also configure Cortex XSIAM to normalize Azure Event Hub audit logs, including Azure Kubernetes Service (AKS) audit logs, with other Cortex XSIAM authentication stories across all cloud providers using the same format, which you can query with XQL Search using the `cloud_audit_logs` dataset. For logs that you do not configure Cortex XSIAM to normalize, you can change the default dataset. Cortex XSIAM can also raise Cortex XSIAM alerts (Analytics, IOC, BIOC, and Correlation Rules) when relevant from Azure Event Hub logs. While Correlation Rules alerts are raised on non-normalized and normalized logs, Analytics, IOC, and BIOC alerts are only raised on normalized logs.

Enhanced cloud protection provides:

* Normalization of cloud logs  
* Cloud logs stitching  
* Enrichment with cloud data  
* Detection based on cloud analytics  
* Cloud-tailored investigations  
* Misconfiguration of Event Hub resources could cause ingestion delays.  
* In an existing Event Hub integration, do not change the mapping to a different Event Hub.  
* Do not use the same Event Hub for more than two purposes.

The following table provides a brief description of the different types of Azure audit logs you can collect.

For more information on Azure Event Hub audit logs, see [Overview of Azure platform logs](https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/platform-logs-overview).

| Type of data | Description |
| ----- | ----- |
| Activity logs | Retrieves events related to the operations on each Azure resource in the subscription from the outside in addition to updates on Service Health events. These logs are from the management plane. |
| Azure Active Directory (AD) Activity logs and Azure Sign-in logs | Contain the history of sign-in activity and audit trail of changes made in Azure AD for a particular tenant. Even though you can collect Azure AD Activity logs and Azure Sign-in logs using the Azure Event Hub data collector, we recommend using the Microsoft 365 data collector, because it is easier to configure. In addition, ensure that you don't configure both collectors to collect the same types of logs, because if you do so, you will be creating duplicate data in Cortex XSIAM. |
| Resource logs, including AKS audit logs | Retrieves events related to operations that were performed within an Azure resource. These logs are from the data plane. |

If you want to ingest raw Microsoft Defender for Endpoint events, use the Microsoft Defender log collector. For more information, see [Ingest raw EDR events from Microsoft Defender for Endpoint](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-E30SPrsh~A1Jt8Nm79uiwg).

Ensure that you do the following tasks before you begin configuring data collection from Azure Event Hub.

* Before you set up an Azure Event Hub, calculate the quantity of data that you expect to send to Cortex XSIAM, taking into account potential data spikes and potential increases in data ingestion, because partitions cannot be modified after creation. Use this information to ascertain the optimal number of partitions and Throughput Units (for Azure Basic or Standard) or Processing Units (for Azure Premium). Configure your Event Hub accordingly.  
* Create an Azure Event Hub. We recommend using a dedicated Azure Event Hub for this Cortex XSIAM integration. For more information, see [Quickstart: Create an event hub using Azure portal](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-create).  
* Each partition can support a throughput of up to 1 MB/s.  
* Ensure the format for the logs you want collected from the Azure Event Hub is either JSON or raw.

Configure the Azure Event Hub collection in Cortex XSIAM:

1. In the Microsoft Azure console, open the Event Hubs page, and select the Azure Event Hub that you created for collection in Cortex XSIAM.  
2. Record the following parameters from your configured event hub, which you will need when configuring data collection in Cortex XSIAM.  
   1. Your event hub’s consumer group.  
      * Select Entities → Event Hubs, and select your event hub.  
      * Select Entities → Consumer groups, and select your event hub.  
      * In the Consumer group table, copy the applicable value listed in the Name column for your Cortex XSIAM data collection configuration.  
   2. Your event hub’s connection string for the designated policy.  
      * Select Settings → Shared access policies.  
      * In the Shared access policies table, select the applicable policy.  
      * Copy the Connection string-primary key.  
   3. Your storage account connection string required for partitions lease management and checkpointing in Cortex XSIAM.  
      * Open the Storage accounts page, and either create a new storage account or select an existing one, which will contain the storage account connection string.  
      * Select Security \+ networking → Access keys, and click Show keys.  
      * Copy the applicable Connection string.  
3. Configure diagnostic settings for the relevant log types you want to collect and then direct these diagnostic settings to the designated Azure Event Hub.  
   1. Open the Microsoft Azure console.  
   2. Your navigation is dependent on the type of logs you want to configure.

| Log type | Navigation path |
| :---- | :---- |
| Activity logs | Select Azure services → Activity log → Export Activity Logs, and \+Add diagnostic setting. |
| Azure AD Activity logs and Azure Sign-in logs | Select Azure services → Azure Active Directory. Select Monitoring → Diagnostic settings, and \+Add diagnostic setting. |
| Resource logs, including AKS audit logs | Search for Monitor, and select Settings → Diagnostic settings. From your list of available resources, select the resource that you want to configure for log collection, and then select \+Add diagnostic setting.For every resource that you want to confiure, you'll have to repeat this step, or use [Azure policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview) for a general configuration. |

   3.   
      Set the following parameters:  
      * Diagnostic setting name: Specify a name for your Diagnostic setting.  
      * Logs Categories/Metrics: The options listed are dependent on the type of logs you want to configure. For Activity logs and Azure AD logs and Azure Sign-in logs, the option is called Logs Categories, and for Resource logs it's called Metrics.

| Log type | Log categories/metrics |
| :---- | :---- |
| Activity logs | Select from the list of applicable Activity log categories, the ones that you want to configure your designated resource to collect. We recommend selecting all of the options. Administrative Security ServiceHealth Alert Recommendation Policy Autoscale ResourceHealth |
| Azure AD Activity logs and Azure Sign-in logs | Select from the list of applicable Azure AD Activity and Azure Sign-in Logs Categories, the ones that you want to configure your designated resource to collect. You can select any of the following categories to collect these types of Azure logs. Azure AD Activity logs: AuditLogs Azure Sign-in logs: SignInLogs NonInteractiveUserSignInLogs ServicePrincipalSignInLogs ManagedIdentitySignInLogs ADFSSignInLogs There are additional log categories displayed. We recommend selecting all the available options. |
| Resource logs, including AKS audit logs | The list displayed is dependent on the resource that you selected. We recommend selecting all the options available for the resource. |

      *   
        Destination details: Select Stream to event hub, where additional parameters are displayed that you need to configure. Ensure that you set the following parameters using the same settings for the Azure Event Hub that you created for the collection.  
        * Subscription: Select the applicable Subscription for the Azure Event Hub.  
        * Event hub namespace: Select the applicable Subscription for the Azure Event Hub.  
        * (Optional) Event hub name: Specify the name of your Azure Event Hub.  
        * Event hub policy: Select the applicable Event hub policy for your Azure Event Hub.  
   4. Save your settings.  
4. Configure the Azure Event Hub collection in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select Azure Event Hub, and click Connect.  
   3. Set these parameters.  
      * Name: Specify a descriptive name for your log collection configuration.  
      * Event Hub Connection String: Specify your event hub’s connection string for the designated policy.  
      * Storage Account Connection String: Specify your storage account’s connection string for the designated policy.  
      * Consumer Group: Specify your event hub’s consumer group.  
      * Log Format: Select the log format for the logs collected from the Azure Event Hub as Raw, JSON, CEF, LEEF, Cisco-asa, or Corelight.  
        When you Normalize and enrich audit logs, the log format is automatically configured. As a result, the Log Format option is removed and is no longer available to configure (default).  
        * CEF or LEEF: The Vendor and Product defaults to Auto-Detect.  
          For a Log Format set to CEF or LEEF, Cortex XSIAM reads events row by row to look for the Vendor and Product configured in the logs. When the values are populated in the event log row, Cortex XSIAM uses these values even if you specified a value in the Vendor and Product fields in the Azure Event Hub data collector settings. Yet, when the values are blank in the event log row, Cortex XSIAM uses the Vendor and Product that you specified in the Azure Event Hub data collector settings. If you did not specify a Vendor or Product in the Azure Event Hub data collector settings, and the values are blank in the event log row, the values for both fields are set to unknown.  
        * Cisco-asa: The following fields are automatically set and not configurable.  
          * Vendor: Cisco  
          * Product: ASA  
        * Cisco data can be queried in XQL Search using the `cisco_asa_raw` dataset.  
        * Corelight: The following fields are automatically set and not configurable.  
          * Vendor: Corelight  
          * Product: Zeek  
        * Corelight data can be queried in XQL Search using the `corelight_zeek_raw` dataset.  
        * Raw or JSON: The following fields are automatically set and are configurable.  
          * Vendor: Msft  
          * Product: Azure  
        * Raw or JSON data can be queried in XQL Search using the `msft_azure_raw` dataset.  
      * Vendor and Product: Specify the Vendor and Product for the type of logs you are ingesting.  
        The Vendor and Product are used to define the name of your Cortex Query Language (XQL) dataset (`<vendor>_<product>_raw`). The Vendor and Product values vary depending on the Log Format selected. To uniquely identify the log source, consider changing the values if the values are configurable.  
        When you Normalize and enrich audit logs, the Vendor and Product fields are automatically configured, so these fields are removed as available options (default).  
      * Normalize and enrich audit logs: (Optional) For enhanced cloud protection, you can Normalize and enrich audit logs by selecting the checkbox (default). If selected, Cortex XSIAM normalizes and enriches Azure Event Hub audit logs with other Cortex XSIAM authentication stories across all cloud providers using the same format. You can query this normalized data with XQL Search using the `cloud_audit_logs` dataset.  
   4. Click Test to validate access, and then click Enable.  
      When events start to come in, a green check mark appears underneath the Azure Event Hub configuration with the amount of data received.

### Ingest network flow logs from Microsoft Azure Network Watcher

Abstract

Ingest network security group (NSG) or Virtual network (VNet) flow logs from Microsoft Azure Network Watcher for use in Cortex XSIAM network stories.

To receive network security group (NSG) or Virtual network (VNet) flow logs from Azure Network Watcher, you must configure data collection from Microsoft Azure Network Watcher using an Azure Function provided by Cortex XSIAM. This Azure Function requires a token that is generated when you configure your Azure Network Watcher Collector in Cortex XSIAM. After you have configured the Cortex XSIAM collector and successfully deployed the Azure Function to your Azure account, Cortex XSIAM will start receiving and ingesting network flow logs from Azure Network Watcher.

The Azure Network Watcher Collector is deployed using an ARM template. During deployment, the template retrieves keys using the `listKeys` function, and your app can bind to the blob storage using the connection string generated from those keys. After deployment, this binding works without the need to provide any connection string manually, because the keys were already retrieved and injected during deployment.

In addition to the user-specified storage account that captures the log blobs, the template also creates a secondary, internal storage account for internal operations related to the function app. This internal storage account is used by the function app for operations such as storing function state, and intermediate processing. To enhance security, public network access is disabled, and the account is restricted to private endpoints only. This additional internal storage account allows the function app to securely store data without relying on the user-specified storage account for internal processes. This separation enhances data security and isolation between user-facing storage and internal application operations. VNet integration is required only for the internal storage account's internal operations. The user-specified storage account used for NSG or VNet flow logs does not require VNet integration.

When Cortex XSIAM begins receiving logs, the app creates a new dataset (`MSFT_Azure_raw`) that you can use to initiate XQL Search queries. For example queries, refer to the in-app XQL Library. For enhanced cloud protection, you can also configure Cortex XSIAM to ingest network flow logs as Cortex XSIAM network connection stories, which you can query with XQL Search using the `xdr_data` dataset with the preset called `network_story`. Cortex XSIAM can also raise Cortex XSIAM alerts (Analytics, Correlation Rules, IOC, and BIOC) when relevant from Azure Network Watcher flow logs. While Correlation Rules alerts are raised on non-normalized and normalized logs, Analytics, IOC, and BIOC alerts are only raised on normalized logs.

Enhanced cloud protection provides:

* Normalization of cloud logs  
* Cloud logs stitching  
* Enrichment with cloud data  
* Detection based on cloud analytics  
* Cloud-tailored investigations  
* For NSG:  
  * Ensure that your NSG flow logs in Azure Network Watcher conform to the requirements as outlined in Microsoft documentation. For more information, see [Introduction to flow logging for network security groups](https://docs.microsoft.com/en-us/azure/network-watcher/network-watcher-nsg-flow-logging-overview#enabling-nsg-flow%20logs).  
  * [Enable NSG flow logs in the Microsoft Azure Portal](https://docs.microsoft.com/en-us/azure/network-watcher/network-watcher-nsg-flow-logging-portal).  
  * For VNet:  
    * Ensure that your VNet flow logs in Azure Network Watcher conform to the requirements as outlined in Microsoft documentation. For more information, see [Introduction to flow logging for virtual networks](https://learn.microsoft.com/en-us/azure/network-watcher/vnet-flow-logs-overview).  
    * [Enable VNet flow logs in the Microsoft Azure Portal](https://learn.microsoft.com/en-us/azure/network-watcher/vnet-flow-logs-manage).  
* Ensure that you have an Azure subscription with user role permissions to deploy ARM templates and create the required resources.  
  The `listKeys` function in an Azure Resource Manager (ARM) template retrieves the storage account keys, and it requires special permissions to execute. Specifically, the user or identity running the ARM template needs the following permission: `Microsoft.Storage/storageAccounts/listKeys/action`. If the user or service principal running the ARM template has the necessary user role (such as Owner or Storage Account Contributor), permission is implicitly granted for the template to retrieve the storage account keys.  
* Perform this procedure in the order shown below, because you need to save a token and a URL from Cortex XSIAM in earlier steps, and use them in Azure in later steps.  
1. Configure the Azure Network Watcher collection in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select Azure Network Watcher, and click Connect.  
   3. Set these parameters:  
      * Name: Specify a meaningful name for your log collection configuration.  
      * Enhanced Cloud Protection: (Optional) For enhanced cloud protection, you can normalize and enrich flow logs by selecting the Use flow logs in analytics checkbox. If selected, Cortex XSIAM ingests network flow logs as Cortex XSIAM network connection stories, which you can query with XQL Search using the `xdr_data` dataset with the preset called `network_story`.  
   4. Click Save & Generate Token. The token is displayed in a popup.  
      Click the copy icon next to the key and save the copy of this token somewhere safe. You will need to provide this token when you configure the Azure Function and set the Cortex Access Token value. If you forget to record the token and close the window, you will need to generate a new one and repeat this process. When you are finished, click Done to close the window.  
   5. On the Integrations page for the Azure Network Watch Collector that you created, click the Copy API URL icon and save a copy of the URL somewhere safe. You will need to provide this URL when you configure the Azure Function and set the Cortex Http Endpoint value.  
2. Configure the Azure Function provided by Cortex XSIAM.  
   1. Do one of the following, depending on the flow log type:  
      * For NSG, open this [Azure Function](https://github.com/PaloAltoNetworks/cortex-azure-functions/tree/master/nsg-flow-logs) provided by Cortex XSIAM.  
      * For VNet, open this [Azure Function](https://github.com/PaloAltoNetworks/cortex-azure-functions/tree/master/vnet-flow-logs) provided by Cortex XSIAM.  
   2. Click Deploy to Azure.  
   3. Log in to Azure, and if necessary, complete authentication procedures.  
   4. Set these parameters, where some fields are mandatory to set and others may already be populated for you.  
      * Subscription: Specify the Azure subscription that you want to use for the App Configuration. If your account has only one subscription, it is automatically selected.  
      * Resource group: Specify or create a resource group for your App Configuration store resource.  
      * Region: Specify the Azure region that you want to use.  
      * Unique Name: Enter a unique name for the function app. The name that you provide will be concatenated to some of the resource names, to make it easier to locate the related resources later on. The name must only contain alphanumeric characters (letters and numbers, no special symbols) and must contain no more than 10 characters.  
      * Cortex Access Token: Cortex HTTP authorization key that you recorded when you configured the Azure Network Watcher collection in Cortex XSIAM in an earlier step.  
      * Target Storage Account Name: Enter the name of the Azure Storage Account that was created during the NSG or VNet flow logs setup in Azure Network Watcher, where the log blobs are being stored.  
      * Target Container Name: This field should be left empty for most use cases.  
        For NSG, the default value `insights-logs-networksecuritygroupflowevent`  is the name that is automatically created for the container during configuration of the network watcher.  
        For VNet, the default value `insights-logs-flowlogflowevent` is the name that is automatically created for the container during configuration of the network watcher.  
      * Location: The region where all the resources will be deployed (leave blank to use the same region as the resource group).  
      * Cortex Http Endpoint: Specify the API URL that you recorded when you configured the Azure Network Watcher collection in Cortex XSIAM.  
      * Remote Package: The URL of the remote package ZIP file containing the Azure Function code. Leave this field empty unless instructed otherwise.  
   5. Click Review \+ Create to confirm your settings for the Azure Function.  
   6. Click Create. It can take a few minutes until the deployment is complete.  
3. In addition to your storage account, the template automatically creates another storage account that is required by the function app for internal use only. The internal storage account name is prefixed with `cortex` and is followed by a unique suffix based on the resource group, storage account, and container names.  
   After events start to come in, a green check mark appears underneath the Azure Network Watcher configuration that you created in Cortex XSIAM, and the amount of data received is displayed.

### Ingest Logs and Data from Okta

Abstract

Ingest authentication logs and data from Okta for use in Cortex XSIAM authentication stories.

To receive logs and data from Okta, you must configure the Data Sources settings in Cortex XSIAM. After you set up data collection, Cortex XSIAM immediately begins receiving new logs and data from the source. The information from Okta is then searchable in XQL Search using the `okta_sso_raw` dataset. In addition, depending on the event type, data is normalized to either `xdr_data` or `saas_audit_logs` datasets.

You can collect all types of events from Okta. When setting up the Okta data collector in Cortex XSIAM , a field called Okta Filter is available to configure collection for events of your choosing. All events are collected by default unless you define an Okta API Filter expression for collecting the data, such as `filter=eventType eq “user.session.start”.\n`. For Okta information to be weaved into authentication stories, `“user.authentication.sso”` events must be collected.

Since the Okta API enforces concurrent rate limits, the Okta data collector is built with a mechanism to reduce the amount of requests whenever an error is received from the Okta API indicating that too many requests have already been sent. In addition, to ensure you are properly notified about this, an alert is displayed in the Notification Area and a record is added to the Management Audit Logs.

Before you begin configuring data collection from Okta, ensure your Okta user has administrator privileges with a role that can create API tokens, such as the read-only administrator, Super administrator, and Organization administrator. For more information, see the [Okta Administrators Documentation](https://help.okta.com/en-us/Content/Topics/Security/Administrators.htm?cshid=ext_Security_Administrators).

To configure the Okta collection in Cortex XSIAM:

1. Identify the domain name of your Okta service.  
   From the Dashboard of your Okta console, note your Org URL.  
   For more information, see the [Okta Documentation](https://developer.okta.com/docs/guides/find-your-domain/findorg/).  
   okta-identify-domain.png  
2. Obtain your authentication token in Okta.  
   1. Select API → Tokens.  
   2. Create Token and record the token value.  
      This is your only opportunity to record the value.  
3. Select Settings → Data Sources.  
4. On the Data Sources page, click Add Data Source, search for and select Okta, and click Connect.  
5. Integrate the Okta authentication service with Cortex XSIAM.  
   1. Specify the OKTA DOMAIN (Org URL) that you identified on your Okta console.  
   2. Specify the TOKEN used to authenticate with Okta.  
   3. Specify the Okta Filter to configure collection for events of your choosing. All events are collected by default unless you define an Okta API Filter expression for collecting the data, such as `filter=eventType eq “user.session.start”.\n`. For Okta information to be weaved into authentication stories, `“user.authentication.sso”` events must be collected.  
   4. Test the connection settings.  
   5. If successful, Enable Okta log collection.  
      Once events start to come in, a green check mark appears underneath the Okta configuration with the amount of data received.  
6. After Cortex XSIAM begins receiving information from the service, you can Create an XQL Query to search for specific data. When including authentication events, you can also Create an Authentication Query to search for specific authentication data.

### Ingest logs from Windows DHCP using Elasticsearch Filebeat

Abstract

Learn how to configure Cortex XSIAM to receive Windows DHCP logs.

You can configure Cortex XSIAM to receive Windows DHCP logs using Elasticsearch Filebeat with the following data collectors.

###### Ingest Windows DHCP logs with an XDR Collector profile

Cortex XSIAM

Extend Cortex XSIAM visibility into logs from Windows DHCP using an XDR Collector Windows Filebeat profile.

You can enrich network logs with Windows DHCP data when defining data collection in an XDR Collector Windows Filebeat profile. When you add a XDR Collector Windows Filebeat profile using the Elasticsearch Filebeat default configuration file called `filebeat.yml`, you can define whether the collected data undergoes follow-up processing in the backend for Windows DHCP data. Cortex XSIAM uses Windows DHCP logs to enrich your network logs with hostnames and MAC addresses that are searchable in XQL Search using the Windows DHCP Cortex Query Language (XQL) dataset (`microsoft_dhcp_raw`).

While this enrichment is also available when configuring a [Windows DHCP Collector](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#UUID-29b52165-3275-1b22-a599-4eeb8498aa11_id32070829-07ad-475b-a5d9-200566abae3c) for a cloud data collection integration, we recommend configuring Cortex XSIAM to receive Windows DHCP logs with an XDR Collector Windows Filebeat profile because it’s the ideal setup configuration.

Configure Cortex XSIAM to receive logs from Windows DHCP using an XDR Collector Windows Filebeat profile.

1. Add an XDR Collector Profile for Windows.  
   Follow the steps for creating a Windows Filebeat profile as described in Add an XDR Collector Profile for Windows, and in the Filebeat Configuration File area, ensure that you select and Add the DHCP template. The template's content will be displayed here, and is editable.  
2. To configure collection of Windows DHCP data, edit the template text as necessary for your system.  
   You can enrich network logs with Windows DHCP data when defining data collection by setting the `vendor` to `“microsoft”` , and `product` to `“dhcp”` in the `filebeat.yml` file, which you can then query in the `microsoft_dhcp_raw` dataset.  
   To avoid formatting issues in `filebeat.yml`, we recommend that you edit the text file inside the user interface, instead of copying it and editing it elsewhere. Validate the syntax of the YML file before you finish creating the profile.

###### Ingest Windows DHCP logs with the Windows DHCP Collector

Cortex XSIAM

Extend Cortex XSIAM visibility into logs from Windows DHCP using Elasticsearch Filebeat with the Windows DHCP data collector.

To receive Windows DHCP logs, you must configure data collection from Windows DHCP via Elasticsearch Filebeat. This is configured by setting up a Windows DHCP Collector in Cortex XSIAM and installing and configuring an Elasticsearch Filebeat agent on your Windows DHCP Server. Cortex XSIAM supports using Filebeat up to version 8.0.1 with the Windows DHCP Collector.

Certain settings in the Elasticsearch Filebeat default configuration file called `filebeat.yml` must be populated with values provided when you configure the Data Sources settings in Cortex XSIAM for the Windows DHCP Collector. To help you configure the `filebeat.yml` correctly, Cortex XSIAM provides an example file that you can download and customize. After you set up collection integration, Cortex XSIAM begins receiving new logs and data from the source.

For more information on configuring the `filebeat.yml` file, see the Elastic Filebeat Documentation.

Windows DHCP logs are stored as CSV (comma-separated values) log files. The logs rotate by days (`DhcpSrvLog-<day>.log`), and each file contains two sections: `Event ID Meaning` and the events list.

As soon as Cortex XSIAM begins receiving logs, the app automatically creates a Windows DHCP XQL dataset (`microsoft_dhcp_raw`). Cortex XSIAM uses Windows DHCP logs to enrich your network logs with hostnames and MAC addresses that are searchable in XQL Search using the Windows DHCP Cortex Query Language (XQL) dataset.

Configure Cortex XSIAM to receive logs from Windows DHCP via Elasticsearch Filebeat with the Windows DHCP collector.

1. Configure the Windows DHCP Collector in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select Windows DHCP, and click Connect.  
   3. (Optional) Download example filebeat.yml file.  
      To help you configure your `filebeat.yml` file correctly, Cortex XSIAM provides an example `filebeat.yml` file that you can download and customize. To download this file, use the link provided in this dialog box.  
      To avoid formatting issues in your `filebeat.yml`, we recommend that you use the download example file to make your customizations. Do not copy and paste the code syntax examples provided later in this procedure into your file.  
   4. Specify a descriptive Name for your log collection configuration.  
   5. Save & Generate Token. The token is displayed in a blue box, which is blurred out in the image below.  
      Click the copy icon next to the key and record it somewhere safe. You will need to provide this key when you set the `api_key` value in the **Elasticsearch Output** section in the `filebeat.yml` file as explained in **Step \#2**. If you forget to record the key and close the window you will need to generate a new key and repeat this process.  
   6. Select Done to close the window.  
   7. In the Integrations page for the Windows DHCP Collector that you created, select Copy api url and record it somewhere safe. You will need to provide this URL when you set the **`hosts`** value in the **Elasticsearch Output** section in the `filebeat.yml` file as explained in **Step \#2**.  
2. Configure an Elasticsearch Filebeat agent on your Windows DHCP Server.  
   1. Navigate to the Elasticsearch Filebeat installation directory, and open the `filebeat.yml` file to configure data collection with Cortex XSIAM. We recommend that you use the download example file provided by Cortex XSIAM.  
   2. Update the following sections and tags in the `filebeat.yml` file. The example code below details the specific sections to make these changes in the file.

**Filebeat inputs**: Define the paths to crawl and fetch. The code below provides an example of how to configure the **Filebeat inputs** section in the `filebeat.yml` file with these paths configured.  
\# \============================== Filebeat inputs \===============================  
filebeat.inputs:  
  \# Each \- is an input. Most options can be set at the input level, so  
  \# you can use different inputs for various configurations.  
  \# Below are the input specific configurations.  
  \- type: log    
    \# Change to true to enable this input configuration.    
    enabled: true    
    \# Paths that should be crawled and fetched. Glob based paths.    
    paths:         
      \- c:\\Windows\\System32\\dhcp\\DhcpSrvLog\*.log    

* 

**Elasticsearch Output**: Set the `hosts` and `api_key`, where both of these values are obtained when you configured the Windows DHCP Collector in Cortex XSIAM as explained in **Step \#1**. The code below provides an example of how to configure the **Elasticsearch Output** section in the `filebeat.yml` file and indicates which settings need to be obtained from Cortex XSIAM.  
\# \---------------------------- Elasticsearch Output \----------------------------  
output.elasticsearch:    
  enabled: true    
  \# Array of hosts to connect to.      
  hosts: \["OBTAIN THIS URL FROM CORTEX XDR"\]    
  \# Protocol \- either \`http\` (default) or \`https\`.    
  protocol: "https"    
  compression\_level: 5    
  \# Authentication credentials \- either API key or username/password. 

*   api\_key: "OBTAIN THIS KEY FROM CORTEX XDR"

**Processors**: Set the `tokenizer` and add a `drop_event processor` to drop all events that do not start with an event ID. The code below provides an example of how to configure the **Processors** section in the `filebeat.yml` file and indicates which settings need to be obtained from Cortex XSIAM.  
The `tokenizer` definition is dependent on the Windows server version that you are using as the log format differs.  
\-For platforms earlier than Windows Server 2008, use `"%{id},%{date},%{time},%{description},%{ipAddress},%{hostName},%{macAddress}"`  
\-For Windows Server 2008 and 2008 R2, use `"%{id},%{date},%{time},%{description},%{ipAddress},%{hostName},%{macAddress},%{userName},%{transactionID},%{qResult},%{probationTime},%{correlationID}"`  
For Windows Server 2012 and above, use `"%{id},%{date},%{time},%{description},%{ipAddress},%{hostName},%{macAddress},%{userName},%{transactionID},%{qResult},%{probationTime},%{correlationID},%{dhcid},%{vendorClassHex},%{vendorClassASCII},%{userClassHex},%{userClassASCII},%{relayAgentInformation},%{dnsRegError}"`  
\# \================================= Processors \=================================  
processors:    
  \- add\_host\_metadata:        
    when.not.contains.tags: forwarded    
  \- drop\_event.when.not.regexp.message: "^\[0-9\]+,.\*"    
  \- dissect:         
    tokenizer: "%{id},%{date},%{time},%{description},%{ipAddress},%{hostName},%{macAddress},%{userName},%{transactionID},%{qResult},%{probationTime},%{correlationID},%{dhcid},%{vendorClassHex},%{vendorClassASCII},%{userClassHex},%{userClassASCII},%{relayAgentInformation},%{dnsRegError}"    
  \- drop\_fields:         
    fields: \["message"\]    
  \- add\_locale: \~  
  \- rename:  
      fields:  
        \- from: "event.timezone"  
          to: "dissect.timezone"  
      ignore\_missing: true  
      fail\_on\_error: false  
  \- add\_cloud\_metadata: \~    
  \- add\_docker\_metadata: \~  

*   \- add\_kubernetes\_metadata: \~  
3. Verify the status of the integration.  
   Return to the Integrations page and view the statistics for the log collection configuration.  
4. After Cortex XSIAM begins receiving logs from Windows DHCP via Elasticsearch Filebeat, you can use the XQL Search to search for logs in the new dataset (`microsoft_dhcp_raw`).

### Ingest logs from Zscaler Internet Access

Abstract

Extend Cortex XSIAM visibility into logs from Zscaler Internet Access (ZIA).

If you use Zscaler Internet Access (ZIA) in your network, you can forward your firewall and network logs to Cortex XSIAM for analysis. This enables you to take advantage of Cortex XSIAM anomalous behavior detection and investigation capabilities. Cortex XSIAM can use the firewall and network logs from ZIA as the sole data source, and can also use these firewall and network logs from ZIA in conjunction with Palo Alto Networks firewall and network logs. For additional endpoint context, you can also use Cortex XSIAM to collect and alert on endpoint data.

To integrate your logs, you first need to set up an applet in a broker VM within your network to act as a Syslog Collector. You then configure forwarding on your log devices to send logs to the Syslog collector in a CEF format. To provide seamless log ingestion, Cortex XSIAM automatically maps the fields in your traffic logs to the Cortex XSIAM log format.

As soon as Cortex XSIAM starts to receive logs, the app performs these actions.

* Begins stitching network connection and firewall logs with other logs to form network stories. Cortex XSIAM can also analyze your logs to raise Analytics alerts and can apply IOC, BIOC, and Correlation Rule matching. You can also use queries to search your network connection logs.  
* Creates a Zscaler Cortex Query Language (XQL) dataset, which enables you to search the logs using XQL Search. The Zscaler XQL datasets are dependent on the ZIA NSS Feed that you've configured for the types of logs you want to collect.  
  * Firewall logs: `zscaler_nssfwlog_raw`  
  * Web logs: `zscalar_nssweblog_raw`

To ingest logs from Zscaler Internet Access (ZIA):

1. Activate the Syslog Collector.  
2. Increase log storage for ZIA logs. For more information, see Manage Your Log Storage.  
3. Configure NSS log forwarding in Zscaler Internet Access to the Syslog Collector in a CEF format.  
   1. In the Zscaler Internet Access application, select Administration → Nanolog Streaming Service.  
   2. In the NSS Feeds tab, Add NSS Feed.  
   3. In the Add NSS Feed screen, configure the fields for the Cortex XSIAM Syslog Collector.  
      The steps below differ depending on the type of NSS Feed you are configuring to collect either firewall logs or web logs. For more information on all the configurations available on the screen, see the ZIA documentation:  
      * Firewall logs: See [Adding NSS Feeds for Firewall Logs](https://help.zscaler.com/zia/adding-nss-feeds-firewall-logs).  
      * Web logs: See [Adding NSS Feeds for Web Logs](https://help.zscaler.com/zia/adding-nss-feeds-web-logs).  
   4. The following image displays the fields required to add an NSS feed.  
      ![zscaler\_add\_nss\_feed.png][image9]  
      * NSS Type: Select either NSS for Web (default) to collect web logs or NSS for Firewall to collect firewall logs.  
      * SIEM TCP Port: Specify the port that you set when activating the Syslog Collector in Cortex XSIAM. See [Activate the Syslog Collector](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#UUID-717ddb62-da1d-361a-e9bd-f47bdf9eacd6_N1669558051390).  
      * SIEM IP Address: Specify the IP that you set when activating the Syslog Collector in Cortex XSIAM. See [Activate the Syslog Collector](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#UUID-717ddb62-da1d-361a-e9bd-f47bdf9eacd6_N1669558051390).  
      * Feed Escape Character: Specify the feed escape character as `=`.  
      * Feed Output Type: Select Custom.  
      * Feed Output Format: Specify the output format, which is dependent on the type of logs you are collecting as defined in the NSS Type field:

| Log type | Feed output format |
| :---- | :---- |
| Firewall logs | `%s{mon} %02d{dd} %02d{hh}:%02d{mm}:%02d{ss} zscaler-nss-fw CEF:0|Zscaler|NSSFWlog|5.7|%s{action}|%s{rulelabel}|3|act=%s{action} suser=%s{login} src=%s{csip} spt=%d{csport} dst=%s{cdip} dpt=%d{cdport} deviceTranslatedAddress=%s{ssip} deviceTranslatedPort=%d{ssport} destinationTranslatedAddress=%s{sdip} destinationTranslatedPort=%d{sdport} sourceTranslatedAddress=%s{tsip} sourceTranslatedPort=%d{tsport} proto=%s{ipproto} tunnelType=%s{ttype} dnat=%s{dnat} stateful=%s{stateful} spriv=%s{location} reason=%s{rulelabel} in=%ld{inbytes} out=%ld{outbytes} rt=%s{mon} %02d{dd} %02d{hh}:%02d{mm}:%02d{ss} deviceDirection=1 cs1=%s{dept} cs1Label=dept cs2=%s{nwsvc} cs2Label=nwService cs3=%s{nwapp} cs3Label=nwApp cs4=%s{aggregate} cs4Label=aggregated cs6=%s{threatname} cs6label=threatname cn1=%d{durationms} cn1Label=durationms cn2=%d{numsessions} cn2Label=numsessions cs5Label=ipCat cs5=%s{ipcat} cat=%s{threatcat} destCountry=%s{destcountry} avgduration=%d{avgduration}` |
| Web logs | `%s{mon} %02d{dd} %02d{hh}:%02d{mm}:%02d{ss} zscaler-nss CEF:0|Zscaler|NSSWeblog|5.0|%s{action}|%s{reason}|3|act=%s{action} app=%s{proto} cat=%s{urlcat} dhost=%s{ehost} dst=%s{sip} src=%s{cip} in=%d{respsize} outcome=%s{respcode} out=%d{reqsize} request=%s{eurl} rt=%s{mon} %02d{dd} %d{yy} %02d{hh}:%02d{mm}:%02d{ss} sourceTranslatedAddress=%s{cintip} requestClientApplication=%s{ua} requestMethod=%s{reqmethod} suser=%s{login} spriv=%s{location} externalId=%d{recordid} fileType=%s{filetype} reason=%s{reason} destinationServiceName=%s{appname} cn1=%d{riskscore} cn1Label=riskscore cs1=%s{dept} cs1Label=dept cs2=%s{urlsupercat} cs2Label=urlsupercat cs3=%s{appclass} cs3Label=appclass cs4=%s{malwarecat} cs4Label=malwarecat cs5=%s{threatname} cs5Label=threatname cs6=%s{dlpeng} cs6Label=dlpeng ZscalerNSSWeblogURLClass=%s{urlclass} ZscalerNSSWeblogDLPDictionaries=%s{dlpdict} requestContext=%s{ereferer} contenttype=%s{contenttype} unscannabletype=%s{unscannabletype} deviceowner=%s{deviceowner} devicehostname=%s{devicehostname}\n` |

   5.   
      Click Save.  
   6. Click Save and activate the change according to the [Zscaler Internet Access (ZIA) documentation](https://help.zscaler.com/zia/saving-and-activating-changes-admin-portal).

### Ingest logs from Zscaler Private Access

Abstract

Extend Cortex XSIAM visibility into logs from Zscaler Private Access (ZPA).

If you use Zscaler Private Access (ZPA) in your network as an alternative to VPNs, you can forward your network logs to Cortex XSIAM for analysis. This enables you to take advantage of Cortex XSIAM anomalous behavior detection and investigation capabilities. Cortex XSIAM can use the network logs from ZPA as the sole data source, and can also use these network logs from ZPA in conjunction with Palo Alto Networks network logs.

As soon as Cortex XSIAM starts to receive logs, the following actions are performed:

* Stitching network connection logs with other logs to form network stories. Cortex XSIAM can also analyze your logs to apply IOC, BIOC, and Correlation Rules matching. You can also use queries to search your network connection logs.  
* Creates a Zscaler Cortex Query Language (XQL) dataset (`zscaler_zpa_raw`), which enables you to search the logs using XQL Search.

To integrate your logs, you first need to set up an applet in a Broker VM within your network to act as a Syslog Collector. You then configure forwarding on your log devices to send logs to the Syslog collector in a LEEF format. To provide seamless log ingestion, Cortex XSIAM automatically maps the fields in your traffic logs to the Cortex XSIAM log format.

**Prerequisite Step**

Before you can add a log receiver in Zscaler Private Access, as explained in the task below, you must first deploy your App Connectors. For more information, see [App Connector Deployment Guides for Supported Platforms](https://help.zscaler.com/zpa/app-connector-management/app-connector-deployment-guides-supported-platforms).

To ingest logs from Zscaler Private Access (ZPA):

1. Activate the Syslog Collector.  
2. Increase log storage for ZPA logs. For more information, see Manage Your Log Storage.  
3. Configure ZPA log forwarding in Zscaler Private Access to the Syslog Collector in a LEEF format.  
   1. In the Zscaler Private Access application, select Administration → Log Receivers.  
   2. Click Add Log Receiver.  
      For more information on configuring the parameters on the screen, see the Zscaler Private Access (ZPA) documentation for [Configuring a Log Receiver](https://help.zscaler.com/zpa/configuring-log-receiver).  
   3. In the Add Log Receiver window, configure the following fields on the Log Receiver tab:  
      * Name: Specify a name for the log receiver. The name cannot contain special characters, with the exception of periods (.), hyphens (-), and underscores ( \_ ).  
      * Description: (Optional) Specify a log receiver description.  
      * Domain or IP Address: Specify the fully qualified domain name (FQDN) or IP address for the log receiver that you set when activating the Syslog Collector in Cortex XSIAM. See Activate Syslog Collector.  
      * TCP Port: Specify the TCP port number used by the log receiver that you set when activating the Syslog Collector in Cortex XSIAM. See Activate Syslog Collector.  
      * TLS Encryption: Toggle to Enabled to encrypt traffic between the log receiver and your Syslog Collector in Cortex XSIAMusing mutually authenticated TLS communication. To use this setting, the log receiver must support TLS communication. For more information, see [About the Log Streaming Service](https://help.zscaler.com/zpa/about-log-streaming-service#tlsencryption).  
      * App Connector Groups: (Optional) Select the App Connector groups that can forward logs to the receiver, and click Done. You can search for a specific group, click Select All to apply all groups, or click Clear Selection to remove all selections.  
   4. Click Next.  
   5. Configure the following fields in the Log Stream tab:  
      * Log Type: Select the log type you want to collect, where only the following logs types are currently supported to collect with your Syslog Collector in Cortex XSIAM:  
        You can only configure a ZPA log receiver to collect one type of log with your Syslog Collector in Cortex XSIAM. To configure more that one log type, you'll need to add another log receiver.  
        * User Activity: Information on end user requests to applications. For more information, see [User Activity Log Fields](https://help.zscaler.com/zpa/about-user-activity-log-fields).  
        * User Status: Information related to an end user's availability and connection to ZPA. For more information, see [User Status Log Fields](https://help.zscaler.com/zpa/about-user-status-log-fields).  
        * App Connector Status: Information related to an App Connector's availability and connection to ZPA. For more information, see [About App Connector Status Log Fields](https://help.zscaler.com/zpa/about-connector-status-log-fields).  
        * Audit Logs: Session information for all admins accessing the ZPA Admin Portal. For more information, See [About Audit Log Fields](https://help.zscaler.com/zpa/about-audit-log-fields) and [About Audit Logs](https://help.zscaler.com/zpa/about-audit-logs).  
      * Log Template: Select a Custom template.  
      * Log Stream Content: Create the log template that you require, according to the Log Type you've selected, using the Zscaler documentation mentioned in previous steps as a reference.  
        If you copy and modify the following examples in the table below, validate your log template using an editor, ensuring that there are no additional spaces or line breaks, and then copy and paste it into the Log Stream Content field.

| Log type | Log template |
| :---- | :---- |
| User activity | LEEF:1.0|Zscaler|ZPA|4.1|%s{ConnectionStatus}%s{InternalReason}|cat=ZPA User  Activity\\tdevTime=%s{LogTimestamp:epoch}\\tCustomer=%s{Customer}\\tSessionID=%s {SessionID}\\tConnectionID=%s{ConnectionID}\\tInternalReason=%s{InternalReason} \\tConnectionStatus=%s{ConnectionStatus}\\tproto=%d{IPProtocol} \\tDoubleEncryption=%d{DoubleEncryption}\\tusrName=%s{Username} \\tdstPort=%d{ServicePort}\\tsrc=%s{ClientPublicIP}\\tsrcPreNAT=%s{ClientPrivateIP} \\tClientLatitude=%f{ClientLatitude}\\tClientLongitude=%f{ClientLongitude} \\tClientCountryCode=%s{ClientCountryCode}\\tClientZEN=%s{ClientZEN} \\tpolicy=%s{Policy}\\tConnector=%s{Connector}\\tConnectorZEN=%s{ConnectorZEN} \\tConnectorIP=%s{ConnectorIP}\\tConnectorPort=%d{ConnectorPort} \\tApplicationName=%s{Host}\\tApplicationSegment=%s{Application}\\tAppGroup=%s{AppGroup} \\tServer=%s{Server}\\tdst=%s{ServerIP}\\tServerPort=%d{ServerPort} \\tPolicyProcessingTime=%d{PolicyProcessingTime}\\tServerSetupTime=%d{ServerSetupTime} \\tTimestampConnectionStart:iso8601=%s{TimestampConnectionStart:iso8601} \\tTimestampConnectionEnd:iso8601=%s{TimestampConnectionEnd:iso8601} \\tTimestampCATx:iso8601=%s{TimestampCATx:iso8601} \\tTimestampCARx:iso8601=%s{TimestampCARx:iso8601} \\tTimestampAppLearnStart:iso8601=%s{TimestampAppLearnStart:iso8601} \\tTimestampZENFirstRxClient:iso8601=%s{TimestampZENFirstRxClient:iso8601} \\tTimestampZENFirstTxClient:iso8601=%s{TimestampZENFirstTxClient:iso8601} \\tTimestampZENLastRxClient:iso8601=%s{TimestampZENLastRxClient:iso8601} \\tTimestampZENLastTxClient:iso8601=%s{TimestampZENLastTxClient:iso8601} \\tTimestampConnectorZENSetupComplete:iso8601=%s{TimestampConnectorZENSetupComplete:iso8601} \\tTimestampZENFirstRxConnector:iso8601=%s{TimestampZENFirstRxConnector:iso8601} \\tTimestampZENFirstTxConnector:iso8601=%s{TimestampZENFirstTxConnector:iso8601} \\tTimestampZENLastRxConnector:iso8601=%s{TimestampZENLastRxConnector:iso8601} \\tTimestampZENLastTxConnector:iso8601=%s{TimestampZENLastTxConnector:iso8601} \\tZENTotalBytesRxClient=%d{ZENTotalBytesRxClient}\\tZENBytesRxClient=%d{ZENBytesRxClient} \\tZENTotalBytesTxClient=%d{ZENTotalBytesTxClient}\\tZENBytesTxClient=%d{ZENBytesTxClient} \\tZENTotalBytesRxConnector=%d{ZENTotalBytesRxConnector} \\tZENBytesRxConnector=%d{ZENBytesRxConnector} \\tZENTotalBytesTxConnector=%d{ZENTotalBytesTxConnector} \\tZENBytesTxConnector=%d{ZENBytesTxConnector}\\tIdp=%s{Idp}\\n |
| User status | LEEF:1.0|Zscaler|ZPA|4.1|%s{SessionStatus}|cat=ZPA User Status \\tdevTime=%s{LogTimestamp:epoch}\\tCustomer=%s{Customer} \\tusrName=%s{Username}\\tSessionID=%s{SessionID}\\tSessionStatus=%s{SessionStatus} \\tVersion=%s{Version}\\tZEN=%s{ZEN}\\tCertificateCN=%s{CertificateCN} \\tsrcPreNAT=%s{PrivateIP}\\tsrc=%s{PublicIP}\\tLatitude=%f{Latitude} \\tLongitude=%f{Longitude}\\tCountryCode=%s{CountryCode} \\tTimestampAuthentication:iso8601=%s{TimestampAuthentication:iso8601} \\tTimestampUnAuthentication:iso8601=%s{TimestampUnAuthentication:iso8601} \\tdstBytes=%d{TotalBytesRx}\\tsrcBytes=%d{TotalBytesTx}\\tIdp=%s{Idp} \\tidentHostName=%s{Hostname}\\tPlatform=%s{Platform}\\tClientType=%s{ClientType} \\tTrustedNetworks=%s(,){TrustedNetworks}\\tTrustedNetworksNames=%s(,){TrustedNetworksNames} \\tSAMLAttributes=%s{SAMLAttributes}\\tPosturesHit=%s(,){PosturesHit} \\tPosturesMiss=%s(,){PosturesMiss}\\tZENLatitude=%f{ZENLatitude} \\tZENLongitude=%f{ZENLongitude}\\tZENCountryCode=%s{ZENCountryCode}\\n |
| App connector status | LEEF:1.0|Zscaler|ZPA|4.1|%s{SessionStatus}|cat=Connector Status \\tdevTime=%s{LogTimestamp:epoch}\\tCustomer=%s{Customer}\\tSessionID=%s{SessionID} \\tSessionType=%s{SessionType}\\tVersion=%s{Version}\\tPlatform=%s{Platform} \\tZEN=%s{ZEN}\\tConnector=%s{Connector}\\tConnectorGroup=%s{ConnectorGroup} \\tsrcPreNAT=%s{PrivateIP}\\tsrc=%s{PublicIP}\\tLatitude=%f{Latitude} \\tLongitude=%f{Longitude}\\tCountryCode=%s{CountryCode} \\tTimestampAuthentication:iso8601=%s{TimestampAuthentication:iso8601} \\tTimestampUnAuthentication:iso8601=%s{TimestampUnAuthentication:iso8601} \\tCPUUtilization=%d{CPUUtilization}\\tMemUtilization=%d{MemUtilization} \\tServiceCount=%d{ServiceCount}\\tInterfaceDefRoute=%s{InterfaceDefRoute} \\tDefRouteGW=%s{DefRouteGW}\\tPrimaryDNSResolver=%s{PrimaryDNSResolver} \\tHostStartTime=%s{HostStartTime}\\tConnectorStartTime=%s{ConnectorStartTime} \\tNumOfInterfaces=%d{NumOfInterfaces}\\tBytesRxInterface=%d{BytesRxInterface} \\tPacketsRxInterface=%d{PacketsRxInterface}\\tErrorsRxInterface=%d{ErrorsRxInterface} \\tDiscardsRxInterface=%d{DiscardsRxInterface}\\tBytesTxInterface=%d{BytesTxInterface} \\tPacketsTxInterface=%d{PacketsTxInterface}\\tErrorsTxInterface=%d{ErrorsTxInterface} \\tDiscardsTxInterface=%d{DiscardsTxInterface}\\tTotalBytesRx=%d{TotalBytesRx} \\tTotalBytesTx=%d{TotalBytesTx}\\n |
| Audit logs | LEEF:1.0|Zscaler|ZPA|4.1|%s{auditOperationType}|cat=ZPA\_Audit\_Log\\t devTime=%s{modifiedTime:epoch}\\t creationTime=%s{creationTime:iso8601}\\t requestId=%s{requestId}\\t sessionId=%s{sessionId}\\t auditOldValue=%s{auditOldValue}\\t auditNewValue=%s{auditNewValue}\\t auditOperationType=%s{auditOperationType}\\t objectType=%s{objectType}\\t objectName=%s{objectName}\\t objectId=%d{objectId}\\t accountName=%d{customerId}\\t usrName=%s{modifiedByUser}\\n |

      *   
        (Optional) You can define a streaming Policy for the log receiver. This entails configuring the SAML Attributes, Application Segments, Segment Groups, Client Types, and Session Statuses. For more information on configuring these settings, see the [Log Stream instructions](https://help.zscaler.com/zpa/configuring-log-receiver#Step2).  
   6. Click Next.  
   7. In the Review tab, verify your log receiver configuration.  
   8. Click Save.

## Ingest authentication logs and data

Abstract

Ingest authentication logs from external authentication services—such as Okta and Azure AD—into authentication stories with Cortex XSIAM.

When you ingest authentication logs and data from an external source, Cortex XSIAM can weave that information into authentication stories. An authentication story unites logs and data regardless of the information source (for example, from an on-premise KDC or from a cloud-based authentication service) into a uniform schema. To search authentication stories, you can use the Query Builder or XQL Search.

Cortex XSIAM can ingest authentication logs and data from various authentication services.

### Ingest audit logs from AWS Cloud Trail

Abstract

Take advantage of Cortex XSIAM investigation capabilities and set up audit log ingestion for your AWS CloudTrail logs.

You can forward audit logs for the relative service to Cortex XSIAM from AWS CloudTrail.

To receive audit logs from Amazon Simple Storage Service (Amazon S3) via AWS CloudTrail, you must first configure data collection from Amazon S3. You can then configure the Data Sources settings in Cortex XSIAM for Amazon S3. After you set up collection integration, Cortex XSIAM begins receiving new logs and data from the source.

For more information on configuring data collection from Amazon S3 using AWS CloudTrail, see the [AWS CloudTrail Documentation](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-create-a-trail-using-the-console-first-time.html).

As soon as Cortex XSIAM begins receiving logs, the app automatically creates an Amazon S3 Cortex Query Language (XQL) dataset (`aws_s3_raw`). This enables you to search the logs with XQL Search using the dataset. For example queries, refer to the in-app XQL Library. As part of the enhanced cloud protection,

For enhanced cloud protection, you can also configure Cortex XSIAM to stitch Amazon S3 audit logs with other Cortex XSIAM authentication stories across all cloud providers using the same format, which you can query with XQL Search using the `cloud_audit_logs` dataset. Cortex XSIAM can also raise Cortex XSIAM alerts (Analytics, IOC, BIOC, and Correlation Rules) when relevant from Amazon S3 logs. While Correlation Rules alerts are raised on non-normalized and normalized logs, Analytics, IOC, and BIOC alerts are only raised on normalized logs.

Enhanced cloud protection provides the following:

* Normalization of cloud logs  
* Cloud logs stitching  
* Enrichment with cloud data  
* Detection based on cloud analytics  
* Cloud-tailored investigations

**Prerequisite Steps**

Be sure you do the following tasks before you begin configuring data collection from Amazon S3 via AWS CloudTrail.

* Ensure that you have the proper permissions to access AWS CloudTrail and have the necessary permissions to create audit logs. You need at a minimum the following permissions in AWS for an Amazon S3 bucket and Amazon Simple Queue Service (SQS).  
  * **Amazon S3 bucket**: `GetObject`  
  * **SQS**: `ChangeMessageVisibility`, `ReceiveMessage`, and `DeleteMessage`.  
* Determine how you want to provide access to Cortex XSIAM to your logs and to perform API operations. You have the following options:  
  * Designate an AWS IAM user, where you will need to know the Account ID for the user and have the relevant permissions to create an access key/id for the relevant IAM user. This is the default option as explained in Configure the Amazon S3 collection by selecting Access Key.  
  * Create an assumed role in AWS to delegate permissions to a Cortex XSIAM AWS service. This role grants Cortex XSIAM access to your flow logs. For more information, see [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html). This is the Assumed Role option described in the Amazon S3 collection configuration.  
* To collect Amazon S3 logs that use server-side encryption (SSE), the user role must have an IAM policy that states that Cortex XSIAM has kms:Decrypt permissions. With this permission, Amazon S3 automatically detects if a bucket is encrypted and decrypts it. If you want to collect encrypted logs from different accounts, you must have the decrypt permissions for the user role also in the key policy for the master account Key Management Service (KMS). For more information, see [Allowing users in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html).

To configure Cortex XSIAM to receive audit logs from Amazon S3 via AWS Cloudtrail:

1. Log in to the [AWS Management Console](https://console.aws.amazon.com/).  
2. From the menu bar, ensure that you have selected the correct region for your configuration.  
3. Configure an AWS CloudTrail trail with audit logs.  
   1. For more information on creating an AWS CloudTrail trail, see [Create a trail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-create-a-trail-using-the-console-first-time.html).  
   2. If you already have an Amazon S3 bucket configured with AWS CloudTrail audit logs, skip this step and go to Configure an Amazon Simple Queue Service (SQS).  
   3. Open the [CloudTrail Console](https://console.aws.amazon.com/cloudtrail/), and click Create trail.  
   4. Configure the following settings for your CloudTrail trail, where the default settings should be configured unless otherwise indicated.  
      * Trail name: Specify a descriptive name for your CloudTrail trail.  
      * Storage location: Select Create new S3 bucket to configure a new Amazon S3 bucket, and specify a unique name in the Trail log bucket and folder field, or select Use existing S3 bucket and Browse to the S3 bucket you already created. If you select an existing Amazon S3 bucket, the bucket policy must grant CloudTrail permission to write to it. For information about manually editing the bucket policy, see [Amazon S3 Bucket Policy for CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create-s3-bucket-policy-for-cloudtrail.html).  
        It is the customer’s responsibility to define a retention policy for your Amazon S3 bucket by creating a Lifecycle rule in the Management tab. We recommend setting the retention policy to at least 7 days to ensure that the data is retrieved under all circumstances.  
      * Customer managed AWS KMS key: You can either select a New key and specify the AWS KMS alias, or select an Existing key, and select the AWS KMS alias. The KMS key and S3 bucket must be in the same region.  
      * SNS notification delivery: (Optional) If you want to be notified whenever CloudTrail publishes a new log to your Amazon S3 bucket, click Enabled. Amazon Simple Notification Service (Amazon SNS) manages these notifications, which are sent for every log file delivery to your S3 bucket, as opposed to every event. When you enable this option, you can either Create a new SNS topic by selecting New and the SNS topic is displayed in the field, or use an Existing topic and select the SNS topic. For more information, see [Configure SNS Notifications for CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/configure-sns-notifications-for-cloudtrail.html).  
   5. The CloudWatch Logs \- optional settings are not supported and should be left disabled.  
   6. Click Next, and configure the following Choose log events settings.  
      * Event type: Leave the default Management events checkbox selected to capture audit logs. Depending on your system requirements, you can also select Data events to log the resource operations performed on or within a resource, or Insights events to identify unusual activity, errors, or user behavior in your account. Based on your selection, additional fields are displayed on the screen to configure under section headings with the same name as the event type.  
      * Management events section: Configure the following settings.  
        \-API activity: For Management events, select the API activities you want to log. By default, the Read and Write activities are logged.  
        \-Exclude AWS KMS events: (Optional) If you want to filter AWS Key Management Service (AWS KMS) events out of your trail, select the checkbox. By default, all AWS KMS events are included.  
      * Data events section: (Optional) This section is displayed when you configure the Event type to include Data events, which relate to resource operations performed on or within a resource, such as reading and writing to a S3 bucket. For more information on configuring these optional settings in AWS CloudTrail, see [Creating a trail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-create-a-trail-using-the-console-first-time.html).  
      * Insights events section: (Optional) This section is displayed when you configure the Event type to include Insight events, which relate to unusual activities, errors, or user behavior on your account. For more information on configuring these optional settings in AWS CloudTrail, see [Creating a trail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-create-a-trail-using-the-console-first-time.html).  
   7. Click Next.  
   8. In the Review and create page, look over the trail configurations settings that you have configured and if they are correct, click Create trail. If you need to make a change, click Edit beside the particular step that you want to update.  
      The new trail is listed in the Trails page, which lists the trails in your account from all Regions. It can take up to 15 minutes for CloudTrail to begin publishing log files. You can see the log files in the S3 bucket that you specified. For more information, see [Creating a trail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-create-a-trail-using-the-console-first-time.html).  
4. Configure an Amazon Simple Queue Service (SQS).  
   Ensure that you create your Amazon S3 bucket and Amazon SQS queue in the same region.  
   1. In the [Amazon SQS Console](https://console.aws.amazon.com/sqs/), click Create Queue.  
   2. Configure the following settings, where the default settings should be configured unless otherwise indicated.  
      * Type: Select Standard queue (default).  
      * Name: Specify a descriptive name for your SQS queue.  
      * Configuration section: Leave the default settings for the various fields.

Access policy → Choose method: Select Advanced and update the Access policy code in the editor window to enable your Amazon S3 bucket to publish event notification messages to your SQS queue. Use this sample code as a guide for defining the `“Statement”` with the following definitions:  
\-**`“Resource”`**: Leave the automatically generated ARN for the SQS queue that is set in the code, which uses the format `“arn:sns:Region:account-id:topic-name”`.  
You can retrieve your bucket’s ARN by opening the [Amazon S3 Console](https://console.aws.amazon.com/s3/) in a browser window. In the Buckets section, select the bucket that you created for collecting the Amazon S3 flow logs, click Copy ARN, and paste the ARN in the field.  
![bucket-copy-arn.png][image10]  
For more information on granting permissions to publish messages to an SQS queue, see [Granting permissions to publish event notification messages to a destination](https://docs.aws.amazon.com/AmazonS3/latest/userguide/grant-destinations-permissions-to-s3.html).  
{  
  "Version": "2012-10-17",  
  "Statement": \[  
    {  
      "Effect": "Allow",  
      "Principal": {  
        "Service": "s3.amazonaws.com"  
      },  
      "Action": "SQS:SendMessage",  
      "Resource": "\[Leave automatically generated ARN for the SQS queue defined by AWS\]",  
      "Condition": {  
        "ArnLike": {  
          "aws:SourceArn": "\[ARN of your Amazon S3 bucket\]"  
        }  
      }  
    },  
  \]

* }  
  * Dead-letter queue section: We recommend that you configure a queue for sending undeliverable messages by selecting Enabled, and then in the Choose queue field selecting the queue to send the messages. You may need to create a new queue for this, if you do not already have one set up. For more information, see [Amazon SQS dead-letter queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html).  
  3. Click Create queue.  
     Once the SQS is created, a message indicating that the queue was successfully configured is displayed at the top of the page.  
5. Configure an event notification to your Amazon SQS whenever a file is written to your Amazon S3 bucket.  
   1. Open the [Amazon S3 Console](https://console.aws.amazon.com/s3/) and in the Properties tab of your Amazon S3 bucket, scroll down to the Event notifications section, and click Create event notification.  
   2. Configure the following settings.  
      * Event name: Specify a descriptive name for your event notification containing up to 255 characters.  
      * Prefix: Do not set a prefix as the Amazon S3 bucket is meant to be a dedicated bucket for collecting audit logs.  
      * Event types: Select All object create events for the type of event notifications that you want to receive.  
      * Destination: Select SQS queue to send notifications to an SQS queue to be read by a server.  
      * Specify SQS queue: You can either select Choose from your SQS queues and then select the SQS queue, or select Enter SQS queue ARN and specify the ARN in the SQS queue field.  
        You can retrieve your SQS queue ARN by opening another instance of the AWS Management Console in a browser window, and opening the [Amazon SQS Console](https://console.aws.amazon.com/sqs/), and selecting the Amazon SQS that you created. In the Details section, under ARN, click the copy icon (![copy-icon.png][image11])), and paste the ARN in the field.  
        sqs-arn2.png  
   3. Click Save changes.  
      Once the event notification is created, a message indicating that the event notification was successfully created is displayed at the top of the page.  
      If your receive an error when trying to save your changes, you should ensure that the permissions are set up correctly.  
6. Configure access keys for the AWS IAM user that Cortex XSIAM uses for API operations.  
   1. It is the responsibility of the customer’s organization to ensure that the user who performs this task of creating the access key is designated with the relevant permissions. Otherwise, this can cause the process to fail with errors.  
   2. Skip this step if you are using an Assumed Role for Cortex XSIAM.  
   3. Open the [AWS IAM Console](https://console.aws.amazon.com/iam/), and in the navigation pane, select Access management → Users.  
   4. Select the User name of the AWS IAM user.  
   5. Select the Security credentials tab, scroll down to the Access keys section, and click Create access key.  
   6. Click the copy icon next to the Access key ID and Secret access key keys, where you must click Show secret access key to see the secret key and record them somewhere safe before closing the window. You will need to provide these keys when you edit the Access policy of the SQS queue and when setting the AWS Client ID and AWS Client Secret in Cortex XSIAM. If you forget to record the keys and close the window, you will need to generate new keys and repeat this process.  
      For more information, see [Managing access keys for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).  
7. Update the Access policy of your Amazon SQS queue.  
   Skip this step if you are using an Assumed Role for Cortex XSIAM.  
   1. In the [Amazon SQS Console](https://console.aws.amazon.com/sqs/), select the SQS queue that you created in Configure an Amazon Simple Queue Service (SQS).  
   2. Select the Access policy tab, and Edit the Access policy code in the editor window to enable the IAM user to perform operations on the Amazon SQS with permissions to `SQS:ChangeMessageVisibility`, `SQS:DeleteMessage`, and `SQS:ReceiveMessage`. Use this sample code as a guide for defining the `“Sid”: “__receiver_statement”` with the following definitions:  
      * **`“aws:SourceArn”`**: Specify the ARN of the AWS IAM user. You can retrieve the User ARN from the Security credentials tab, which you accessed when configuring access keys for the AWS API user.

**`“Resource”`**: Leave the automatically generated ARN for the SQS queue that is set in the code, which uses the format `“arn:sns:Region:account-id:topic-name”`.  
For more information on granting permissions to publish messages to an SQS queue, see [Granting permissions to publish event notification messages to a destination](https://docs.aws.amazon.com/AmazonS3/latest/userguide/grant-destinations-permissions-to-s3.html).  
{  
  "Version": "2012-10-17",  
  "Statement": \[  
    {  
      "Effect": "Allow",  
      "Principal": {  
        "Service": "s3.amazonaws.com"  
      },  
      "Action": "SQS:SendMessage",  
      "Resource": "\[Leave automatically generated ARN for the SQS queue defined by AWS\]",  
      "Condition": {  
        "ArnLike": {  
          "aws:SourceArn": "\[ARN of your Amazon S3 bucket\]"  
        }  
      }  
    },  
   {  
      "Sid": "\_\_receiver\_statement",  
      "Effect": "Allow",  
      "Principal": {  
        "AWS": "\[Add the ARN for the AWS IAM user\]"  
      },  
      "Action": \[  
        "SQS:ChangeMessageVisibility",  
        "SQS:DeleteMessage",  
        "SQS:ReceiveMessage"  
      \],  
      "Resource": "\[Leave automatically generated ARN for the SQS queue defined by AWS\]"  
    }  
  \]

* }  
8. Configure the Amazon S3 collection in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select Amazon S3, and click Connect.  
   3. Set these parameters, where the parameters change depending on whether you configured an Access Key or Assumed Role.  
      * To provide access to Cortex XSIAM to your logs and perform API operations using a designated AWS IAM user, leave the Access Key option selected. Otherwise, select Assumed Role, and ensure that you Create an Assumed Role for Cortex XSIAM before continuing with these instructions. In addition, when you create an Assumed Role for Cortex XSIAM, ensure that you edit the policy that defines the permissions for the role with the Amazon S3 Bucket ARN and SQS ARN.  
      * SQS URL: Specify the SQS URL, which is the ARN of the Amazon SQS that you configured in the AWS Management Console.  
      * Name: Specify a descriptive name for your log collection configuration.  
      * When setting an Access Key, set these parameters.  
        * AWS Client ID: Specify the Access key ID, which you received when you configured access keys for the AWS IAM user in AWS.  
        * AWS Client Secret: Specify the Secret access key you received when you configured access keys for the AWS IAM user in AWS.  
      * When setting an Assumed Role, set these parameters.  
        * Role ARN: Specify the Role ARN for the Assumed Role you created for in AWS.  
        * External Id: Specify the External Id for the Assumed Role you created for in AWS.  
      * Log Type: Select Audit Logs to configure your log collection to receive audit logs from Amazon S3 via AWS CloudTrail. When configuring audit log collection, the following additional field is displayed for Enhanced Cloud Protection.  
        You can Normalize and enrich audit logs by selecting the checkbox. If selected, Cortex XSIAM stitches Amazon S3 audit logs with other Cortex XSIAM authentication stories across all cloud providers using the same format, which you can query with XQL Search using the `cloud_audit_logs` dataset.  
   4. Click Test to validate access, and then click Enable.  
      Once events start to come in, a green check mark appears underneath the Amazon S3 configuration with the number of logs received.

### Ingest Logs and Data from a GCP Pub/Sub

Abstract

If you use the Pub/Sub messaging service from Global Cloud Platform (GCP), you can send logs and data from GCP to Cortex XSIAM.

If you use the Pub/Sub messaging service from Global Cloud Platform (GCP), you can send logs and data from your GCP instance to Cortex XSIAM. Data from GCP is then searchable in Cortex XSIAM to provide additional information and context to your investigations using the GCP Cortex Query Language (XQL) dataset, which is dependent on the type of GCP logs collected. For example queries, refer to the in-app XQL Library. You can configure a Google Cloud Platform collector to receive generic, flow, audit, or Google Cloud DNS logs. When configuring generic logs, you can receive logs in a Raw, JSON, CEF, LEEF, Cisco, or Corelight format.

You can also configure Cortex XSIAM to normalize different GCP logs as part of the enhanced cloud protection, which you can query with XQL Search using the applicable dataset. Cortex XSIAM can also raise Cortex XSIAM alerts (Analytics, IOC, BIOC, and Correlation Rules) when relevant from GCP logs. While Correlation Rules alerts are raised on non-normalized and normalized logs, Analytics, IOC, and BIOC alerts are only raised on normalized logs.

Enhanced cloud protection provides the following:

* Normalization of cloud logs  
* Cloud logs stitching  
* Enrichment with cloud data  
* Detection based on cloud analytics  
* Cloud-tailored investigations

The following table lists the various GCP log types the XQL datasets you can use to query in XQL Search:

| GCP log type | Dataset | Dataset with normalized data |
| ----- | ----- | ----- |
| Audit logs, including Google Kubernetes Engine (GKE) audit logs | `google_cloud_logging_raw` | `cloud_audit_logs` |
| Generic logs | Log Format types: **CEF** or **`LEEF`**: Automatically detected from either the logs or the user's input in the User Interface. **Cisco**: `cisco_asa_raw` **Corelight**: `corelight_zeek_raw` **JSON or Raw**: `google_cloud_logging_raw` | N/A |
| Google Cloud DNS logs | `google_dns_raw` | `xdr_data`: Once configured, Cortex XSIAM ingests Google Cloud DNS logs as XDR network connection stories, which you can query with XQL Search using the `xdr_data` dataset with the preset called `network_story`. |
| Network flow logs | `google_cloud_logging_raw` | `xdr_data`: Once configured, Cortex XSIAM ingests network flow logs as XDR network connection stories, which you can query with XQL Search using the `xdr_data` dataset with the preset called `network_story`. |

When collecting flow logs, we recommend that you include GKE annotations in your logs, which enable you to view the names of the containers that communicated with each other. GKE annotations are only included in logs if appended manually using the custom metadata configuration in GCP. For more information, see [VPC Flow Logs Overview](https://cloud.google.com/vpc/docs/flow-logs#customizing_metadata_fields). In addition, to customize metadata fields, you must use the gcloud command-line interface or the API. For more information, see [Using VPC Flow Logs](https://cloud.google.com/vpc/docs/using-flow-logs#enabling_vpc_flow_logging_for_an_existing_subnet).

To receive logs and data from GCP, you must first set up log forwarding using a Pub/Sub topic in GCP. You can configure GCP settings using either the GCP web interface or a GCP cloud shell terminal. After you set up your service account in GCP, you configure the Data Collection settings in Cortex XSIAM. The setup process requires the subscription name and authentication key from your GCP instance.

After you set up log collection, Cortex XSIAM immediately begins receiving new logs and data from GCP.

###### Set up log forwarding using the GCP web interface

* In Cortex XSIAM, set up Data Collection.  
  1. Select Settings → Data Sources.  
  2. On the Data Sources page, click Add Data Source, search for and select Google Cloud Platform, and click Connect.  
  3. Specify the Subscription Name that you previously noted or copied.  
  4. Browse to the JSON file containing your authentication key for the service account.  
  5. Select the Log Type as one of the following, where your selection changes the options displayed.  
     * Flow or Audit Logs: When selecting this log type, you can decide whether to normalize and enrich the logs as part of the enhanced cloud protection.  
       * (Optional) You can Normalize and enrich flow and audit logs by selecting the checkbox (default). If selected, Cortex XSIAM ingests the network flow logs as Cortex XSIAM network connection stories, which you can query using XQL Search from the `xdr_dataset` dataset with the preset called `network_story`. In addition, you can configure Cortex XSIAM to normalize GCP audit logs, which you can query with XQL Search using the `cloud_audit_logs` dataset.  
       * The Vendor is automatically set to Google and Product to Cloud Logging, which is not configurable. This means that all GCP data for the flow and audit logs, whether it's normalized or not, can be queried in XQL Search using the `google_cloud_logging_raw` dataset.  
     * Generic: When selecting this log type, you can configure the following settings.  
       * Log Format: Select the log format type as Raw, JSON, CEF, LEEF, Cisco, or Corelight.  
         * CEF or LEEF: The Vendor and Product defaults to Auto-Detect.  
           For a Log Format set to CEF or LEEF, Cortex XSIAM reads events row by row to look for the Vendor and Product configured in the logs. When the values are populated in the event log row, Cortex XSIAM uses these values even if you specified a value in the Vendor and Product fields in the GCP data collector settings. Yet, when the values are blank in the event log row, Cortex XSIAM uses the Vendor and Product that you specified in the GCP data collector settings. If you did not specify a Vendor or Product in the GCP data collector settings, and the values are blank in the event log row, the values for both fields are set to unknown.  
         * Cisco: The following fields are automatically set and not configurable.  
           * Vendor: Cisco  
           * Product: ASA  
         * Cisco data can be queried in XQL Search using the `cisco_asa_raw` dataset.  
         * Corelight: The following fields are automatically set and not configurable.  
           * Vendor: Corelight  
           * Product: Zeek  
         * Corelight data can be queried in XQL Search using the `corelight_zeek_raw` dataset.  
         * Raw or JSON: The following fields are automatically set and are configurable.  
           * Vendor: Google  
           * Product: Cloud Logging  
         * Raw or JSON data can be queried in XQL Search using the `google_cloud_logging_raw` dataset.  
           Cortex XSIAM supports logs in single line format or multiline format. For a JSON format, multiline logs are collected automatically when the Log Format is configured as JSON. When configuring a Raw format, you must also define the Multiline Parsing Regex as explained below.  
       * Vendor: (Optional) Specify a particular vendor name for the GCP generic data collection, which is used in the GCP XQL dataset `<Vendor>_<Product>_raw` that Cortex XSIAM creates as soon as it begins receiving logs.  
       * Product: (Optional) Specify a particular product name for the GCP generic data collection, which is used in the GCP XQL dataset name `<Vendor>_<Product>_raw` that Cortex XSIAM creates as soon as it begins receiving logs.  
       * Multiline Parsing Regex: (Optional) This option is only displayed when the Log Format is set to Raw, where you can set the regular expression that identifies when the multiline event starts in logs with multilines. It is assumed that when a new event begins, the previous one has ended.  
     * Google Cloud DNS: When selecting this log type, you can configure whether to normalize the logs as part of the enhanced cloud protection.  
       * Optional) You can Normalize DNS logs by selecting the checkbox (default). If selected, Cortex XSIAM ingests the Google Cloud DNS logs as Cortex XSIAM network connection stories, which you can query using XQL Search from the `xdr_dataset` dataset with the preset called `network_story`.  
       * The Vendor is automatically set to Google and Product to DNS , which is not configurable. This means that all Google Cloud DNS logs, whether it's normalized or not, can be queried in XQL Search using the `google_dns_raw` dataset.  
  6. Test the provided settings and, if successful, proceed to Enable log collection.  
1. Log in to your GCP account.  
2. Set up log forwarding from GCP to Cortex XSIAM.  
   1. Select Logging → Logs Router.  
   2. Select Create Sink → Cloud Pub/Sub topic, and then click Next.  
   3. To filter only specific types of data, select the filter or desired resource.  
   4. In the Edit Sink configuration, define a descriptive Sink Name.  
   5. Select Sink Destination → Create new Cloud Pub/Sub topic.  
   6. Enter a descriptive Name that identifies the sink purpose for Cortex XSIAM, and then Create.  
   7. Create Sink and then Close when finished.  
3. Create a subscription for your Pub/Sub topic.  
   1. Select the hamburger menu in G Cloud and then select Pub/Sub → Topics.  
   2. Select the name of the topic you created in the previous steps. Use the filters if necessary.  
   3. Create Subscription → Create subscription.  
   4. Enter a unique Subscription ID.  
   5. Choose Pull as the Delivery Type.  
   6. Create the subscription.  
      After the subscription is set up, G Cloud displays statistics and settings for the service.  
   7. In the subscription details, identify and note your Subscription Name.  
      Optionally, use the copy button to copy the name to the clipboard. You will need the name when you configure Collection in Cortex XSIAM.  
4. Create a service account and authentication key.  
   You will use the key to enable Cortex XSIAM to authenticate with the subscription service.  
   1. Select the menu icon, and then select IAM & Admin → Service Accounts.  
   2. Create Service Account.  
   3. Enter a Service account name and then Create.  
   4. Select a role for the account: Pub/Sub → Pub/Sub Subscriber.  
   5. Click Continue → Done.  
   6. Locate the service account by name, using the filters to refine the results, if needed.  
   7. Click the Actions menu identified by the three dots in the row for the service account and then Create Key.  
   8. Select JSON as the key type, and then Create.  
      After you create the service account key, G Cloud automatically downloads it.  
5. After Cortex XSIAM begins receiving information from the GCP Pub/Sub service, you can use the XQL Query language to search for specific data.

###### Set up log forwarding using the GCP cloud shell terminal

* In Cortex XSIAM, set up Data Collection.  
  1. Select Settings → Data Sources.  
  2. On the Data Sources page, click Add Data Source, search for and select Google Cloud Platform, and click Connect.  
  3. Specify the Subscription Name that you previously noted or copied.  
  4. Browse to the JSON file containing your authentication key for the service account.  
  5. Select the Log Type as one of the following, where your selection changes the options displayed.  
     * Flow or Audit Logs: When selecting this log type, you can decide whether to normalize and enrich the logs as part of the enhanced cloud protection.  
       * (Optional) You can Normalize and enrich flow and audit logs by selecting the checkbox (default). If selected, Cortex XSIAM ingests the network flow logs as Cortex XSIAM network connection stories, which you can query using XQL Search from the `xdr_dataset` dataset with the preset called `network_story`. In addition, you can configure Cortex XSIAM to normalize GCP audit logs, which you can query with XQL Search using the `cloud_audit_logs` dataset.  
       * The Vendor is automatically set to Google and Product to Cloud Logging, which is not configurable. This means that all GCP data for the flow and audit logs, whether it's normalized or not, can be queried in XQL Search using the `google_cloud_logging_raw` dataset.  
     * Generic: When selecting this log type, you can configure the following settings.  
       * Log Format: Select the log format type as Raw, JSON, CEF, LEEF, Cisco, or Corelight.  
         * CEF or LEEF: The Vendor and Product defaults to Auto-Detect.  
           For a Log Format set to CEF or LEEF, Cortex XSIAM reads events row by row to look for the Vendor and Product configured in the logs. When the values are populated in the event log row, Cortex XSIAM uses these values even if you specified a value in the Vendor and Product fields in the GCP data collector settings. Yet, when the values are blank in the event log row, Cortex XSIAM uses the Vendor and Product that you specified in the GCP data collector settings. If you did not specify a Vendor or Product in the GCP data collector settings, and the values are blank in the event log row, the values for both fields are set to unknown.  
         * Cisco: The following fields are automatically set and not configurable.  
           * Vendor: Cisco  
           * Product: ASA  
         * Cisco data can be queried in XQL Search using the `cisco_asa_raw` dataset.  
         * Corelight: The following fields are automatically set and not configurable.  
           * Vendor: Corelight  
           * Product: Zeek  
         * Corelight data can be queried in XQL Search using the `corelight_zeek_raw` dataset.  
         * Raw or JSON: The following fields are automatically set and are configurable.  
           * Vendor: Google  
           * Product: Cloud Logging  
         * Raw or JSON data can be queried in XQL Search using the `google_cloud_logging_raw` dataset.  
           Cortex XSIAM supports logs in single line format or multiline format. For a JSON format, multiline logs are collected automatically when the Log Format is configured as JSON. When configuring a Raw format, you must also define the Multiline Parsing Regex as explained below.  
       * Vendor: (Optional) Specify a particular vendor name for the GCP generic data collection, which is used in the GCP XQL dataset `<Vendor>_<Product>_raw` that Cortex XSIAM creates as soon as it begins receiving logs.  
       * Product: (Optional) Specify a particular product name for the GCP generic data collection, which is used in the GCP XQL dataset name `<Vendor>_<Product>_raw` that Cortex XSIAM creates as soon as it begins receiving logs.  
       * Multiline Parsing Regex: (Optional) This option is only displayed when the Log Format is set to Raw, where you can set the regular expression that identifies when the multiline event starts in logs with multilines. It is assumed that when a new event begins, the previous one has ended.  
     * Google Cloud DNS: When selecting this log type, you can configure whether to normalize the logs as part of the enhanced cloud protection.  
       * Optional) You can Normalize DNS logs by selecting the checkbox (default). If selected, Cortex XSIAM ingests the Google Cloud DNS logs as Cortex XSIAM network connection stories, which you can query using XQL Search from the `xdr_dataset` dataset with the preset called `network_story`.  
       * The Vendor is automatically set to Google and Product to DNS , which is not configurable. This means that all Google Cloud DNS logs, whether it's normalized or not, can be queried in XQL Search using the `google_dns_raw` dataset.  
  6. Test the provided settings and, if successful, proceed to Enable log collection.  
1. Launch the GCP cloud shell terminal or use your preferred shell with gcloud installed.  
   gcp-cli.png

Define your project ID.  
gcloud config set project \<PROJECT\_ID\>

2.                     

Create a Pub/Sub topic.  
gcloud pubsub topics create \<TOPIC\_NAME\>

3.                     

Create a subscription for this topic.  
gcloud pubsub subscriptions create \<SUBSCRIPTION\_NAME\> \--topic=\<TOPIC\_NAME\>

4.                       
    Note the subscription name you define in this step as you will need it to set up log ingestion from Cortex XSIAM.

Create a logging sink.  
During the logging sink creation, you can also define additional log filters to exclude specific logs. To filter logs, supply the optional parameter `--log-filter=<LOG_FILTER>`  
gcloud logging sinks create \<SINK\_NAME\> pubsub.googleapis.com/projects/\<PROJECT\_ID\>/topics/\<TOPIC\_NAME\> \--log-filter=\<LOG\_FILTER\>

5.                       
    If setup is successful, the console displays a summary of your log sink settings:  
   Created \[https://logging.googleapis.com/v2/projects/PROJECT\_ID/sinks/SINK\_NAME\]. Please remember to grant \`serviceAccount:LOGS\_SINK\_SERVICE\_ACCOUNT\` \\ the Pub/Sub Publisher role on the topic. More information about sinks can be found at /logging/docs/export/configure\_export  
6. Grant log sink service account to publish to the new topic.  
   Note the `serviceAccount` name from the previous step and use it to define the service for which you want to grant publish access.  
   gcloud pubsub topics add-iam-policy-binding \<TOPIC\_NAME\> \--member serviceAccount:\<LOGS\_SINK\_SERVICE\_ACCOUNT\> \--role=roles/pubsub.publisher  
7. Create a service account.  
   For example, use cortex-xdr-sa as the service account name and Cortex XSIAM Service Account as the display name.  
   gcloud iam service-accounts create \<SERVICE\_ACCOUNT\> \--description="\<DESCRIPTION\>" \--display-name="\<DISPLAY\_NAME\>"  
8. Grant the IAM role to the service account.  
   gcloud pubsub subscriptions add-iam-policy-binding \<SUBSCRIPTION\_NAME\> \--member serviceAccount:\<SERVICE\_ACCOUNT\>@\<PROJECT\_ID\>.iam.gserviceaccount.com \--role=roles/pubsub.subscriber  
9. Create a JSON key for the service account.  
   You will need the JSON file to enable Cortex XSIAM to authenticate with the GCP service. Specify the file destination and filename using a .json extension.  
   gcloud iam service-accounts keys create \<OUTPUT\_FILE\> \--iam-account \<SERVICE\_ACCOUNT\>@\<PROJECT\_ID\>.iam.gserviceaccount.com  
10. After Cortex XSIAM begins receiving information from the GCP Pub/Sub service, you can use the XQL Query language to search for specific data.

### Ingest Logs and Data from Google Workspace

Abstract

Ingest logs and data from Google Workspace for use in Cortex XSIAM.

Cortex XSIAM can ingest the following types of data from Google Workspace, where most of the data is collected as audit events from various Google reports, using the Google Workspace data collector.

* Google Chrome  
* Admin Console  
* Google Chat  
* Enterprise Groups  
* Login  
* Rules  
* Google drive  
* Token  
* User Accounts  
* SAML  
* Alerts  
* Emails—Requires a compliance mailbox to ingest email data (not email reports).  
  * All message details except email headers and email content (`payload.body`, `payload.parts`, and `snippet`).  
  * Attachment details, when Get Attachment Info is selected, includes file name, size, and hash calculation.

The following Google APIs are required to collect the different types of data from Google Workspace.

* For all data types, except emails: [Admin SDK API](https://developers.google.com/admin-sdk).  
* For all data types, except alerts and emails: [Admin Reports API](https://developers.google.com/admin-sdk/reports/reference/rest) (part of Admin SDK API).  
  For all types of data collected via the Admin Reports API, except alerts and emails, the log events are collected with a preset lag time as reported by Google Workspace. For more information on these lag times for the different types of data, see [Google Workspace Data retention and lag times](https://support.google.com/a/answer/7061566?hl=en).  
* Alerts require implementing an additional API: [Alert Center API](https://developers.google.com/admin-sdk/alertcenter) (part of Admin SDK API).  
* Emails require implementing the [Gmail API](https://developers.google.com/gmail/api).

To receive logs from Google Workspace for any of the data types except emails, you must first enable the Google Workspace Admin SDK API with a user with access to the Admin SDK Reports API. For emails, you must set up a compliance email account as explained in the prerequisite steps below and then enable the Google Workspace Gmail API. Once implemented, you can then configure the Data Sources settings in Cortex XSIAM. After you set up data collection, Cortex XSIAM begins receiving new logs and data from the source.

When Cortex XSIAM begins receiving logs, the app creates a new dataset for the different types of data that you are collecting, which you can use to initiate XQL Search queries. For example queries, refer to the in-app XQL Library. For all logs, Cortex XSIAM can raise Cortex XSIAM alerts for Correlation Rules only, when relevant from Google Workspace logs.

For the different types of data you can collect using the Google Workspace data collector, the following table lists the different datasets, vendors, and products automatically configured, and whether the data is normalized.

| Data type | Dataset | Vendor | Product | Normalized data |
| ----- | ----- | ----- | ----- | ----- |
| Google Chrome | `google_workspace_chrome_raw` | Google | Workspace Chrome | — |
| Admin console | `google_workspace_admin_console_raw` | Google | Workspace Admin Console | When relevant, Cortex XSIAM normalizes Admin Console audit logs into authentication stories. All SaaS audit logs are collected in a dataset called `saas_audit_logs` and specific relevant events are collected in the `authentication_story` preset for the `xdr_data` dataset. |
| Google Chat | `google_workspace_chat_raw` | Google | Workspace Chat | — |
| Enterprise groups | `google_workspace_enterprise_groups_raw` | Google | Workspace Enterprise Groups | When relevant, Cortex XSIAM normalizes Enterprise Group audit logs into authentication stories. All SaaS audit logs are collected in a dataset called `saas_audit_logs` and specific relevant events are collected in the `authentication_story` preset for the `xdr_data` dataset. |
| Login | `google_workspace_login_raw` | Google | Workspace Login | When relevant, Cortex XSIAM normalizes Login audit logs into authentication stories. All SaaS audit logs are collected in a dataset called `saas_audit_logs` and specific relevant events are collected in the `authentication_story` preset for the `xdr_data` dataset. |
| Rules | `google_workspace_rules_raw` | Google | Workspace Rules | When relevant, Cortex XSIAM normalizes Rules audit logs into authentication stories. All SaaS audit logs are collected in a dataset called `saas_audit_logs` and specific relevant events are collected in the `authentication_story` preset for the `xdr_data` dataset. |
| Google Drive | `google_workspace_drive_raw` | Google | Workspace Drive | When relevant, Cortex XSIAM normalizes Google drive audit logs into authentication stories. All SaaS audit logs are collected in a dataset called `saas_audit_logs` and specific relevant events are collected in the `authentication_story` preset for the `xdr_data` dataset. |
| Token | `google_workspace_token_raw` | Google | Workspace Token | When relevant, Cortex XSIAM normalizes Token audit logs into authentication stories. All SaaS audit logs are collected in a dataset called `saas_audit_logs` and specific relevant events are collected in the `authentication_story` preset for the `xdr_data` dataset. |
| User accounts | `google_workspace_user_accounts_raw` | Google | Workspace User Accounts | — |
| SAML | `google_workspace_saml_raw` | Google | Workspace SAML | When relevant, Cortex XSIAM normalizes SAML audit logs into authentication stories. All SaaS audit logs are collected in a dataset called `saas_audit_logs` and specific relevant events are collected in the `authentication_story` preset for the `xdr_data` dataset. |
| Alerts | `google_workspace_alerts_raw` | Google | Workspace Alerts | — |
| Emails | `google_gmail_raw` | Google | Gmail | — |

**Prerequisite Steps**

Be sure you do the following tasks before you begin configuring data collection from Google Workspace using the instructions detailed below.

* When configuring data collection for all data types except emails, you need to complete the Google Workspace Reports API Prerequisites to set up the Google Workspace Admin SDK environment. This entails completing the instructions for **Set up the basics** and **Set up a Google API Console project** *without* activating the Reports API service as this will be explained in greater detail in the task below. For more information on these Google Workspace prerequisite steps, see [Reports API Prerequisites](https://developers.google.com/admin-sdk/reports/v1/guides/prerequisites).  
* When you only want to collect Google Workspace alerts without configuring any other data types, you need to set up a [Cloud Platform project](https://developers.google.com/admin-sdk/alertcenter/quickstart/java).  
* Before you can collect Google emails, you need to set up the following:  
  * A compliance email account.  
  * The organization’s Google Workspace account administrator can now set up a BCC to this compliance email account for all incoming and outgoing emails of any user in the organization.  
    1. Login to the [Admin direct routing URL](https://admin.google.com/ac/apps/gmail/routing) in Google Workspace for the user account that you want to configure.  
    2. Double-click Routing, and set the following parameters in the Add setting dialog.  
       * Routing: Configure the compliance email account that you want to receive a BCC for emails from this user account using the format `BCC TO <compliance email>`. For example, `BCC TO admin@organization.com`.  
       * Select Inbound and Outbound to ensure all incoming and outgoing emails are sent.  
       * (Optional) To configure another email address to receive a BCC for emails from this account, select Add more recipients in the Also deliver to section, and then click Add.  
       * Click Show options, and from the list displayed select Account types to affect → Users.  
       * Save your changes.  
* This configuration ensures to forward every message sent to a user account to a defined compliance mailbox. After the Google Workspace data collector ingests the emails, they are deleted from the compliance mailbox to prevent email from building up over time (nothing touches the actual users’ mailboxes).  
  * Spam emails from the compliance email account, and from all other monitored email accounts, are not collected.  
  * Any draft emails written in the compliance email account are collected by the Google Workspace data collector, and are then deleted even if the email was never sent.

To set up the Google Workspace integration:

1. Complete the applicable prerequisite steps for the types of data you want to collect from Google Workspace.  
2. Log in to your [GCP account](https://console.cloud.google.com/).  
3. Perform Google Workspace Domain-Wide Delegation of Authority when collecting any type of data from Google Workspace except Google Emails.  
   When collecting any type of data from Google Workspace except emails, you need to set up Google Workspace enterprise applications to access users’ data without any manual authorization. This is performed by following these steps.  
   For more information on the entire process, see [Perform Google Workspace Domain-Wide Delegation of Authority](https://developers.google.com/admin-sdk/reports/v1/guides/delegation).  
   1. Enable the Admin SDK API to create a service account and set credentials for this service account.  
      As you complete this step, you need to gather information related to your service account, including the Client ID, Private key file, and Email address, which you will need to use later on in this task.  
      * Select the menu icon → APIs & Services → Library.  
      * Search for the **`Admin SDK API`**, and select the API from the results list.  
      * Enable the Admin SDK API.  
      * Select APIs & Services → Credentials.  
      * Select \+ CREATE CREDENTIALS → Service account.  
      * Set the following Service account details in the applicable fields.  
        * Specify a service account name. This name is automatically used to populate the following field as the service account ID, where the name is changed to lowercase letters and all spaces are changed to hyphens.  
        * Specify the service account ID, where you can either leave the default service account ID or add a new one. This service account ID is used to set the service account email using the following format: `<id>@<project name>.iam.gserviceaccount.com`.  
        * (Optional) Specify a service account description.  
      * CREATE AND CONTINUE.  
      * (Optional) Decide whether you want to Grant this service account access to project or Grant users access to this service account.  
      * Click Done.  
      * Select your newly created Service Account from the list.  
      * Create a service account private key and download the private key file as a JSON file.  
        In the Keys tab, select ADD KEY → Create new key, leave the default Key type set to JSON, and CREATE the private key. Once you’ve downloaded the new private key pair to your machine, ensure that you store it in a secure location, because it’s the only copy of this key. You will need to browse to this JSON file when configuring the Google Workplace data collector in Cortex XSIAM.  
   2. When collecting alerts, enable the Alert Center API to create a service account and set credentials for this service account.  
      When collecting Google Workspace alerts with other types of data, except emails, you need to configure a service account in Google with the applicable permissions to collect events from the Google Reports API and alerts from the Alert Center API. If you prefer to use different service accounts to collect events and alerts separately, you'll need to create two service accounts with different instances of the Google Workspace data collector. One instance to collect events with a certain service account, and another instance to collect alerts using another service account. The instructions below explain how to set up one Google Workspace instance to collect both event and alerts.  
      * Select the menu icon → APIs & Services → Library.  
      * Search for the **`Alert Center API`**, and select the API from the results list.  
      * Enable the Alert Center API.  
      * Select APIs & Services → Credentials.  
      * Select the same service account in the Service Accounts section that you created for the Admin SDK API above.  
   3. Delegate domain-wide authority to your service account with the Admin Reports API and Alert Center API scopes.  
      * Open the [Google Admin Console](https://admin.google.com/).  
      * Select Security → Access and data control → API controls.  
      * Scroll down to the Domain wide delegation section, and select MANAGE DOMAIN WIDE DELEGATION.  
      * Click Add new.  
      * Set the following settings to define permissions for the Admin SDK API.  
        * Client ID: Specify the service account’s Unique ID, which you can obtain from the [Service accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts) by clicking the email of the service account to view further details. When creating a single Google Workspace data collector instance to collect both events and alert data, provide the same service account ID as the Admin SDK API.  
        * In the OAuth scopes (comma-delimited) field, paste in the first of the two Admin Reports API scopes: `https://www.googleapis.com/auth/admin.reports.audit.readonly`  
        * In the following OAuth scopes (comma-delimited) field, paste in the second Admin Reports API scope: `https://www.googleapis.com/auth/admin.reports.usage.readonly`  
          For more information on the Admin Reports API scopes, see [OAuth 2.0 Scopes for Google APIs](https://developers.google.com/identity/protocols/oauth2/scopes).  
        * When collecting alerts, add the following Alert Center API scope: `https://www.googleapis.com/auth/apps.alerts`  
      * Authorize the domain-wide authority to your service account.  
        This ensures that your service account now has domain-wide access to the Google Admin SDK Reports API and Google Workspace Alert Center API, if configured, for all of the users of your domain.  
4. Enable the Gmail API to collect Google emails.  
   When you are configuring the Google Workspace data collector to collect Google emails, the instruction differ depending on whether you are configuring the collection along with other types of data with the Admin SDK API already set up or you are configuring the collection to only include emails using only the Gmail API. The steps below explain both scenarios.  
   1. Select the menu icon → APIs & Services → Library.  
   2. Search for the `Gmail API`, and select the API from the results list.  
   3. Enable the Gmail API.  
   4. Select APIs & Services → Credentials.  
      The instructions for setting up credentials differ depending on whether you are setting up the Gmail API together with the Admin SDK API as you are collecting other data types, or you are configuring collection for emails only with the Gmail API.  
      * When you’ve already set up the Admin SDK API, verify that the same [Service Account](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#UUID-6c0f6c99-c933-d494-f4d5-343d3779818f_ServiceAccount) that you configured for the Admin SDK API is listed, and continue on to the next step.  
      * When you’re only collecting Google emails without the Admin SDK API, complete these steps.  
        * Select \+ CREATE CREDENTIALS → Service account.  
        * Set the following Service account details in the applicable fields.  
          \-Specify a service account name. This name is automatically used to populate the following field as the service account ID, where the name is changed to lowercase letters and all spaces are changed to hyphens.  
          \-Specify the service account ID, where you can either leave the default service account ID or add a new one. This service account ID is used to set the service account email using the following format: `<id>@<project name>.iam.gserviceaccount.com`.  
          \-(Optional) Specify a service account description.  
        * CREATE AND CONTINUE.  
        * (Optional) Decide whether you want to Grant this service account access to project or Grant users access to this service account.  
        * Click Done.  
        * Select your newly created Service Account from the list.  
        * Create a service account private key and download the private key file as a JSON file.  
          In the Keys tab, select ADD KEY → Create new key, leave the default Key type set to JSON, and CREATE the private key. Once you’ve downloaded the new private key pair to your machine, ensure that you store it in a secure location as it’s the only copy of this key. You will need to browse to this JSON file when configuring the Google Workplace data collector in Cortex XSIAM .  
   5. Delegate domain-wide authority to your service account with the Gmail API scopes.  
      * Open the [Google Admin Console](https://admin.google.com/).  
      * Select Security → Access and data control → API controls.  
      * Scroll down to the Domain wide delegation section, and select MANAGE DOMAIN WIDE DELEGATION.  
        This step explains how the following Gmail API scopes are added.  
        * `https://mail.google.com/`  
        * `https://www.googleapis.com/auth/gmail.addons.current.action.compose`  
        * `https://www.googleapis.com/auth/gmail.addons.current.message.action`  
        * `https://www.googleapis.com/auth/gmail.addons.current.message.metadata`  
        * `https://www.googleapis.com/auth/gmail.addons.current.message.readonly`  
        * `https://www.googleapis.com/auth/gmail.compose`  
        * `https://www.googleapis.com/auth/gmail.insert`  
        * `https://www.googleapis.com/auth/gmail.labels`  
        * `https://www.googleapis.com/auth/gmail.metadata`  
        * `https://www.googleapis.com/auth/gmail.modify`  
        * `https://www.googleapis.com/auth/gmail.readonly`  
        * `https://www.googleapis.com/auth/gmail.send`  
        * `https://www.googleapis.com/auth/gmail.settings.basic`  
        * `https://www.googleapis.com/auth/gmail.settings.sharing`  
          For more information on the Gmail API scopes, see [OAuth 2.0 Scopes for Google APIs](https://developers.google.com/identity/protocols/oauth2/scopes).  
      * The instructions differ depending on whether you are setting up the Gmail API together with the Admin SDK API as you are collecting other data types, or you are configuring collection for emails only with the Gmail API.  
        * When you’ve already set up the Admin SDK API, Edit the same [Service Account](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#UUID-6c0f6c99-c933-d494-f4d5-343d3779818f_ServiceAccount) that you configured for the Admin SDK API, and add the Gmail API scopes listed above.  
        * When you’re only collecting Google emails without the Admin SDK API, click Add New, and set the following settings to define permissions for the Admin SDK API.  
          \-Client ID—Specify the service account’s Unique ID, which you can obtain from the [Service accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts) by clicking the email of the service account to view further details.  
          In the OAuth scopes (comma-delimited) field, paste in the first of the Gmail API scopes listed above, and continue adding in the rest of the scopes.  
          Authorize the domain-wide authority to your service account.  
          This ensures that your service account now has domain-wide access to the Google Gmail API for all of the users of your domain.  
5. Prepare your service account to impersonate a user with access to the Admin SDK Reports API when collecting any type of data from Google Workspace except Google emails.  
   Only users with access to the Admin APIs can access the Admin SDK Reports API. Therefore, your service account needs to be set up to impersonate one of these users to access the Admin SDK Reports API. This means that when collecting any type of data from Google Workspace except Google emails, you need to designate a user whose Roles permissions are set to access reports, where Security → Reports is selected. This user’s email will be required when configuring the Google Workspace data collector in Cortex XSIAM.  
   1. In the [Google Admin Console](https://admin.google.com/), select Directory → Users.  
   2. From the list of users listed, select the user configured with the necessary permissions in Admin roles and privileges to view reports, such as a Super Admin, that you want to set up your service account to impersonate.  
   3. Record the email of this user as you will need it in Cortex XSIAM .  
6. In Cortex XSIAM, select Settings → Data Sources.  
7. On the Data Sources page, click Add Data Source, search for and select Google Workspace, and click Connect.  
8. Integrate the applicable Google Workspace service with Cortex XSIAM.  
   1. Specify a descriptive Name for your log collection integration.  
   2. Browse to the JSON file containing your [service account key](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#UUID-6c0f6c99-c933-d494-f4d5-343d3779818f_ServiceAccount) Credentials for the Google Workspace Admin SDK API that you enabled. If you’re only collecting Google emails, ensure that you Browse to the JSON file containing your [service account private key](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#UUID-6c0f6c99-c933-d494-f4d5-343d3779818f_N1667813723835) Credentials for the Gmail API that you enabled.  
   3. Select the types of data that you want to Collect from Google Workspace.  
      * Google Chrome: [Chrome browser and Chrome OS events](https://developers.google.com/admin-sdk/reports/v1/appendix/activity/chrome) included in the Chrome activity reports.  
      * Admin Console: Account information about different types of [administrator activity events](https://developers.google.com/admin-sdk/reports/v1/appendix/activity/admin-event-names) included in the Admin console application's activity reports.  
      * Google Chat: [Chat activity events](https://developers.google.com/admin-sdk/reports/v1/appendix/activity/chat) included in the Chat activity reports.  
      * Enterprise Groups: [Enterprise group activity events](https://developers.google.com/admin-sdk/reports/v1/appendix/activity/groups-enterprise) included in the Enterprise Groups activity reports.  
      * Login: Account information about different types of [login activity events](https://developers.google.com/admin-sdk/reports/v1/appendix/activity/login) included in the Login application's activity reports.  
      * Rules: [Rules activity events](https://developers.google.com/admin-sdk/reports/v1/appendix/activity/rules) included in the Rules activity report.  
      * Google drive: [Google Drive activity events](https://developers.google.com/admin-sdk/reports/v1/appendix/activity/drive) included in the Google Drive application's activity reports.  
      * Token: [Token activity events](https://developers.google.com/admin-sdk/reports/v1/appendix/activity/token) included in the Token application's activity reports.  
      * User Accounts: Account information about different types of [User Accounts activity events](https://developers.google.com/admin-sdk/reports/v1/appendix/activity/user-accounts) included in the User Accounts application's activity reports.  
      * SAML: [SAML activity events](https://developers.google.com/admin-sdk/reports/v1/appendix/activity/saml) included in the SAML activity report.  
      * Alerts: Alerts from the Alert Center API beta version, which is still subject to change.  
      * Emails: Collects email data (not emails reports). All message details except email headers and email content (`payload.body`, `payload.parts`, and `snippet`).  
        For more information about the events collected from the various Google Reports, see [Google Workspace Reports API Documentation](https://developers.google.com/admin-sdk/reports/reference/rest/v1/activities/list#ApplicationName).  
   4. For all options selected, except Emails, you must specify the Service Account Email. This is the email account of the user with access to the Admin SDK Reports API that you [prepared your service account to impersonate](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#UUID-6c0f6c99-c933-d494-f4d5-343d3779818f_N1667813918059).  
      When selecting Emails, configure the following.  
      * Audit Email Account: Specify the email address for the [compliance mailbox](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#UUID-6c0f6c99-c933-d494-f4d5-343d3779818f_emailPrereq) that you set up.  
      * Get Attachment Info from the ingested email, which includes file name, size, and hash calculation.  
   5. Test the connection settings.  
      To test the connection, you must select one or more log types. Cortex XSIAM then tests the connection settings for the selected log types.  
   6. If successful, Enable Google Workspace log collection.

### Ingest Logs from Microsoft Azure Event Hub

Abstract

Ingest logs from Microsoft Azure Event Hub with an option to ingest audit logs to use in Cortex XSIAM authentication stories.

Cortex XSIAM can ingest different types of data from Microsoft Azure Event Hub using the Microsoft Azure Event Hub data collector. To receive logs from Azure Event Hub, you must configure the Data Sources settings in Cortex XSIAM based on your Microsoft Azure Event Hub configuration. After you set up data collection, Cortex XSIAM begins receiving new logs and data from the source.

When Cortex XSIAM begins receiving logs, the app creates a new dataset (`MSFT_Azure_raw`) that you can use to initiate XQL Search queries. For example, queries refer to the in-app XQL Library. For enhanced cloud protection, you can also configure Cortex XSIAM to normalize Azure Event Hub audit logs, including Azure Kubernetes Service (AKS) audit logs, with other Cortex XSIAM authentication stories across all cloud providers using the same format, which you can query with XQL Search using the `cloud_audit_logs` dataset. For logs that you do not configure Cortex XSIAM to normalize, you can change the default dataset. Cortex XSIAM can also raise Cortex XSIAM alerts (Analytics, IOC, BIOC, and Correlation Rules) when relevant from Azure Event Hub logs. While Correlation Rules alerts are raised on non-normalized and normalized logs, Analytics, IOC, and BIOC alerts are only raised on normalized logs.

Enhanced cloud protection provides:

* Normalization of cloud logs  
* Cloud logs stitching  
* Enrichment with cloud data  
* Detection based on cloud analytics  
* Cloud-tailored investigations  
* Misconfiguration of Event Hub resources could cause ingestion delays.  
* In an existing Event Hub integration, do not change the mapping to a different Event Hub.  
* Do not use the same Event Hub for more than two purposes.

The following table provides a brief description of the different types of Azure audit logs you can collect.

For more information on Azure Event Hub audit logs, see [Overview of Azure platform logs](https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/platform-logs-overview).

| Type of data | Description |
| ----- | ----- |
| Activity logs | Retrieves events related to the operations on each Azure resource in the subscription from the outside in addition to updates on Service Health events. These logs are from the management plane. |
| Azure Active Directory (AD) Activity logs and Azure Sign-in logs | Contain the history of sign-in activity and audit trail of changes made in Azure AD for a particular tenant. Even though you can collect Azure AD Activity logs and Azure Sign-in logs using the Azure Event Hub data collector, we recommend using the Microsoft 365 data collector, because it is easier to configure. In addition, ensure that you don't configure both collectors to collect the same types of logs, because if you do so, you will be creating duplicate data in Cortex XSIAM. |
| Resource logs, including AKS audit logs | Retrieves events related to operations that were performed within an Azure resource. These logs are from the data plane. |

If you want to ingest raw Microsoft Defender for Endpoint events, use the Microsoft Defender log collector. For more information, see [Ingest raw EDR events from Microsoft Defender for Endpoint](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-E30SPrsh~A1Jt8Nm79uiwg).

Ensure that you do the following tasks before you begin configuring data collection from Azure Event Hub.

* Before you set up an Azure Event Hub, calculate the quantity of data that you expect to send to Cortex XSIAM, taking into account potential data spikes and potential increases in data ingestion, because partitions cannot be modified after creation. Use this information to ascertain the optimal number of partitions and Throughput Units (for Azure Basic or Standard) or Processing Units (for Azure Premium). Configure your Event Hub accordingly.  
* Create an Azure Event Hub. We recommend using a dedicated Azure Event Hub for this Cortex XSIAM integration. For more information, see [Quickstart: Create an event hub using Azure portal](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-create).  
* Each partition can support a throughput of up to 1 MB/s.  
* Ensure the format for the logs you want collected from the Azure Event Hub is either JSON or raw.

Configure the Azure Event Hub collection in Cortex XSIAM:

1. In the Microsoft Azure console, open the Event Hubs page, and select the Azure Event Hub that you created for collection in Cortex XSIAM.  
2. Record the following parameters from your configured event hub, which you will need when configuring data collection in Cortex XSIAM.  
   1. Your event hub’s consumer group.  
      * Select Entities → Event Hubs, and select your event hub.  
      * Select Entities → Consumer groups, and select your event hub.  
      * In the Consumer group table, copy the applicable value listed in the Name column for your Cortex XSIAM data collection configuration.  
   2. Your event hub’s connection string for the designated policy.  
      * Select Settings → Shared access policies.  
      * In the Shared access policies table, select the applicable policy.  
      * Copy the Connection string-primary key.  
   3. Your storage account connection string required for partitions lease management and checkpointing in Cortex XSIAM.  
      * Open the Storage accounts page, and either create a new storage account or select an existing one, which will contain the storage account connection string.  
      * Select Security \+ networking → Access keys, and click Show keys.  
      * Copy the applicable Connection string.  
3. Configure diagnostic settings for the relevant log types you want to collect and then direct these diagnostic settings to the designated Azure Event Hub.  
   1. Open the Microsoft Azure console.  
   2. Your navigation is dependent on the type of logs you want to configure.

| Log type | Navigation path |
| :---- | :---- |
| Activity logs | Select Azure services → Activity log → Export Activity Logs, and \+Add diagnostic setting. |
| Azure AD Activity logs and Azure Sign-in logs | Select Azure services → Azure Active Directory. Select Monitoring → Diagnostic settings, and \+Add diagnostic setting. |
| Resource logs, including AKS audit logs | Search for Monitor, and select Settings → Diagnostic settings. From your list of available resources, select the resource that you want to configure for log collection, and then select \+Add diagnostic setting.For every resource that you want to confiure, you'll have to repeat this step, or use [Azure policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview) for a general configuration. |

   3.   
      Set the following parameters:  
      * Diagnostic setting name: Specify a name for your Diagnostic setting.  
      * Logs Categories/Metrics: The options listed are dependent on the type of logs you want to configure. For Activity logs and Azure AD logs and Azure Sign-in logs, the option is called Logs Categories, and for Resource logs it's called Metrics.

| Log type | Log categories/metrics |
| :---- | :---- |
| Activity logs | Select from the list of applicable Activity log categories, the ones that you want to configure your designated resource to collect. We recommend selecting all of the options. Administrative Security ServiceHealth Alert Recommendation Policy Autoscale ResourceHealth |
| Azure AD Activity logs and Azure Sign-in logs | Select from the list of applicable Azure AD Activity and Azure Sign-in Logs Categories, the ones that you want to configure your designated resource to collect. You can select any of the following categories to collect these types of Azure logs. Azure AD Activity logs: AuditLogs Azure Sign-in logs: SignInLogs NonInteractiveUserSignInLogs ServicePrincipalSignInLogs ManagedIdentitySignInLogs ADFSSignInLogs There are additional log categories displayed. We recommend selecting all the available options. |
| Resource logs, including AKS audit logs | The list displayed is dependent on the resource that you selected. We recommend selecting all the options available for the resource. |

      *   
        Destination details: Select Stream to event hub, where additional parameters are displayed that you need to configure. Ensure that you set the following parameters using the same settings for the Azure Event Hub that you created for the collection.  
        * Subscription: Select the applicable Subscription for the Azure Event Hub.  
        * Event hub namespace: Select the applicable Subscription for the Azure Event Hub.  
        * (Optional) Event hub name: Specify the name of your Azure Event Hub.  
        * Event hub policy: Select the applicable Event hub policy for your Azure Event Hub.  
   4. Save your settings.  
4. Configure the Azure Event Hub collection in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select Azure Event Hub, and click Connect.  
   3. Set these parameters.  
      * Name: Specify a descriptive name for your log collection configuration.  
      * Event Hub Connection String: Specify your event hub’s connection string for the designated policy.  
      * Storage Account Connection String: Specify your storage account’s connection string for the designated policy.  
      * Consumer Group: Specify your event hub’s consumer group.  
      * Log Format: Select the log format for the logs collected from the Azure Event Hub as Raw, JSON, CEF, LEEF, Cisco-asa, or Corelight.  
        When you Normalize and enrich audit logs, the log format is automatically configured. As a result, the Log Format option is removed and is no longer available to configure (default).  
        * CEF or LEEF: The Vendor and Product defaults to Auto-Detect.  
          For a Log Format set to CEF or LEEF, Cortex XSIAM reads events row by row to look for the Vendor and Product configured in the logs. When the values are populated in the event log row, Cortex XSIAM uses these values even if you specified a value in the Vendor and Product fields in the Azure Event Hub data collector settings. Yet, when the values are blank in the event log row, Cortex XSIAM uses the Vendor and Product that you specified in the Azure Event Hub data collector settings. If you did not specify a Vendor or Product in the Azure Event Hub data collector settings, and the values are blank in the event log row, the values for both fields are set to unknown.  
        * Cisco-asa: The following fields are automatically set and not configurable.  
          * Vendor: Cisco  
          * Product: ASA  
        * Cisco data can be queried in XQL Search using the `cisco_asa_raw` dataset.  
        * Corelight: The following fields are automatically set and not configurable.  
          * Vendor: Corelight  
          * Product: Zeek  
        * Corelight data can be queried in XQL Search using the `corelight_zeek_raw` dataset.  
        * Raw or JSON: The following fields are automatically set and are configurable.  
          * Vendor: Msft  
          * Product: Azure  
        * Raw or JSON data can be queried in XQL Search using the `msft_azure_raw` dataset.  
      * Vendor and Product: Specify the Vendor and Product for the type of logs you are ingesting.  
        The Vendor and Product are used to define the name of your Cortex Query Language (XQL) dataset (`<vendor>_<product>_raw`). The Vendor and Product values vary depending on the Log Format selected. To uniquely identify the log source, consider changing the values if the values are configurable.  
        When you Normalize and enrich audit logs, the Vendor and Product fields are automatically configured, so these fields are removed as available options (default).  
      * Normalize and enrich audit logs: (Optional) For enhanced cloud protection, you can Normalize and enrich audit logs by selecting the checkbox (default). If selected, Cortex XSIAM normalizes and enriches Azure Event Hub audit logs with other Cortex XSIAM authentication stories across all cloud providers using the same format. You can query this normalized data with XQL Search using the `cloud_audit_logs` dataset.  
   4. Click Test to validate access, and then click Enable.  
      When events start to come in, a green check mark appears underneath the Azure Event Hub configuration with the amount of data received.

### Ingest logs and data from Microsoft 365

Abstract

The Microsoft 365 email collector fetches emails through Microsoft Graph API, using an authorized app. A compliance mailbox is not required.

The Microsoft 365 email collector fetches email metadata through Microsoft Graph API, using an authorized app. A compliance mailbox is not required.

* A user account with the Microsoft Azure Account Administrator role is required to set up a new Microsoft 365 email collector.  
* The following Microsoft Graph API permissions are required:  
  * Mailbox access (read-write)  
    * Read and write mail in all mailboxes  
    * Read contacts in all mailboxes  
    * Read all user mailbox settings  
  * User information, groups, and directory data (read-only)  
    * Read directory data  
    * Read all groups  
    * Read all users' full profiles

You can narrow down the scope of ingested mailboxes by:

* Microsoft 365 Group  
* Distribution List  
* Mail-enabled Security Group  
* Mail-enabled Users

Datasets

The Microsoft 365 collector ingests data into the following datasets:

* `msft_o365_emails_raw`  
* `msft_o365_users_raw`  
* `msft_o365_groups_raw`  
* `msft_o365_devices_raw`  
* `msft_o365_mailboxes_raw`  
* `msft_o365_rules_raw`  
* `msft_o365_contacts_raw`

###### Configure ingestion into Cortex XSIAM

1. On the Data Sources page, click Add Data Source, search for and select Microsoft 365, and click Connect.  
2. In the wizard that opens, ensure that you have configured the items listed on the Permissions page, and then click Next.  
3. To confirm that you know that API authorization consent is required, click OK.  
4. Select the Microsoft account from which you want to collect email data.  
5. Click Next.  
6. Enter your password for the Microsoft account, and click Sign in.  
7. If you are asked to perform authentication using your organization's authentication tools, do so.  
8. For the list of of permissions that Cortex Email Security requires, click Accept.  
9. On the Scope page, select one of the following:  
   * Entire organization: Emails will be collected from all mailboxes in your organization.  
   * Specific groups: Enter the email addresses of group names, such as Microsoft 365 Groups, Mail-enabled Security Groups, Distribution Lists, or Mail-enabled Users.  
10. Click Next.  
11. On the Details page, enter a meaningful instance name, and click Next.  
12. On the Summary page, check your configurations, and then click Create.

After data starts to come in, a green check mark appears below the Microsoft 365 configuration, along with the amount of data received.

### Ingest Logs from Microsoft Office 365

Abstract

Ingest logs and data from Microsoft Office 365 Management Activity API and Microsoft Graph API for use in Cortex XSIAM.

* Ingesting Microsoft Entra ID (formerly known as Azure AD) authentication and audit events from Microsoft Graph API requires a Microsoft Azure Premium 1 or Premium 2 license. Alternatively, if the directory type is Azure AD B2C, the sign-in reports are accessible through the API without any additional license requirement.  
* To ingest **email** logs and data from Microsoft Office 365, use the dedicated data collector. For more information, see [Ingest logs and data from Microsoft 365](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-~eBfFPy8ou2131eb_fr8Ng).

Cortex XSIAM can ingest the following logs and data from Microsoft Office 365 Management Activity API and Microsoft Graph API using the Office 365 data collector. Alerts are collected with a delay of 5 minutes. If your organization requires collection that is closer to real-time collection, we recommend using the Microsoft Azure Event Hub integration instead.

* Microsoft Office 365 audit events from Management Activity API, which provides information about various user, administrator, system, and policy actions and events from Office 365, Microsoft Entra ID (formerly known as Azure AD) and MDO activity logs.  
  When auditing is turned off from the default setting, you need to first [turn on auditing](https://learn.microsoft.com/en-us/microsoft-365/compliance/turn-audit-log-search-on-or-off?view=o365-worldwide#verify-the-auditing-status-for-your-organization) for your organization to collect Microsoft Office 365 audit events from the Management Activity API. Log duplication of up to 5% in Microsoft products is considered normal. In some cases, such as login to a portal using MFA, two log entries are recorded by design.  
* Microsoft Entra ID (Azure AD) authentication and audit events from Microsoft Graph API.  
  When collecting Azure AD Authentication Logs, Cortex XSIAM also collects by default all sign-in event types from a beta version of Microsoft Graph API, which is still subject to change. In addition to classic interactive user sign-ins, selecting this option allows you to collect.  
  * Non-interactive user sign-ins.  
  * Service principal sign-ins.  
  * Managed Identities for Azure resource sign-ins.  
* To address [Azure reporting latency](https://docs.microsoft.com/en-us/azure/active-directory/reports-monitoring/reference-reports-latencies), there is a 10-minute latency period for Cortex XSIAM to receive Azure AD logs.  
* Microsoft 365 alerts from Microsoft Graph Security API are available for different products.  
  * Microsoft Graph Security API v1: Alerts from the following products are available via the Microsoft Graph Security API v1:  
    * Microsoft Defender for Cloud, Azure Active Directory Identity Protection, Microsoft Defender for Cloud Apps, Microsoft Defender for Endpoint, Microsoft Defender for Identity, Microsoft 365, Azure Information Protection, and Azure Sentinel.  
  * Microsoft Graph Security API v2: Alerts (alerts\_v2) from the following products are available via the Microsoft Graph Security API v2 beta version, which is still subject to change:  
    * Microsoft 365 Defender unified alerts API, which serves alerts from Microsoft 365 Defender, Microsoft Defender for Endpoint, Microsoft Defender for Office 365, Microsoft Defender for Identity, Microsoft Defender for Cloud Apps, and Microsoft Purview Data Loss Prevention (including any future new signals integrated into M365D).  
  * You can also implement the corresponding Cortex Data Model (XDM) mappings for these Microsoft Graph Security API v2 alerts using Cortex Marketplace via the Microsoft Graph Security content pack.  
* To view alerts from the various products via the Microsoft Graph Security API versions, you need to ensure that you've set up the applicable licenses in Office 365\. The table below lists the various licenses required for the different Microsoft Defender products. For more information on other Microsoft product licenses, see the Microsoft documentation.

| Product | Standalone license | E3 license | E3 \+ Security add-on license | E5 license | E5 Security license | E5 Compliance license |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Microsoft Defender for Endpoint Plan 1 | ✓ | ✓ | ✓ | — | — | — |
| Microsoft Defender for Endpoint Plan 2 | — | — | ✓ | ✓ | ✓ | — |
| Microsoft Defender for Identity | — | — | ✓ | ✓ | ✓ | — |
| Microsoft Defender for Office 365 Plan 1 | ✓ | — | — | — | — | — |
| Microsoft Defender for Office 365 Plan 2 | ✓ | — | ✓ | ✓ | ✓ | — |
| Microsoft Defender for Cloud Apps | — | — | ✓ | ✓ | ✓ | ✓ |

For more information, see the [Office 365 Management Activity API schema](https://docs.microsoft.com/en-us/office/office-365-management-api/office-365-management-activity-api-schema).

To receive logs from Microsoft Office 365, you must first configure the Data Sources settings in Cortex XSIAM. After you set up data collection, Cortex XSIAM begins receiving new logs and data from the source.

When Cortex XSIAM begins receiving logs, the app creates a new dataset for the different types of logs and data that you are collecting, which you can use to initiate XQL Search queries. For example queries, refer to the in-app XQL Library. For all Microsoft Office 365 logs, Cortex XSIAM can also raise Cortex XSIAM alerts (Analytics, IOC, BIOC, and Correlation Rules) when relevant from Office 365 logs. While Correlation Rules alerts are raised on non-normalized and normalized logs, Analytics, IOC, and BIOC alerts are only raised on normalized logs.

For the different types of data you can collect using the Office 365 data collector, the following table lists the different datasets, vendors, and products automatically configured, and whether the data is normalized.

| Data type | Dataset | Vendor | Product | Normalized data |
| ----- | ----- | ----- | ----- | ----- |
| Microsoft Office 365 audit events from Management Activity API |  |  |  |  |
| Microsoft Entra ID (Azure AD) | `msft_o365_azure_ad_raw` | `msft` | `O365 Azure AD` | — |
| Exchange Online | `msft_o365_exchange_online_raw` | `msft` | `O365 Exchange Online` | Cortex XSIAM supports normalizing Exchange Online audit logs into stories, which are collected in a dataset called `saas_audit_logs*`. |
| SharePoint Online | `msft_o365_sharepoint_online_raw` | `msft` | `O365 Sharepoint Online` | Cortex XSIAM supports normalizing SharePoint Online audit logs into stories, which are collected in a dataset called `saas_audit_logs*`. |
| DLP | `msft_o365_dlp_raw` | `msft` | `O365 DLP` | — |
| General | `msft_o365_general_raw` | `msft` | `O365 General` | Cortex XSIAM supports normalizing General audit logs into stories, which are collected in a dataset called `saas_audit_logs*`. |
| Microsoft Entra ID (Azure AD) authentication events from Microsoft Graph API | `msft_azure_ad_raw` | `msft` | `Azure AD` | When relevant, Cortex XSIAM normalizes Azure AD authentication logs and Azure AD Sign-in logs to authentication stories. |
| Microsoft Entra ID (Azure AD) audit events from Microsoft Graph API | `msft_azure_ad_audit_raw` | `msft` | `Azure AD Audit` | When relevant, Cortex XSIAM normalizes Azure AD audit logs to cloud audit logs stories. |
| Alerts from Microsoft Graph Security API v1 and v2 | `msft_graph_security_alerts_raw` | `msft` | `Security Alerts` | — |

\***Note**: For the `saas_audit_logs` dataset, the Vendor is saas and Product is Audit Logs.

In FedRAMP environments, Azure sign-in logs are not supported, due to vendor technical constraints.

To set up the Office 365 integration:

1. From the Microsoft Entra ID console (formerly Azure AD console), create an app for Cortex XSIAM with the applicable API permissions for the logs and data you want to collect as detailed in the following table.

| Log type and data | API/Permission name |
| :---- | :---- |
| Microsoft Office 365 audit events from Management Activity API |  |
| \-Azure AD | Office 365 Management APIs → ActivityFeed.Read |
| \-Exchange Online | Office 365 Management APIs → ActivityFeed.Read |
| \-Sharepoint Online | Office 365 Management APIs → ActivityFeed.Read |
| \-DLP | Office 365 Management APIs → ActivityFeed.ReadDlp |
| \-General | Office 365 Management APIs → ActivityFeed.Read |
| Microsoft Office 365 emails via Microsoft’s Graph API | Microsoft Graph → Mail.ReadWrite |
| Azure AD authentication and audit events from Microsoft Graph API | Microsoft Graph → AuditLog.Read.All Microsoft Graph → Directory.Read.All |
| Alerts from Microsoft Graph Security API v1 and v2 | Microsoft Graph → SecurityAlert.Read.All Microsoft Graph → SecurityEvents.Read.All |

2.   
   For more information on Microsoft Azure, see the following instructions in the Microsoft documentation portal.  
   1. [Register an app](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app).  
   2. [Add API permissions with type Application](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-configure-app-access-web-apis#add-permissions-to-access-web-apis).  
   3. [Create an application secret](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#create-a-new-application-secret).  
3. In Cortex XSIAM, select Settings → Data Sources.  
4. On the Data Sources page, click Add Data Source, search for and select Office 365, and click Connect.  
5. Integrate the applicable Microsoft Entra ID (Azure AD) service with Cortex XSIAM.  
   1. Specify the Tenant Domain of your Microsoft Entra ID tenant.  
   2. Obtain the Application Client ID and Secret for your Microsoft Entra ID (Azure AD) service from the Microsoft Entra ID console, and specify the values in Cortex XSIAM.  
      These values enable Cortex XSIAM to authenticate with your Microsoft Entra ID (Azure AD) service.  
   3. Select the types of logs that you want to receive from Office 365\.  
      The following options are available.  
      * Office 365 Management Activity API  
        * Cloud Environment: select the cloud environment used by your organization:  
          * Enterprise: Default option for non-US Government tenants  
          * GCC: US Government Compliant Cloud tenants  
          * GCC High: US Government Compliant Cloud High tenants  
          * DoD: US Department of Defense tenants  
        * Azure AD: Includes subset of Azure AD audit events and Azure AD authentication events. There can be significant overlap between these and the Azure AD Authentication Logs originating from Microsoft Graph API.  
          Use this option when you don’t want to grant permissions for Azure AD Authentication and Azure AD Audit.  
        * Exchange Online: Includes audit logs on [Azure Exchange mailboxes](https://docs.microsoft.com/en-us/office/office-365-management-api/office-365-management-activity-api-schema#exchange-mailbox-schema) and [Exchange admin activities](https://docs.microsoft.com/en-us/office/office-365-management-api/office-365-management-activity-api-schema#exchange-admin-schema) on the Office 365 Exchange.  
        * Sharepoint Online: Includes audit events on Sharepoint and OneDrive activities.  
        * DLP: Includes Microsoft 365 DLP events for Exchange, Sharepoint, and OneDrive.  
        * General: Includes audit logs for [various Microsoft 365 applications](https://docs.microsoft.com/en-us/office/office-365-management-api/office-365-management-activity-api-schema), such as Power BI and Microsoft Forms.  
      * Microsoft Graph API  
        * Cloud Environment: select the cloud environment used by your organization:  
          * Global Service: Default option for non-US Government tenants  
          * Government L4: US Government Layer 4 tenants  
          * Government L5 (DOD): US Government Layer 5 tenants  
        * Azure AD Authentication Logs and Collect all sign-in event types: [Azure AD Sign-in logs](https://docs.microsoft.com/en-us/azure/active-directory/reports-monitoring/concept-sign-ins) includes by default all sign-in event types from a beta version of Microsoft Graph API, which is still subject to change. In addition to classic interactive user sign-ins, selecting the Collect all sign-in event types allows you to collect.  
          \-Non-interactive user sign-ins.  
          \-Service principal sign-ins.  
          \-Managed Identities for Azure resource sign-ins.  
        * Azure AD Audit Logs: [Azure AD Audit logs](https://docs.microsoft.com/en-us/azure/active-directory/reports-monitoring/concept-audit-logs) includes different categories, such as User Management, Group Management and Application Management.  
        * Alerts: When this checkbox is selected, alerts from the following products are collected via the Microsoft Graph Security API v1:  
          * Microsoft Defender for Cloud, Azure Active Directory Identity Protection, Microsoft Defender for Cloud Apps, Microsoft Defender for Endpoint, Microsoft Defender for Identity, Microsoft 365, Azure Information Protection, and Azure Sentinel.  
          * Use Microsoft Graph API v2: When this checkbox is also selected, alerts (alerts\_v2) from the following products are only collected via the Microsoft Graph Security API v2 beta version, which is still subject to change:  
            * Microsoft 365 Defender unified alerts API, which serves alerts from Microsoft 365 Defender, Microsoft Defender for Endpoint, Microsoft Defender for Office 365, Microsoft Defender for Identity, Microsoft Defender for Cloud Apps, and Microsoft Purview Data Loss Prevention (including any future new signals integrated into M365D).  
        * Emails: Deprecated. Use the dedicated email collector instead. For more information, see [Ingest logs and data from Microsoft 365](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-~eBfFPy8ou2131eb_fr8Ng).  
   4. Click Test to test the connection settings.  
      To test the connection, you must select one or more log types. Cortex XSIAM then tests the connection settings for the selected log types.  
   5. If successful, click Enable to enable Office 365 log collection.

### Ingest Logs and Data from Okta

Abstract

Ingest authentication logs and data from Okta for use in Cortex XSIAM authentication stories.

To receive logs and data from Okta, you must configure the Data Sources settings in Cortex XSIAM. After you set up data collection, Cortex XSIAM immediately begins receiving new logs and data from the source. The information from Okta is then searchable in XQL Search using the `okta_sso_raw` dataset. In addition, depending on the event type, data is normalized to either `xdr_data` or `saas_audit_logs` datasets.

You can collect all types of events from Okta. When setting up the Okta data collector in Cortex XSIAM , a field called Okta Filter is available to configure collection for events of your choosing. All events are collected by default unless you define an Okta API Filter expression for collecting the data, such as `filter=eventType eq “user.session.start”.\n`. For Okta information to be weaved into authentication stories, `“user.authentication.sso”` events must be collected.

Since the Okta API enforces concurrent rate limits, the Okta data collector is built with a mechanism to reduce the amount of requests whenever an error is received from the Okta API indicating that too many requests have already been sent. In addition, to ensure you are properly notified about this, an alert is displayed in the Notification Area and a record is added to the Management Audit Logs.

Before you begin configuring data collection from Okta, ensure your Okta user has administrator privileges with a role that can create API tokens, such as the read-only administrator, Super administrator, and Organization administrator. For more information, see the [Okta Administrators Documentation](https://help.okta.com/en-us/Content/Topics/Security/Administrators.htm?cshid=ext_Security_Administrators).

To configure the Okta collection in Cortex XSIAM:

1. Identify the domain name of your Okta service.  
   From the Dashboard of your Okta console, note your Org URL.  
   For more information, see the [Okta Documentation](https://developer.okta.com/docs/guides/find-your-domain/findorg/).  
   okta-identify-domain.png  
2. Obtain your authentication token in Okta.  
   1. Select API → Tokens.  
   2. Create Token and record the token value.  
      This is your only opportunity to record the value.  
3. Select Settings → Data Sources.  
4. On the Data Sources page, click Add Data Source, search for and select Okta, and click Connect.  
5. Integrate the Okta authentication service with Cortex XSIAM.  
   1. Specify the OKTA DOMAIN (Org URL) that you identified on your Okta console.  
   2. Specify the TOKEN used to authenticate with Okta.  
   3. Specify the Okta Filter to configure collection for events of your choosing. All events are collected by default unless you define an Okta API Filter expression for collecting the data, such as `filter=eventType eq “user.session.start”.\n`. For Okta information to be weaved into authentication stories, `“user.authentication.sso”` events must be collected.  
   4. Test the connection settings.  
   5. If successful, Enable Okta log collection.  
      Once events start to come in, a green check mark appears underneath the Okta configuration with the amount of data received.  
6. After Cortex XSIAM begins receiving information from the service, you can Create an XQL Query to search for specific data. When including authentication events, you can also Create an Authentication Query to search for specific authentication data.

### Ingest Logs and Data from OneLogin

Abstract

Learn how to ingest different types of logs and data from OneLogin.

Cortex XSIAM can ingest different types of data from OneLogin accounts using the OneLogin data collector.

To receive logs and data from OneLogin via the OneLogin REST APIs, you must configure the Data Sources settings in Cortex XSIAM based on your OneLogin credentials. After you set up data collection, Cortex XSIAM begins receiving new logs and data from the source.

When Cortex XSIAM begins receiving logs, the app creates a new dataset for the different types of data collected and normalizes the ingested data into authentication stories, where specific relevant events are collected in the `authentication_story` preset for the **`xdr_data`** dataset. You can search these datasets using XQL Search queries. For all logs, Cortex XSIAM can raise Cortex XSIAM alerts (Analytics, Correlation Rules, IOC, and BIOC), when relevant from OneLogin logs. While Correlation Rules alerts are raised on non-normalized and normalized logs, Analytics, IOC, and BIOC alerts are only raised on normalized logs.

The following table provides a description of the different types of data you can collect, the collection method and fetch interval for the data collected, and the name of the dataset to use in Cortex Query Language (XQL) queries.

| Data type | Description | Collection method | Fetch interval | Dataset name |
| ----- | ----- | ----- | ----- | ----- |
| **Log collection** |  |  |  |  |
| Events | User logins, administrative operations, provisioning, and a list of all OneLogin event types | Appends data | 30 seconds | onelogin\_events\_raw |
| **Directory** |  |  |  |  |
| Users | Lists of users | Overwrites data | 10 minutes | onelogin\_users\_raw |
| Groups | Lists of groups | Overwrites data | 10 minutes | onelogin\_groups\_raw |
| Apps | Lists of apps | Overwrites data | 10 minutes | onelogin\_apps\_raw |

Before you configure Cortex XSIAM data collection from OneLogin, make sure you have the following.

* An Advanced OneLogin account.  
* Owner or administrator permissions in your OneLogin account which enable Cortex XSIAM to access the OneLogin account and generate the OAuth 2.0 access token.  
* A Cortex XSIAM user account with permissions to Read Log Collections, for example an Instance Administrator.

Configure Cortex XSIAM to receive logs and data from OneLogin.

1. Log in to OneLogin as an account owner or administrator.  
2. Under Administration → Developers → API Credentials, [Create a New Credential](https://developers.onelogin.com/api-docs/1/getting-started/working-with-api-credentials) with scope Read All.  
3. In the credential details page, copy the Client ID and the Client Secret, and save them somewhere safe. You will need to provide these keys when you configure the OneLogin data collector in Cortex XSIAM .  
4. Select Settings → Data Sources.  
5. On the Data Sources page, click Add Data Source, search for and select OneLogin, and click Connect.  
6. Configure the following parameters.  
   * Domain: Specify the domain of the OneLogin instance. The domain name must be in the format `https://<subdomain-name>.onelogin.com`.  
   * Name: Specify a descriptive and unique name for the configuration.  
   * Client ID: Specify the Client ID for the OneLogin API credential pair.  
   * Secret: Specify the Client Secret for the OneLogin API credential pair.  
   * Collect: Select the types of data to collect. By default, all the options are selected.  
     * Log Collection  
       * Events: Retrieves user logins, administrative operations, provisioning, and OneLogin event types. After normalization, the event types are enriched with the event name and description.  
     * Event data is collected every 30 seconds.  
     * Directory  
       * Users: Retrieves lists of users.  
       * Groups: Retrieves lists of groups.  
       * Apps: Retrieves lists of apps.  
     * Inventory data snapshots are collected every 10 minutes.  
7. Test the connection settings. If successful, Enable the OneLogin log collection.  
   When events start to come in, a green check mark appears underneath the OneLogin configuration.

### Ingest authentication logs from PingFederate

Abstract

Ingest authentication logs and data from PingFederate for use in Cortex XSIAM authentication stories.

To receive authentication logs from PingFederate, you must first write Audit and Provisioner Audit Logs to CEF in PingFederate and then set up a Syslog Collector in Cortex XSIAM to receive the logs. After you set up log collection, Cortex XSIAM immediately begins receiving new authentication logs from the source. Cortex XSIAM creates a dataset named `ping_identity_pingfederate_raw`. Logs from PingFederate are searchable in Cortex Query Language (XQL) queries using the dataset and surfaced, when relevant, in authentication stories.

1. Activate the Syslog Collector.  
2. Set up PingFederate to write logs in CEF.  
   To set up the integration, you must have an account for the PingFederate management dashboard and access to create a subscription for SSO logs.  
   In your PingFederate deployment, [write audit logs in CEF](https://docs.pingidentity.com/bundle/pingfederate-102/page/obk1564002980895.html). During this set up you will need the IP address and port you configured in the Syslog Collector.  
3. To search for specific authentication logs or data, you can Create an Authentication Query or use the XQL Search.

### Ingest Authentication Logs and Data from PingOne

Abstract

Ingest authentication logs and data from PingOne for Enterprise for use in Cortex XSIAM authentication stories.

To receive authentication logs and data from PingOne for Enterprise, you must first set up a Poll subscription in PingOne and then configure the Collection Integrations settings in Cortex XSIAM. After you set up collection integration, Cortex XSIAM immediately begins receiving new authentication logs and data from the source. These logs and data are then searchable in Cortex XSIAM.

1. Set up PingOne for Enterprise to send logs and data.  
   To set up the integration, you must have an account for the PingOne management dashboard and access to create a subscription for SSO logs.  
   From the PingOne Dashboard:  
   1. [Set up a Poll subscription](https://docs.pingidentity.com/bundle/pingone/page/stz1564020498800.html).  
      1. Select Reporting → Subscriptions → Add Subscription.  
      2. Enter a NAME for the subscription.  
      3. Select Poll as the subscription type.  
      4. Leave the remaining defaults and select Done.  
   2. Identify your account ID and subscription ID.  
      1. Select the subscription you just set up and note the part of the poll URL between /reports/ and /poll-subscriptions. This is your PingOne account ID.  
         For example:  
         `https://admin-api.pingone.com/v3/reports/1234567890asdfghjk-123456-zxcvbn/poll-subscriptions/***-0912348765-4567-98012***/events`  
         In this URL, the account ID is `1234567890asdfghjk-123456-zxcvbn`.  
      2. Next, note the part of the poll URL between /poll-subscriptions/ and /events. This is your subscription ID.  
         In the example above, the subscription ID is `***-0912348765-4567-98012***`.  
2. Select Settings → Data Sources.  
3. On the Data Sources page, click Add Data Source, search for and select PingOne, and click Connect.  
4. Connect Cortex XSIAM to your PingOne for Enterprise authentication service.  
   1. Enter your PingOne ACCOUNT ID.  
   2. Enter your PingOne SUBSCRIPTION ID.  
   3. Enter your PingOne USER NAME.  
   4. Enter your PingOne PASSWORD.  
   5. Test the connection settings.  
   6. If successful, Enable PingOne authentication log collection.  
5. After configuration is complete, Cortex XSIAM begins receiving information from the authentication service. From the Integrations page, you can view the log collection summary.  
6. To search for specific authentication logs or data, you can Create an Authentication Query or Create an XQL Query.

## Ingest operation and system logs from cloud providers

Abstract

Learn how to ingest operation and system logs from supported cloud providers into Cortex XSIAM.

You can ingest operation and system logs from supported cloud providers into Cortex XSIAM.

### Ingest generic logs from Amazon S3

Abstract

Take advantage of Cortex XSIAM investigation capabilities and set up generic log ingestion for your Amazon S3 logs.

You can forward generic logs for the relative service to Cortex XSIAM from Amazon S3.

To receive generic data from Amazon Simple Storage Service (Amazon S3), you must first configure data collection from Amazon S3. You can then configure the Data Sources settings in Cortex XSIAM for Amazon S3. After you set up collection integration, Cortex XSIAM begins receiving new logs and data from the source.

For more information on configuring data collection from Amazon S3, see the Amazon S3 Documentation.

As soon as Cortex XSIAM begins receiving logs, the app automatically creates an Amazon S3 Cortex Query Language (XQL) dataset (`<Vendor>_<Product>_raw`). This enables you to search the logs using XQL Search with the dataset. For example queries, refer to the in-app XQL Library. Cortex XSIAM can also raise Cortex XSIAM alerts (Correlation Rules only) when relevant from Amazon S3 logs.

You need to set up an Amazon S3 data collector to receive generic logs when collecting logs from BeyondTrust Privilege Management Cloud. For more information, see [Ingest logs from BeyondTrust Privilege Management Cloud](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-qd~7~n3M3Ro66DFaTUjm5g).

If you want to ingest raw EDR events from SentinelOne DeepVisibility, use the SentinelOne DeepVisibility log collector. For more information, see [Ingest raw EDR events from SentinelOne DeepVisibility](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-4SlRsiN0ttpJlujMGYKHRw).

Prerequisites

Perform the following tasks before you begin configuring data collection from Amazon S3:

* Create a dedicated Amazon S3 bucket, which collects the generic logs that you want capture. For more information, see [Creating a bucket using the Amazon S3 Console](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html).  
  It is the customer’s responsibility to define a retention policy for your Amazon S3 bucket by creating a Lifecycle rule in the Management tab. We recommend setting the retention policy to at least 7 days to ensure that the data is retrieved under all circumstances.  
* The logs collected by your dedicated Amazon S3 bucket must adhere to the following guidelines.  
  * Each log file must use the 1 log per line format as multi-line format is not supported.  
  * The log format must be compressed as gzip or uncompressed.  
  * For best performance, we recommend limiting each file size to up to 50 MB (compressed).  
* Ensure that you have at a minimum the following permissions in AWS for an Amazon S3 bucket and Amazon Simple Queue Service (SQS).  
  * **Amazon S3 bucket**: `GetObject`  
  * **SQS**: `ChangeMessageVisibility`, `ReceiveMessage`, and `DeleteMessage`.  
* Determine how you want to provide access to Cortex XSIAM to your logs and perform API operations. You have the following options:  
  * Designate an AWS IAM user, where you will need to know the Account ID for the user and have the relevant permissions to create an access key/id for the relevant IAM user.  
  * Create an assumed role in AWS to delegate permissions to a Cortex XSIAM AWS service. This role grants Cortex XSIAM access to your flow logs. For more information, see [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html). This is the Assumed Role option described in the configure the Amazon S3 collection in Cortex XSIAM. For more information on creating an assumed role for Cortex XSIAM, see [Create an assumed role](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-wPcVj~5r_xRuS_NmMalnOQ).  
* To collect Amazon S3 logs that use server-side encryption (SSE), the user role must have an IAM policy that states that Cortex XSIAM has kms:Decrypt permissions. With this permission, Amazon S3 automatically detects if a bucket is encrypted and decrypts it. If you want to collect encrypted logs from different accounts, you must have the decrypt permissions for the user role also in the key policy for the master account Key Management Service (KMS). For more information, see [Allowing users in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html).

Configure Cortex XSIAM to receive generic logs from Amazon S3:

1. Log in to the [AWS Management Console](https://console.aws.amazon.com/).  
2. From the menu bar, ensure that you have selected the correct region for your configuration.  
3. Configure an Amazon Simple Queue Service (SQS).  
   Ensure that you create your Amazon S3 bucket and Amazon SQS queue in the same region.  
   1. In the [Amazon SQS Console](https://console.aws.amazon.com/sqs/), click Create Queue.  
   2. Configure the following settings, where the default settings should be configured unless otherwise indicated.  
      * Type: Select Standard queue (default).  
      * Name: Specify a descriptive name for your SQS queue.  
      * Configuration section: Leave the default settings for the various fields.

Access policy → Choose method: Select Advanced and update the Access policy code in the editor window to enable your Amazon S3 bucket to publish event notification messages to your SQS queue. Use this sample code as a guide for defining the `“Statement”` with the following definitions.  
\-**`“Resource”`**: Leave the automatically generated ARN for the SQS queue that is set in the code, which uses the format `“arn:sns:Region:account-id:topic-name”`.  
You can retrieve your bucket’s ARN by opening the [Amazon S3 Console](https://console.aws.amazon.com/s3/) in a browser window. In the Buckets section, select the bucket that you created for collecting the Amazon S3 flow logs, click Copy ARN, and paste the ARN in the field.  
![bucket-copy-arn.png][image12]  
For more information on granting permissions to publish messages to an SQS queue, see [Granting permissions to publish event notification messages to a destination](https://docs.aws.amazon.com/AmazonS3/latest/userguide/grant-destinations-permissions-to-s3.html).  
{  
  "Version": "2012-10-17",  
  "Statement": \[  
    {  
      "Effect": "Allow",  
      "Principal": {  
        "Service": "s3.amazonaws.com"  
      },  
      "Action": "SQS:SendMessage",  
      "Resource": "\[Leave automatically generated ARN for the SQS queue defined by AWS\]",  
      "Condition": {  
        "ArnLike": {  
          "aws:SourceArn": "\[ARN of your Amazon S3 bucket\]"  
        }  
      }  
    }  
  \]

* }  
  * Dead-letter queue section: We recommend that you configure a queue for sending undeliverable messages by selecting Enabled, and then in the Choose queue field selecting the queue to send the messages. You may need to create a new queue for this, if you do not already have one set up. For more information, see [Amazon SQS dead-letter queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html).  
  3. Click Create queue.  
     Once the SQS is created, a message indicating that the queue was successfully configured is displayed at the top of the page.  
4. Configure an event notification to your Amazon SQS whenever a file is written to your Amazon S3 bucket.  
   1. Open the [Amazon S3 Console](https://console.aws.amazon.com/s3/) and in the Properties tab of your Amazon S3 bucket, scroll down to the Event notifications section, and click Create event notification.  
   2. Configure the following settings:  
      * Event name: Specify a descriptive name for your event notification containing up to 255 characters.  
      * Prefix: Do not set a prefix as the Amazon S3 bucket is meant to be a dedicated bucket for collecting only network flow logs.  
      * Event types: Select All object create events for the type of event notifications that you want to receive.  
      * Destination: Select SQS queue to send notifications to an SQS queue to be read by a server.  
      * Specify SQS queue: You can either select Choose from your SQS queues and then select the SQS queue, or select Enter SQS queue ARN and specify the ARN in the SQS queue field.  
        You can retrieve your SQS queue ARN by opening another instance of the AWS Management Console in a browser window, and opening the [Amazon SQS Console](https://console.aws.amazon.com/sqs/), and selecting the Amazon SQS that you created. In the Details section, under ARN, click the copy icon (![copy-icon.png][image13])), and paste the ARN in the field.  
        ![sqs-arn2.png][image14]  
   3. Click Save changes.  
      Once the event notification is created, a message indicating that the event notification was successfully created is displayed at the top of the page.  
      If your receive an error when trying to save your changes, you should ensure that the permissions are set up correctly.  
5. Configure access keys for the AWS IAM user.  
   1. It is the responsibility of your organization to ensure that the user who performs this task of creating the access key is assigned the relevant permissions. Otherwise, this can cause the process to fail with errors.  
   2. Skip this step if you are using an Assumed Role for Cortex XSIAM.  
   3. Open the [AWS IAM Console](https://console.aws.amazon.com/iam/), and in the navigation pane, select Access management → Users.  
   4. Select the User name of the AWS IAM user.  
   5. Select the Security credentials tab, and scroll down to the Access keys section, and click Create access key.  
   6. Click the copy icon () next to the Access key ID and Secret access key keys, where you must click Show secret access key to see the secret key, and record them somewhere safe before closing the window. You will need to provide these keys when you edit the Access policy of the SQS queue and when setting the AWS Client ID and AWS Client Secret in Cortex XSIAM. If you forget to record the keys and close the window, you will need to generate new keys and repeat this process.  
      For more information, see [Managing access keys for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).  
6. Update the Access policy of your Amazon SQS queue.  
   Skip this step if you are using an Assumed Role for Cortex XSIAM.  
   1. In the [Amazon SQS Console](https://console.aws.amazon.com/sqs/), select the SQS queue that you created when you configured an Amazon Simple Queue Service (SQS).  
   2. Select the Access policy tab, and Edit the Access policy code in the editor window to enable the IAM user to perform operations on the Amazon SQS with permissions to `SQS:ChangeMessageVisibility`, `SQS:DeleteMessage`, and `SQS:ReceiveMessage`. Use this sample code as a guide for defining the `“Sid”: “__receiver_statement”` with the following definitions.  
      * `“aws:SourceArn”`: Specify the ARN of the AWS IAM user. You can retrieve the User ARN from the Security credentials tab, which you accessed when you configured access keys for the AWS API user.

`“Resource”`: Leave the automatically generated ARN for the SQS queue that is set in the code, which uses the format `“arn:sns:Region:account-id:topic-name”`.  
For more information on granting permissions to publish messages to an SQS queue, see [Granting permissions to publish event notification messages to a destination](https://docs.aws.amazon.com/AmazonS3/latest/userguide/grant-destinations-permissions-to-s3.html).  
{  
  "Version": "2012-10-17",  
  "Statement": \[  
    {  
      "Effect": "Allow",  
      "Principal": {  
        "Service": "s3.amazonaws.com"  
      },  
      "Action": "SQS:SendMessage",  
      "Resource": "\[Leave automatically generated ARN for the SQS queue defined by AWS\]",  
      "Condition": {  
        "ArnLike": {  
          "aws:SourceArn": "\[ARN of your Amazon S3 bucket\]"  
        }  
      }  
    },  
   {  
      "Sid": "\_\_receiver\_statement",  
      "Effect": "Allow",  
      "Principal": {  
        "AWS": "\[Add the ARN for the AWS IAM user\]"  
      },  
      "Action": \[  
        "SQS:ChangeMessageVisibility",  
        "SQS:DeleteMessage",  
        "SQS:ReceiveMessage"  
      \],  
      "Resource": "\[Leave automatically generated ARN for the SQS queue defined by AWS\]"  
    }  
  \]

* }  
7. Configure the Amazon S3 collection in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select Amazon S3, and click Connect.  
   3. Set these parameters, where the parameters change depending on whether you configured an Access Key or Assumed Role.  
      * To provide access to Cortex XSIAM to your logs and perform API operations using a designated AWS IAM user, leave the Access Key option selected. Otherwise, select Assumed Role, and ensure that you create an Assumed Role for Cortex XSIAM before continuing with these instructions. In addition, when you create an Assumed Role for Cortex XSIAM, ensure that you edit the policy that defines the permissions for the role with the Amazon S3 Bucket ARN and SQS ARN.  
      * SQS URL: Specify the SQS URL, which is the ARN of the Amazon SQS that you configured in the AWS Management Console.  
      * Name: Specify a descriptive name for your log collection configuration.  
      * When setting an Access Key, set these parameters.  
        * AWS Client ID: Specify the Access key ID, which you received when you configured access keys for the AWS IAM user in AWS.  
        * AWS Client Secret: Specify the Secret access key you received when you configured access keys for the AWS IAM user in AWS.  
      * When setting an Assumed Role, set these parameters.  
        * Role ARN: Specify the Role ARN for the Assumed Role you created for Cortex XSIAM in AWS.  
        * External Id: Specify the External Id for the Assumed Role you created for Cortex XSIAM in AWS.  
      * Log Type: Select Generic to configure your log collection to receive generic logs from Amazon S3, which can include different types of data, such as file and metadata. When selecting this option, the following additional fields are displayed.  
        * Log Format: Select the log format type as Raw, JSON, CEF, LEEF, Cisco, Corelight, or Beyondtrust Cloud ECS.  
          \-The Vendor and Product defaults to Auto-Detect when the Log Format is set to CEF or LEEF.  
          \-For a Log Format set to CEF or LEEF, Cortex XSIAM reads events row by row to look for the Vendor and Product configured in the logs. When the values are populated in the event log row, Cortex XSIAM uses these values even if you specified a value in the Vendor and Product fields in the Amazon S3 data collector settings. Yet, when the values are blank in the event log row, Cortex XSIAM uses the Vendor and Product that you specified in these fields in the Amazon S3 data collector settings. If you did not specify a Vendor or Product in the Amazon S3 data collector settings, and the values are blank in the event log row, the values for both fields are set to unknown.  
          For a Log Format set to Beyondtrust Cloud ECS, the following fields are automatically set and are not configurable:  
          \-Vendor: Beyondtrust  
          \-Product: Privilege Management  
          \-Compression: Uncompressed  
          For more information, see [Ingest logs from BeyondTrust Privilege Management Cloud](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-qd~7~n3M3Ro66DFaTUjm5g).  
          For a Log Format set to Cisco, the following fields are automatically set and not configurable.  
          \-Vendor: Cisco  
          \-Product: ASA  
          For a Log Format set to Corelight, the following fields are automatically set and not configurable:  
          \-Vendor: Corelight  
          \-Product: Zeek  
          For a Log Format set to Raw or JSON, the following fields are automatically set and are configurable.  
          \-Vendor: AMAZON  
          \-Product: AWS  
          Cortex XSIAM supports logs in single line format or multiline format. For a JSON format, multiline logs are collected automatically when the Log Format is configured as JSON. When configuring a Raw format, you must also define the Multiline Parsing Regex as explained below.  
        * Vendor: (Optional) Specify a particular vendor name for the Amazon S3 generic data collection, which is used in the Amazon S3 XQL dataset `<Vendor>_<Product>_raw` that Cortex XSIAM creates as soon as it begins receiving logs.  
        * Product: (Optional) Specify a particular product name for the Amazon S3 generic data collection, which is used in the Amazon S3 XQL dataset name `<Vendor>_<Product>_raw` that Cortex XSIAM creates as soon as it begins receiving logs.  
        * Compression: Select whether the logs are compressed into a gzip file or are uncompressed.  
        * Multiline Parsing Regex: (Optional) This option is only displayed when the Log Format is set to Raw, where you can set the regular expression that identifies when the multiline event starts in logs with multilines. It is assumed that when a new event begins, the previous one has ended.  
   4. Click Test to validate access, and then click Enable.  
      Once events start to come in, a green check mark appears underneath the Amazon S3 configuration with the number of logs received.

### Ingest logs from Amazon CloudWatch

Abstract

Take advantage of Cortex XSIAM investigation capabilities and set up generic or EKS log ingestion for your Amazon CloudWatch logs.

You can forward generic and Elastic Kubernetes Service (EKS) logs to Cortex XSIAM from Amazon CloudWatch. When forwarding EKS logs, the following log types are included:

* API Server: Logs pertaining to API requests to the cluster.  
* Audit: Logs pertaining to cluster access via the Kubernetes API.  
* Authenticator: Logs pertaining to authentication requests into the cluster.  
* Scheduler: Logs pertaining to scheduling decisions.  
* Controller Manager: Logs pertaining to the state of cluster controllers.

You can ingest generic logs of the raw data or in a JSON format from Amazon Kinesis Firehose. EKS logs are automatically ingested in a JSON format from Amazon Kinesis Firehose. To enable log forwarding, you set up Amazon Kinesis Firehose and then add that to your Amazon CloudWatch configuration. After you complete the set up process, logs from the respective service are then searchable in Cortex XSIAM to provide additional information and context to your investigations.

As soon as Cortex XSIAM begins receiving logs, the application automatically creates one of the following Cortex Query Language (XQL) datasets depending on the type of logs you've configured:

* Generic: `<Vendor>_<Product>_raw`  
* EKS: `amazon_eks_raw`

These datasets enable you to search the logs in XQL Search. For example, queries refer to the in-app XQL Library. For enhanced cloud protection, you can also configure Cortex XSIAM to normalize EKS audit logs, which you can query with XQL Search using the `cloud_audit_logs` dataset. Cortex XSIAM can also raise Cortex XSIAM alerts (Analytics, IOC, BIOC, and Correlation Rules) when relevant from AWS logs. While Correlation Rules alerts are raised on non-normalized and normalized logs, Analytics, IOC, and BIOC alerts are only raised on normalized logs.

Enhanced cloud protection provides the following:

* Normalization of cloud logs  
* Cloud logs stitching  
* Enrichment with cloud data  
* Detection based on cloud analytics  
* Cloud-tailored investigations

To set up Amazon CloudWatch integration, you require certain permissions in AWS. You need a role that enables access to configuring Amazon Kinesis Firehose.

1. Set up the Amazon CloudWatch integration in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select Amazon CloudWatch, and click Connect.  
   3. Specify a descriptive Name for your log collection configuration.  
   4. Select the Log Type as one of the following, where your selection changes the options displayed:  
      * Generic: When selecting this log type, you can configure the following settings:  
        * Log Format: Choose the format of the data input source (CloudWatch) that you'll export to Cortex XSIAM , either JSON or Raw.  
        * Specify the Vendor and Product for the type of generic logs you are ingesting.  
          The vendor and product are used to define the name of your XQL dataset (`<Vendor>_<Product>_raw`). If you do not define a vendor or product, Cortex XSIAM uses the default values of Amazon and AWS with the resulting dataset name as `amazon_aws_raw`. To uniquely identify the log source, consider changing the values.  
      * EKS: When selecting this log type, the following options are displayed:  
        * The Vendor is automatically set to Amazon and Product to EKS , and is non-configurable. This means that all data for the EKS logs, whether it's normalized or not, can be queried in XQL Search using the `amazon_eks_raw` dataset.  
        * (Optional) You can decide whether to Normalize and enrich audit logs as part of the enhanced cloud protection by selecting the checkbox (default). If selected, Cortex XSIAM is configured to normalize EKS audit logs, which you can query with XQL Search using the `cloud_audit_logs` dataset.  
   5. Save & Generate Token.  
      Click the copy icon next to the key and record it somewhere safe. You will need to provide this key when you set up output settings in AWS Kinesis Firehose. If you forget to record the key and close the window you will need to generate a new key and repeat this process.  
   6. Select Done to close the window.  
2. Create a Kinesis Data Firehose delivery stream to your chosen destination.  
   1. Log in to the AWS Management Console, and open the [Kinesis console](https://console.aws.amazon.com/kinesis).  
   2. Select Data Firehose → Create delivery stream.  
      ![aws-kinesis-firehose-create-delivery-system.png][image15]  
   3. Define the name and source for your stream.  
      * Delivery stream name: Enter a descriptive name for your stream configuration.  
      * Source: Select Direct PUT or other sources.  
      * Server-side encryption for source records in the delivery stream: Ensure this option is disabled.  
   4. Click Next to proceed to the process record configuration.  
   5. Define the process records.  
      * Transform source records with AWS Lambda: Set the Data Transformation as Disabled.  
      * Convert record format: Set Record format conversion as Disabled.  
   6. Click Next to proceed to the destination configuration.  
   7. Choose a destination for the logs.  
      Choose HTTP Endpoint as the destination and configure the HTTP endpoint configuration settings:  
      * HTTP endpoint name: Specify the name you used to identify your AWS log collection configuration in Cortex XSIAM.  
      * HTTP endpoint URL: Copy the API URL associated with your log collection from the Cortex XSIAM management console. The URL will include your tenant name (`https://api-<tenant external URL>/logs/v1/aws)`.  
      * Access key: Paste in the token key you recorded earlier during the configuration of your Cortex XSIAM log collection settings.  
      * Content encoding: Select GZIP. Disabling content encoding may result in high egress costs.  
      * Retry duration: Enter 300 seconds.  
      * S3 bucket: Set the S3 backup mode as Failed data only. For the S3 bucket, we recommend that you create a dedicated bucket for Cortex XSIAM integration.  
   8. Click Next to proceed to the settings configuration.  
   9. Configure additional settings.  
      * HTTP endpoint buffer conditions: Set the Buffer size as 1 MiB and the Buffer interval as 60 seconds.  
      * S3 buffer conditions: Use the default settings for Buffer size as 5 MiB and Buffer interval as 300 seconds unless you have alternative sizing preferences.  
      * S3 compression and encryption: Choose your desired compression and encryption settings.  
      * Error logging: Select Enabled.  
      * Permissions: Create or update IAM role option.  
   10. Select Next.  
   11. Review your configuration and Create delivery stream.  
       When your delivery stream is ready, the status changes from Creating to Active.  
3. To begin forwarding logs, add the Kinesis Firehose instance to your Amazon CloudWatch configuration.  
   To do this, [add a subscription filter for Amazon Kinesis Firehose](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/SubscriptionFilters.html#FirehoseExample).  
4. Verify the status of the integration.  
   Return to the Integrations page and view the statistics for the log collection configuration.  
5. After Cortex XSIAM begins receiving logs from your Amazon services, you can use the XQL Search to search for logs in the new dataset.

### Ingest Logs and Data from a GCP Pub/Sub

Abstract

If you use the Pub/Sub messaging service from Global Cloud Platform (GCP), you can send logs and data from GCP to Cortex XSIAM.

If you use the Pub/Sub messaging service from Global Cloud Platform (GCP), you can send logs and data from your GCP instance to Cortex XSIAM. Data from GCP is then searchable in Cortex XSIAM to provide additional information and context to your investigations using the GCP Cortex Query Language (XQL) dataset, which is dependent on the type of GCP logs collected. For example queries, refer to the in-app XQL Library. You can configure a Google Cloud Platform collector to receive generic, flow, audit, or Google Cloud DNS logs. When configuring generic logs, you can receive logs in a Raw, JSON, CEF, LEEF, Cisco, or Corelight format.

You can also configure Cortex XSIAM to normalize different GCP logs as part of the enhanced cloud protection, which you can query with XQL Search using the applicable dataset. Cortex XSIAM can also raise Cortex XSIAM alerts (Analytics, IOC, BIOC, and Correlation Rules) when relevant from GCP logs. While Correlation Rules alerts are raised on non-normalized and normalized logs, Analytics, IOC, and BIOC alerts are only raised on normalized logs.

Enhanced cloud protection provides the following:

* Normalization of cloud logs  
* Cloud logs stitching  
* Enrichment with cloud data  
* Detection based on cloud analytics  
* Cloud-tailored investigations

The following table lists the various GCP log types the XQL datasets you can use to query in XQL Search:

| GCP log type | Dataset | Dataset with normalized data |
| ----- | ----- | ----- |
| Audit logs, including Google Kubernetes Engine (GKE) audit logs | `google_cloud_logging_raw` | `cloud_audit_logs` |
| Generic logs | Log Format types: **CEF** or **`LEEF`**: Automatically detected from either the logs or the user's input in the User Interface. **Cisco**: `cisco_asa_raw` **Corelight**: `corelight_zeek_raw` **JSON or Raw**: `google_cloud_logging_raw` | N/A |
| Google Cloud DNS logs | `google_dns_raw` | `xdr_data`: Once configured, Cortex XSIAM ingests Google Cloud DNS logs as XDR network connection stories, which you can query with XQL Search using the `xdr_data` dataset with the preset called `network_story`. |
| Network flow logs | `google_cloud_logging_raw` | `xdr_data`: Once configured, Cortex XSIAM ingests network flow logs as XDR network connection stories, which you can query with XQL Search using the `xdr_data` dataset with the preset called `network_story`. |

When collecting flow logs, we recommend that you include GKE annotations in your logs, which enable you to view the names of the containers that communicated with each other. GKE annotations are only included in logs if appended manually using the custom metadata configuration in GCP. For more information, see [VPC Flow Logs Overview](https://cloud.google.com/vpc/docs/flow-logs#customizing_metadata_fields). In addition, to customize metadata fields, you must use the gcloud command-line interface or the API. For more information, see [Using VPC Flow Logs](https://cloud.google.com/vpc/docs/using-flow-logs#enabling_vpc_flow_logging_for_an_existing_subnet).

To receive logs and data from GCP, you must first set up log forwarding using a Pub/Sub topic in GCP. You can configure GCP settings using either the GCP web interface or a GCP cloud shell terminal. After you set up your service account in GCP, you configure the Data Collection settings in Cortex XSIAM. The setup process requires the subscription name and authentication key from your GCP instance.

After you set up log collection, Cortex XSIAM immediately begins receiving new logs and data from GCP.

###### Set up log forwarding using the GCP web interface

* In Cortex XSIAM, set up Data Collection.  
  1. Select Settings → Data Sources.  
  2. On the Data Sources page, click Add Data Source, search for and select Google Cloud Platform, and click Connect.  
  3. Specify the Subscription Name that you previously noted or copied.  
  4. Browse to the JSON file containing your authentication key for the service account.  
  5. Select the Log Type as one of the following, where your selection changes the options displayed.  
     * Flow or Audit Logs: When selecting this log type, you can decide whether to normalize and enrich the logs as part of the enhanced cloud protection.  
       * (Optional) You can Normalize and enrich flow and audit logs by selecting the checkbox (default). If selected, Cortex XSIAM ingests the network flow logs as Cortex XSIAM network connection stories, which you can query using XQL Search from the `xdr_dataset` dataset with the preset called `network_story`. In addition, you can configure Cortex XSIAM to normalize GCP audit logs, which you can query with XQL Search using the `cloud_audit_logs` dataset.  
       * The Vendor is automatically set to Google and Product to Cloud Logging, which is not configurable. This means that all GCP data for the flow and audit logs, whether it's normalized or not, can be queried in XQL Search using the `google_cloud_logging_raw` dataset.  
     * Generic: When selecting this log type, you can configure the following settings.  
       * Log Format: Select the log format type as Raw, JSON, CEF, LEEF, Cisco, or Corelight.  
         * CEF or LEEF: The Vendor and Product defaults to Auto-Detect.  
           For a Log Format set to CEF or LEEF, Cortex XSIAM reads events row by row to look for the Vendor and Product configured in the logs. When the values are populated in the event log row, Cortex XSIAM uses these values even if you specified a value in the Vendor and Product fields in the GCP data collector settings. Yet, when the values are blank in the event log row, Cortex XSIAM uses the Vendor and Product that you specified in the GCP data collector settings. If you did not specify a Vendor or Product in the GCP data collector settings, and the values are blank in the event log row, the values for both fields are set to unknown.  
         * Cisco: The following fields are automatically set and not configurable.  
           * Vendor: Cisco  
           * Product: ASA  
         * Cisco data can be queried in XQL Search using the `cisco_asa_raw` dataset.  
         * Corelight: The following fields are automatically set and not configurable.  
           * Vendor: Corelight  
           * Product: Zeek  
         * Corelight data can be queried in XQL Search using the `corelight_zeek_raw` dataset.  
         * Raw or JSON: The following fields are automatically set and are configurable.  
           * Vendor: Google  
           * Product: Cloud Logging  
         * Raw or JSON data can be queried in XQL Search using the `google_cloud_logging_raw` dataset.  
           Cortex XSIAM supports logs in single line format or multiline format. For a JSON format, multiline logs are collected automatically when the Log Format is configured as JSON. When configuring a Raw format, you must also define the Multiline Parsing Regex as explained below.  
       * Vendor: (Optional) Specify a particular vendor name for the GCP generic data collection, which is used in the GCP XQL dataset `<Vendor>_<Product>_raw` that Cortex XSIAM creates as soon as it begins receiving logs.  
       * Product: (Optional) Specify a particular product name for the GCP generic data collection, which is used in the GCP XQL dataset name `<Vendor>_<Product>_raw` that Cortex XSIAM creates as soon as it begins receiving logs.  
       * Multiline Parsing Regex: (Optional) This option is only displayed when the Log Format is set to Raw, where you can set the regular expression that identifies when the multiline event starts in logs with multilines. It is assumed that when a new event begins, the previous one has ended.  
     * Google Cloud DNS: When selecting this log type, you can configure whether to normalize the logs as part of the enhanced cloud protection.  
       * Optional) You can Normalize DNS logs by selecting the checkbox (default). If selected, Cortex XSIAM ingests the Google Cloud DNS logs as Cortex XSIAM network connection stories, which you can query using XQL Search from the `xdr_dataset` dataset with the preset called `network_story`.  
       * The Vendor is automatically set to Google and Product to DNS , which is not configurable. This means that all Google Cloud DNS logs, whether it's normalized or not, can be queried in XQL Search using the `google_dns_raw` dataset.  
  6. Test the provided settings and, if successful, proceed to Enable log collection.  
1. Log in to your GCP account.  
2. Set up log forwarding from GCP to Cortex XSIAM.  
   1. Select Logging → Logs Router.  
   2. Select Create Sink → Cloud Pub/Sub topic, and then click Next.  
   3. To filter only specific types of data, select the filter or desired resource.  
   4. In the Edit Sink configuration, define a descriptive Sink Name.  
   5. Select Sink Destination → Create new Cloud Pub/Sub topic.  
   6. Enter a descriptive Name that identifies the sink purpose for Cortex XSIAM, and then Create.  
   7. Create Sink and then Close when finished.  
3. Create a subscription for your Pub/Sub topic.  
   1. Select the hamburger menu in G Cloud and then select Pub/Sub → Topics.  
   2. Select the name of the topic you created in the previous steps. Use the filters if necessary.  
   3. Create Subscription → Create subscription.  
   4. Enter a unique Subscription ID.  
   5. Choose Pull as the Delivery Type.  
   6. Create the subscription.  
      After the subscription is set up, G Cloud displays statistics and settings for the service.  
   7. In the subscription details, identify and note your Subscription Name.  
      Optionally, use the copy button to copy the name to the clipboard. You will need the name when you configure Collection in Cortex XSIAM.  
4. Create a service account and authentication key.  
   You will use the key to enable Cortex XSIAM to authenticate with the subscription service.  
   1. Select the menu icon, and then select IAM & Admin → Service Accounts.  
   2. Create Service Account.  
   3. Enter a Service account name and then Create.  
   4. Select a role for the account: Pub/Sub → Pub/Sub Subscriber.  
   5. Click Continue → Done.  
   6. Locate the service account by name, using the filters to refine the results, if needed.  
   7. Click the Actions menu identified by the three dots in the row for the service account and then Create Key.  
   8. Select JSON as the key type, and then Create.  
      After you create the service account key, G Cloud automatically downloads it.  
5. After Cortex XSIAM begins receiving information from the GCP Pub/Sub service, you can use the XQL Query language to search for specific data.

###### Set up log forwarding using the GCP cloud shell terminal

* In Cortex XSIAM, set up Data Collection.  
  1. Select Settings → Data Sources.  
  2. On the Data Sources page, click Add Data Source, search for and select Google Cloud Platform, and click Connect.  
  3. Specify the Subscription Name that you previously noted or copied.  
  4. Browse to the JSON file containing your authentication key for the service account.  
  5. Select the Log Type as one of the following, where your selection changes the options displayed.  
     * Flow or Audit Logs: When selecting this log type, you can decide whether to normalize and enrich the logs as part of the enhanced cloud protection.  
       * (Optional) You can Normalize and enrich flow and audit logs by selecting the checkbox (default). If selected, Cortex XSIAM ingests the network flow logs as Cortex XSIAM network connection stories, which you can query using XQL Search from the `xdr_dataset` dataset with the preset called `network_story`. In addition, you can configure Cortex XSIAM to normalize GCP audit logs, which you can query with XQL Search using the `cloud_audit_logs` dataset.  
       * The Vendor is automatically set to Google and Product to Cloud Logging, which is not configurable. This means that all GCP data for the flow and audit logs, whether it's normalized or not, can be queried in XQL Search using the `google_cloud_logging_raw` dataset.  
     * Generic: When selecting this log type, you can configure the following settings.  
       * Log Format: Select the log format type as Raw, JSON, CEF, LEEF, Cisco, or Corelight.  
         * CEF or LEEF: The Vendor and Product defaults to Auto-Detect.  
           For a Log Format set to CEF or LEEF, Cortex XSIAM reads events row by row to look for the Vendor and Product configured in the logs. When the values are populated in the event log row, Cortex XSIAM uses these values even if you specified a value in the Vendor and Product fields in the GCP data collector settings. Yet, when the values are blank in the event log row, Cortex XSIAM uses the Vendor and Product that you specified in the GCP data collector settings. If you did not specify a Vendor or Product in the GCP data collector settings, and the values are blank in the event log row, the values for both fields are set to unknown.  
         * Cisco: The following fields are automatically set and not configurable.  
           * Vendor: Cisco  
           * Product: ASA  
         * Cisco data can be queried in XQL Search using the `cisco_asa_raw` dataset.  
         * Corelight: The following fields are automatically set and not configurable.  
           * Vendor: Corelight  
           * Product: Zeek  
         * Corelight data can be queried in XQL Search using the `corelight_zeek_raw` dataset.  
         * Raw or JSON: The following fields are automatically set and are configurable.  
           * Vendor: Google  
           * Product: Cloud Logging  
         * Raw or JSON data can be queried in XQL Search using the `google_cloud_logging_raw` dataset.  
           Cortex XSIAM supports logs in single line format or multiline format. For a JSON format, multiline logs are collected automatically when the Log Format is configured as JSON. When configuring a Raw format, you must also define the Multiline Parsing Regex as explained below.  
       * Vendor: (Optional) Specify a particular vendor name for the GCP generic data collection, which is used in the GCP XQL dataset `<Vendor>_<Product>_raw` that Cortex XSIAM creates as soon as it begins receiving logs.  
       * Product: (Optional) Specify a particular product name for the GCP generic data collection, which is used in the GCP XQL dataset name `<Vendor>_<Product>_raw` that Cortex XSIAM creates as soon as it begins receiving logs.  
       * Multiline Parsing Regex: (Optional) This option is only displayed when the Log Format is set to Raw, where you can set the regular expression that identifies when the multiline event starts in logs with multilines. It is assumed that when a new event begins, the previous one has ended.  
     * Google Cloud DNS: When selecting this log type, you can configure whether to normalize the logs as part of the enhanced cloud protection.  
       * Optional) You can Normalize DNS logs by selecting the checkbox (default). If selected, Cortex XSIAM ingests the Google Cloud DNS logs as Cortex XSIAM network connection stories, which you can query using XQL Search from the `xdr_dataset` dataset with the preset called `network_story`.  
       * The Vendor is automatically set to Google and Product to DNS , which is not configurable. This means that all Google Cloud DNS logs, whether it's normalized or not, can be queried in XQL Search using the `google_dns_raw` dataset.  
  6. Test the provided settings and, if successful, proceed to Enable log collection.  
1. Launch the GCP cloud shell terminal or use your preferred shell with gcloud installed.  
   gcp-cli.png

Define your project ID.  
gcloud config set project \<PROJECT\_ID\>

2.                     

Create a Pub/Sub topic.  
gcloud pubsub topics create \<TOPIC\_NAME\>

3.                     

Create a subscription for this topic.  
gcloud pubsub subscriptions create \<SUBSCRIPTION\_NAME\> \--topic=\<TOPIC\_NAME\>

4.                       
    Note the subscription name you define in this step as you will need it to set up log ingestion from Cortex XSIAM.

Create a logging sink.  
During the logging sink creation, you can also define additional log filters to exclude specific logs. To filter logs, supply the optional parameter `--log-filter=<LOG_FILTER>`  
gcloud logging sinks create \<SINK\_NAME\> pubsub.googleapis.com/projects/\<PROJECT\_ID\>/topics/\<TOPIC\_NAME\> \--log-filter=\<LOG\_FILTER\>

5.                       
    If setup is successful, the console displays a summary of your log sink settings:  
   Created \[https://logging.googleapis.com/v2/projects/PROJECT\_ID/sinks/SINK\_NAME\]. Please remember to grant \`serviceAccount:LOGS\_SINK\_SERVICE\_ACCOUNT\` \\ the Pub/Sub Publisher role on the topic. More information about sinks can be found at /logging/docs/export/configure\_export  
6. Grant log sink service account to publish to the new topic.  
   Note the `serviceAccount` name from the previous step and use it to define the service for which you want to grant publish access.  
   gcloud pubsub topics add-iam-policy-binding \<TOPIC\_NAME\> \--member serviceAccount:\<LOGS\_SINK\_SERVICE\_ACCOUNT\> \--role=roles/pubsub.publisher  
7. Create a service account.  
   For example, use cortex-xdr-sa as the service account name and Cortex XSIAM Service Account as the display name.  
   gcloud iam service-accounts create \<SERVICE\_ACCOUNT\> \--description="\<DESCRIPTION\>" \--display-name="\<DISPLAY\_NAME\>"  
8. Grant the IAM role to the service account.  
   gcloud pubsub subscriptions add-iam-policy-binding \<SUBSCRIPTION\_NAME\> \--member serviceAccount:\<SERVICE\_ACCOUNT\>@\<PROJECT\_ID\>.iam.gserviceaccount.com \--role=roles/pubsub.subscriber  
9. Create a JSON key for the service account.  
   You will need the JSON file to enable Cortex XSIAM to authenticate with the GCP service. Specify the file destination and filename using a .json extension.  
   gcloud iam service-accounts keys create \<OUTPUT\_FILE\> \--iam-account \<SERVICE\_ACCOUNT\>@\<PROJECT\_ID\>.iam.gserviceaccount.com  
10. After Cortex XSIAM begins receiving information from the GCP Pub/Sub service, you can use the XQL Query language to search for specific data.

### Ingest logs from Google Kubernetes Engine

Abstract

Forward your Google Kubernetes Engine (GKE) logs directly to Cortex XSIAM using Elasticsearch Filebeat.

Instead of forwarding Google Kubernetes Engine (GKE) logs directly to Google StackDrive, Cortex XSIAM can ingest container logs from GKE using Elasticsearch Filebeat. To receive logs, you must install Filebeat on your containers and enable Data Collection settings for Filebeat.

After Cortex XSIAM begins receiving logs, the app automatically creates an Cortex Query Language (XQL) dataset using the vendor and product name that you specify during Filebeat setup. It is recommended to specify a descriptive name. For example, if you specify `google` as the vendor and `kubernetes` as the product, the dataset name will be `google_kubernetes_raw`. If you leave the product and vendor blank, Cortex XSIAM assigns the dataset a name of `container_container_raw`.

After Cortex XSIAM creates the dataset, you can search your GKE logs using XQL Search.

1. Install Filebeat on your containers.  
   For more information, see [https://www.elastic.co/guide/en/beats/filebeat/current/running-on-kubernetes.html](https://www.elastic.co/guide/en/beats/filebeat/current/running-on-kubernetes.html).  
2. Ingest Logs from Elasticsearch Filebeat.  
   Record your token key and API URL for the Filebeat Collector instance as you will need these later in this workflow.  
3. Deploy a Filebeat as a DaemonSet on Kubernetes.  
   This ensures there is a running instance of Filebeat on each node of the cluster.  
   1. Download the manifest file to a location where you can edit it.  
      `curl -L -O https://raw.githubusercontent.com/elastic/beats/7.10/deploy/kubernetes/filebeat-kubernetes.yaml`  
   2. Open the YAML file in your preferred text editor.  
   3. Remove the `cloud.id` and `cloud.auth` lines.  
      ![gke-filebeat-cloud.id-remove.png][image16]  
   4. For the `output.elasticsearch` configuration, replace the `hosts`, `username`, and `password` with environment variable references for `hosts` and `api_key`, and add a field and value for `compression_level` and `bulk_max_size`.  
      ![filebeat-elasticsearch-env-vars.png][image17]  
   5. In the `DaemonSet` configuration, locate the `env` configuration and replace `ELASTIC_CLOUD_AUTH`, `ELASTIC_CLOUD_ID`, `ELASTICSEARCH_USERNAME`, `ELASTICSEARCH_PASSWORD`, `ELASTICSEARCH_HOST`, `ELASTICSEARCH_PORT` and their relative values with the following.  
      * `ELASTICSEARCH_ENDPOINT`: Specify the API URL for your Cortex XSIAM tenant. You can copy the URL from the Filebeat Collector instance you set up for GKE in the Cortex XSIAM management console (Settings → (![gear.png][image18]) → Configurations → Data Collection → Custom Collectors → Copy API URL. The URL will include your tenant name (`https://api-tenant external URL:443/logs/v1/filebeat)`  
      * `ELASTICSEARCH_API_KEY`: Specify the token key you recorded earlier during the configuration of your Filebeat Collector instance.  
   6. After you configure these settings your configuration should look like the following image.  
      ![gke-filebeat-env-config.png][image19]  
   7. Save your changes.  
4. If you use RedHat OpenShift, you must also specify additional settings.  
   See [https://www.elastic.co/guide/en/beats/filebeat/7.10/running-on-kubernetes.html](https://www.elastic.co/guide/en/beats/filebeat/7.10/running-on-kubernetes.html#_red_hat_openshift_configuration).  
5. Deploy Filebeat on your Kubernetes.  
   `kubectl create -f filebeat-kubernetes.yaml`  
   This deploys Filebeat in the kube-system namespace. If you want to deploy the Filebeat configuration in other namespaces, change the namespace values in the YAML file (in any YAML inside this file) and add `-n <your_namespace>`.  
   After you deploy your configuration, the Filebeat DameonSet runs throughout your containers to forward logs to Cortex XSIAM. You can review the configuration from the Kubernetes Engine console: Workloads → Filebeat → YAML.  
   Cortex XSIAM supports logs in single line format or multiline format. For more information on handling messages that span multiple lines of text in Elasticsearch Filebeat, see [Manage Multiline Messages](https://www.elastic.co/guide/en/beats/filebeat/current/multiline-examples.html).  
6. After Cortex XSIAM begins receiving logs from GKE, you can use the XQL Search to search for logs in the new dataset.

### Ingest Logs from Microsoft Azure Event Hub

Abstract

Ingest logs from Microsoft Azure Event Hub with an option to ingest audit logs to use in Cortex XSIAM authentication stories.

Cortex XSIAM can ingest different types of data from Microsoft Azure Event Hub using the Microsoft Azure Event Hub data collector. To receive logs from Azure Event Hub, you must configure the Data Sources settings in Cortex XSIAM based on your Microsoft Azure Event Hub configuration. After you set up data collection, Cortex XSIAM begins receiving new logs and data from the source.

When Cortex XSIAM begins receiving logs, the app creates a new dataset (`MSFT_Azure_raw`) that you can use to initiate XQL Search queries. For example, queries refer to the in-app XQL Library. For enhanced cloud protection, you can also configure Cortex XSIAM to normalize Azure Event Hub audit logs, including Azure Kubernetes Service (AKS) audit logs, with other Cortex XSIAM authentication stories across all cloud providers using the same format, which you can query with XQL Search using the `cloud_audit_logs` dataset. For logs that you do not configure Cortex XSIAM to normalize, you can change the default dataset. Cortex XSIAM can also raise Cortex XSIAM alerts (Analytics, IOC, BIOC, and Correlation Rules) when relevant from Azure Event Hub logs. While Correlation Rules alerts are raised on non-normalized and normalized logs, Analytics, IOC, and BIOC alerts are only raised on normalized logs.

Enhanced cloud protection provides:

* Normalization of cloud logs  
* Cloud logs stitching  
* Enrichment with cloud data  
* Detection based on cloud analytics  
* Cloud-tailored investigations  
* Misconfiguration of Event Hub resources could cause ingestion delays.  
* In an existing Event Hub integration, do not change the mapping to a different Event Hub.  
* Do not use the same Event Hub for more than two purposes.

The following table provides a brief description of the different types of Azure audit logs you can collect.

For more information on Azure Event Hub audit logs, see [Overview of Azure platform logs](https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/platform-logs-overview).

| Type of data | Description |
| ----- | ----- |
| Activity logs | Retrieves events related to the operations on each Azure resource in the subscription from the outside in addition to updates on Service Health events. These logs are from the management plane. |
| Azure Active Directory (AD) Activity logs and Azure Sign-in logs | Contain the history of sign-in activity and audit trail of changes made in Azure AD for a particular tenant. Even though you can collect Azure AD Activity logs and Azure Sign-in logs using the Azure Event Hub data collector, we recommend using the Microsoft 365 data collector, because it is easier to configure. In addition, ensure that you don't configure both collectors to collect the same types of logs, because if you do so, you will be creating duplicate data in Cortex XSIAM. |
| Resource logs, including AKS audit logs | Retrieves events related to operations that were performed within an Azure resource. These logs are from the data plane. |

If you want to ingest raw Microsoft Defender for Endpoint events, use the Microsoft Defender log collector. For more information, see [Ingest raw EDR events from Microsoft Defender for Endpoint](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-E30SPrsh~A1Jt8Nm79uiwg).

Ensure that you do the following tasks before you begin configuring data collection from Azure Event Hub.

* Before you set up an Azure Event Hub, calculate the quantity of data that you expect to send to Cortex XSIAM, taking into account potential data spikes and potential increases in data ingestion, because partitions cannot be modified after creation. Use this information to ascertain the optimal number of partitions and Throughput Units (for Azure Basic or Standard) or Processing Units (for Azure Premium). Configure your Event Hub accordingly.  
* Create an Azure Event Hub. We recommend using a dedicated Azure Event Hub for this Cortex XSIAM integration. For more information, see [Quickstart: Create an event hub using Azure portal](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-create).  
* Each partition can support a throughput of up to 1 MB/s.  
* Ensure the format for the logs you want collected from the Azure Event Hub is either JSON or raw.

Configure the Azure Event Hub collection in Cortex XSIAM:

1. In the Microsoft Azure console, open the Event Hubs page, and select the Azure Event Hub that you created for collection in Cortex XSIAM.  
2. Record the following parameters from your configured event hub, which you will need when configuring data collection in Cortex XSIAM.  
   1. Your event hub’s consumer group.  
      * Select Entities → Event Hubs, and select your event hub.  
      * Select Entities → Consumer groups, and select your event hub.  
      * In the Consumer group table, copy the applicable value listed in the Name column for your Cortex XSIAM data collection configuration.  
   2. Your event hub’s connection string for the designated policy.  
      * Select Settings → Shared access policies.  
      * In the Shared access policies table, select the applicable policy.  
      * Copy the Connection string-primary key.  
   3. Your storage account connection string required for partitions lease management and checkpointing in Cortex XSIAM.  
      * Open the Storage accounts page, and either create a new storage account or select an existing one, which will contain the storage account connection string.  
      * Select Security \+ networking → Access keys, and click Show keys.  
      * Copy the applicable Connection string.  
3. Configure diagnostic settings for the relevant log types you want to collect and then direct these diagnostic settings to the designated Azure Event Hub.  
   1. Open the Microsoft Azure console.  
   2. Your navigation is dependent on the type of logs you want to configure.

| Log type | Navigation path |
| :---- | :---- |
| Activity logs | Select Azure services → Activity log → Export Activity Logs, and \+Add diagnostic setting. |
| Azure AD Activity logs and Azure Sign-in logs | Select Azure services → Azure Active Directory. Select Monitoring → Diagnostic settings, and \+Add diagnostic setting. |
| Resource logs, including AKS audit logs | Search for Monitor, and select Settings → Diagnostic settings. From your list of available resources, select the resource that you want to configure for log collection, and then select \+Add diagnostic setting.For every resource that you want to confiure, you'll have to repeat this step, or use [Azure policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview) for a general configuration. |

   3.   
      Set the following parameters:  
      * Diagnostic setting name: Specify a name for your Diagnostic setting.  
      * Logs Categories/Metrics: The options listed are dependent on the type of logs you want to configure. For Activity logs and Azure AD logs and Azure Sign-in logs, the option is called Logs Categories, and for Resource logs it's called Metrics.

| Log type | Log categories/metrics |
| :---- | :---- |
| Activity logs | Select from the list of applicable Activity log categories, the ones that you want to configure your designated resource to collect. We recommend selecting all of the options. Administrative Security ServiceHealth Alert Recommendation Policy Autoscale ResourceHealth |
| Azure AD Activity logs and Azure Sign-in logs | Select from the list of applicable Azure AD Activity and Azure Sign-in Logs Categories, the ones that you want to configure your designated resource to collect. You can select any of the following categories to collect these types of Azure logs. Azure AD Activity logs: AuditLogs Azure Sign-in logs: SignInLogs NonInteractiveUserSignInLogs ServicePrincipalSignInLogs ManagedIdentitySignInLogs ADFSSignInLogs There are additional log categories displayed. We recommend selecting all the available options. |
| Resource logs, including AKS audit logs | The list displayed is dependent on the resource that you selected. We recommend selecting all the options available for the resource. |

      *   
        Destination details: Select Stream to event hub, where additional parameters are displayed that you need to configure. Ensure that you set the following parameters using the same settings for the Azure Event Hub that you created for the collection.  
        * Subscription: Select the applicable Subscription for the Azure Event Hub.  
        * Event hub namespace: Select the applicable Subscription for the Azure Event Hub.  
        * (Optional) Event hub name: Specify the name of your Azure Event Hub.  
        * Event hub policy: Select the applicable Event hub policy for your Azure Event Hub.  
   4. Save your settings.  
4. Configure the Azure Event Hub collection in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select Azure Event Hub, and click Connect.  
   3. Set these parameters.  
      * Name: Specify a descriptive name for your log collection configuration.  
      * Event Hub Connection String: Specify your event hub’s connection string for the designated policy.  
      * Storage Account Connection String: Specify your storage account’s connection string for the designated policy.  
      * Consumer Group: Specify your event hub’s consumer group.  
      * Log Format: Select the log format for the logs collected from the Azure Event Hub as Raw, JSON, CEF, LEEF, Cisco-asa, or Corelight.  
        When you Normalize and enrich audit logs, the log format is automatically configured. As a result, the Log Format option is removed and is no longer available to configure (default).  
        * CEF or LEEF: The Vendor and Product defaults to Auto-Detect.  
          For a Log Format set to CEF or LEEF, Cortex XSIAM reads events row by row to look for the Vendor and Product configured in the logs. When the values are populated in the event log row, Cortex XSIAM uses these values even if you specified a value in the Vendor and Product fields in the Azure Event Hub data collector settings. Yet, when the values are blank in the event log row, Cortex XSIAM uses the Vendor and Product that you specified in the Azure Event Hub data collector settings. If you did not specify a Vendor or Product in the Azure Event Hub data collector settings, and the values are blank in the event log row, the values for both fields are set to unknown.  
        * Cisco-asa: The following fields are automatically set and not configurable.  
          * Vendor: Cisco  
          * Product: ASA  
        * Cisco data can be queried in XQL Search using the `cisco_asa_raw` dataset.  
        * Corelight: The following fields are automatically set and not configurable.  
          * Vendor: Corelight  
          * Product: Zeek  
        * Corelight data can be queried in XQL Search using the `corelight_zeek_raw` dataset.  
        * Raw or JSON: The following fields are automatically set and are configurable.  
          * Vendor: Msft  
          * Product: Azure  
        * Raw or JSON data can be queried in XQL Search using the `msft_azure_raw` dataset.  
      * Vendor and Product: Specify the Vendor and Product for the type of logs you are ingesting.  
        The Vendor and Product are used to define the name of your Cortex Query Language (XQL) dataset (`<vendor>_<product>_raw`). The Vendor and Product values vary depending on the Log Format selected. To uniquely identify the log source, consider changing the values if the values are configurable.  
        When you Normalize and enrich audit logs, the Vendor and Product fields are automatically configured, so these fields are removed as available options (default).  
      * Normalize and enrich audit logs: (Optional) For enhanced cloud protection, you can Normalize and enrich audit logs by selecting the checkbox (default). If selected, Cortex XSIAM normalizes and enriches Azure Event Hub audit logs with other Cortex XSIAM authentication stories across all cloud providers using the same format. You can query this normalized data with XQL Search using the `cloud_audit_logs` dataset.  
   4. Click Test to validate access, and then click Enable.  
      When events start to come in, a green check mark appears underneath the Azure Event Hub configuration with the amount of data received.

### Ingest Logs and Data from Okta

Abstract

Ingest authentication logs and data from Okta for use in Cortex XSIAM authentication stories.

To receive logs and data from Okta, you must configure the Data Sources settings in Cortex XSIAM. After you set up data collection, Cortex XSIAM immediately begins receiving new logs and data from the source. The information from Okta is then searchable in XQL Search using the `okta_sso_raw` dataset. In addition, depending on the event type, data is normalized to either `xdr_data` or `saas_audit_logs` datasets.

You can collect all types of events from Okta. When setting up the Okta data collector in Cortex XSIAM , a field called Okta Filter is available to configure collection for events of your choosing. All events are collected by default unless you define an Okta API Filter expression for collecting the data, such as `filter=eventType eq “user.session.start”.\n`. For Okta information to be weaved into authentication stories, `“user.authentication.sso”` events must be collected.

Since the Okta API enforces concurrent rate limits, the Okta data collector is built with a mechanism to reduce the amount of requests whenever an error is received from the Okta API indicating that too many requests have already been sent. In addition, to ensure you are properly notified about this, an alert is displayed in the Notification Area and a record is added to the Management Audit Logs.

Before you begin configuring data collection from Okta, ensure your Okta user has administrator privileges with a role that can create API tokens, such as the read-only administrator, Super administrator, and Organization administrator. For more information, see the [Okta Administrators Documentation](https://help.okta.com/en-us/Content/Topics/Security/Administrators.htm?cshid=ext_Security_Administrators).

To configure the Okta collection in Cortex XSIAM:

1. Identify the domain name of your Okta service.  
   From the Dashboard of your Okta console, note your Org URL.  
   For more information, see the [Okta Documentation](https://developer.okta.com/docs/guides/find-your-domain/findorg/).  
   okta-identify-domain.png  
2. Obtain your authentication token in Okta.  
   1. Select API → Tokens.  
   2. Create Token and record the token value.  
      This is your only opportunity to record the value.  
3. Select Settings → Data Sources.  
4. On the Data Sources page, click Add Data Source, search for and select Okta, and click Connect.  
5. Integrate the Okta authentication service with Cortex XSIAM.  
   1. Specify the OKTA DOMAIN (Org URL) that you identified on your Okta console.  
   2. Specify the TOKEN used to authenticate with Okta.  
   3. Specify the Okta Filter to configure collection for events of your choosing. All events are collected by default unless you define an Okta API Filter expression for collecting the data, such as `filter=eventType eq “user.session.start”.\n`. For Okta information to be weaved into authentication stories, `“user.authentication.sso”` events must be collected.  
   4. Test the connection settings.  
   5. If successful, Enable Okta log collection.  
      Once events start to come in, a green check mark appears underneath the Okta configuration with the amount of data received.  
6. After Cortex XSIAM begins receiving information from the service, you can Create an XQL Query to search for specific data. When including authentication events, you can also Create an Authentication Query to search for specific authentication data.

## Ingest endpoint data

Abstract

Cortex XSIAM enables you to ingest endpoint data.

Cortex XSIAM enables you to ingest endpoint data.

The following endpoint data can be ingested by Cortex XSIAM:

* [SentinelOne DeepVisibility raw EDR events](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-4SlRsiN0ttpJlujMGYKHRw)  
* [Microsoft Defender for Endpoint raw EDR events](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-E30SPrsh~A1Jt8Nm79uiwg)  
* [CrowdStrike Falcon Data Replicator raw EDR events](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-Q6IT1fKciJRWqsfMnIRUVw)  
* [CrowdStrike alerts and metadata, using CrowdStrike APIs](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-TJUSvJpht9u7Y7UNiioxAQ)  
* Windows Events and other data using other Broker VM data collector applets

### Ingest alerts and metadata from CrowdStrike APIs

Abstract

Ingest CrowdStrike API real-time alerts and metadata for use in Cortex XSIAM stories.

To enable some of the APIs, you may need to reach out to CrowdStrike support.

To receive CrowdStrike API real-time alerts and logs, you must first configure data collection from CrowdStrike APIs. You can then configure the Data Sources settings in Cortex XSIAM for the CrowdStrike APIs.

For more information on configuring data collection from CrowdStrike APIs, see the CrowdStrike Documentation.

When Cortex XSIAM begins receiving alerts and logs, it automatically creates a CrowdStrike API XQL dataset (`crowdstrike_falcon_incident_raw`). You can use the alerts in rules, and search the logs using XQL Search. For example queries, refer to the in-app XQL Library.

1. Configure data collection from CrowdStrike APIs.  
   1. In the CrowdStrike Falcon application, select ![cs-logo.png][image20] Support → API Clients and Keys.  
   2. Under the OAuth2 API Clients section, Add new API client.  
   3. Configure your new API client with these settings:  
      ![cs-add-new-api-client.png][image21]  
      * CLIENT NAME: Specify a name for the new API client.  
      * DESCRIPTION: (Optional) Specify a description for the new API client.  
      * API SCOPES → Event streams: Select the Read permissions check box.  
      * API SCOPES → Hosts: Select the Read permissions check box.  
   4. Click ADD.  
   5. Copy the values for the CLIENT ID, SECRET, and BASE URL, and save them, because you will need them when you configure the Data Collection settings in Cortex XSIAM.  
      Ensure that you save the SECRET value because this is the only time that it is displayed.  
      cs-api-client-created.png  
   6. Click DONE.  
2. Configure the CrowdStrike Platform collection in Cortex XSIAM.  
   1. In Cortex XSIAM, select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select CrowdStrike Platform, and click Connect.  
   3. Set these parameters:  
      * Name: Specify a descriptive name for your log collection configuration, preferably the same CLIENT NAME used when adding a new client API in the CrowdStrike Falcon application, as explained above.  
      * Base URL: Specify the BASE URL you received when you created the client API in the CrowdStrike Falcon application, as explained above.  
      * Client ID: Specify the CLIENT ID you received when you created the client API in the CrowdStrike Falcon application, as explained above.  
      * Secret: Specify the SECRET you received when you created the client API in the CrowdStrike Falcon application, as explained above.  
      * Collect: Select the items that you want to collect (Alerts, Hosts).  
   4. Click Test to validate access, and then click Enable.  
3. When events start to come in, a green check mark appears below the CrowdStrike Platform configuration, along with the amount of data received.

### Ingest raw EDR events from CrowdStrike Falcon Data Replicator

Abstract

Ingest raw EDR event data from CrowdStrike Falcon Data Replicator into Cortex XSIAM.

Cortex XSIAM enables ingestion of raw EDR event data from CrowdStrike Falcon Data Replicator (FDR), streamed to Amazon S3. In addition to all standard SIEM capabilities, this integration unlocks some advanced Cortex XSIAM features, enabling comprehensive analysis of data from all sources, enhanced detection and response, and deeper visibility into CrowdStrike FDR data.

Key benefits include:

* Querying all raw event data received from CrowdStrike FDR using XQL.  
* Querying critical modeled and unified EDR data via the `xdr_data` dataset.  
* Enriching incident and alert investigations with relevant context.  
* Grouping alerts with alerts from other sources to accelerate the scoping process of incidents, and to cut investigation time.  
* Leveraging the data for analytics-based detection.  
* Utilizing the data for rule-based detection, including correlation rules, BIOC, and IOC.  
* Leveraging the data within playbooks for incident response.

When Cortex XSIAM begins receiving EDR events from CrowdStrike FDR, it automatically creates a new dataset labeled `crowdstrike_fdr_raw`, allowing you to query all CrowdStrike FDR events using XQL. For example XQL queries, refer to the in-app XQL Library.

In addition, Cortex XSIAM parses and maps critical data into the `xdr_data` dataset and XDM data model, enabling unified querying and investigation across all supported EDR vendors' data, and unlocking key benefits like stitching and advanced analytics. While mapped data from all supported EDR vendors, including CrowdStrike, will be available in the `xdr_data` dataset, it's important to note that third-party EDR data present some limitations.

Third-party agents, including CrowdStrike, typically provide less data compared to our native agents, and do not include the same level of optimization for causality analysis and cloud-based analytics. Furthermore, external EDR rate limits and filters might restrict the availability of critical data required for comprehensive analytics. As a result, only a subset of our analytics-based detectors will function with third-party EDR data.

Raw event data from CrowdStrike FDR lacks key contextual information. To enhance its usability, we allocate additional resources to stitch it with other event data and data sources. Therefore, enabling the CrowdStrike FDR integration might temporarily make the tenant unavailable for a maintenance period of up to an hour.

We are continuously enhancing our support and using advanced techniques to enrich missing third-party data, while somehow replicating some proprietary functionalities available with our agents. This approach maximizes value for our customers using third-party EDRs within existing constraints. However, it’s important to recognize that the level of comprehensiveness achieved with our native agents cannot be matched, as much of the logic happens on the agent itself. These capabilities are unique, and are not found in typical SIEMs. Many of them, along with their underlying logic, are patented by Palo Alto Networks. Therefore, they should be regarded as added value beyond standard SIEM functionalities for customers who are not using our agents.

Ensure that your organization has a license for the CrowdStrike Falcon Data Replicator (FDR).

Ensure that CrowdStrike FDR is enabled. CrowdStrike FDR can only be enabled by CrowdStrike Support. If CrowdStrike FDR is not enabled, submit a support ticket through the CrowdStrike support portal.

Follow these steps to check if CrowdStrike FDR is enabled:

1. Log in to the CrowdStrike Falcon user interface using an account that has view/create permission for the API clients and keys page.  
2. Navigate to Support → API Clients and Keys.  
3. Verify that FDR AWS S3 Credentials and SQS Queue is listed.

Due to limitations with the S3 bucket used by CrowdStrike, data can only be collected once, by one system.

For more information on configuring data collection from CrowdStrike via Falcon Data Replicator, see CrowdStrike documentation.

###### Task 1: Create a CrowdStrike FDR feed

1. In the CrowdStrike user interface, select Support and resources → Resources and Tools → Falcon data replicator.  
2. Click the FDR feeds tab.  
3. Click Create feed.  
4. Enter a feed name.  
5. In Falcon Flight Control deployments, there is an option called Select which CID will manage this feed. In typical environments, the parent CID manages the feed for all of its child CIDs. This creates an aggregated feed that has data from all of the child CIDs. For information about aggregated feeds, and how they compare to individual feeds, see CrowdStrike documentation.  
   * To set up an aggregated feed, select the parent CID.  
   * To set up an individual feed, select a child CID or select both a parent CID and the Exclude Child CIDs option.  
   * To exclude only some of the child CIDs, don’t select the Exclude Child CIDs option. Instead, select Customize your FDR feed in the next step.  
6. Set the feed status.  
7. Select the method for creating your feed, from the following options:  
   * Create your FDR feed with default settings, where you get the recommended settings, including all current and future events, all secondary events (if available), and no partitions.  
   * Customize your FDR feed, where you start with the option to use a filter to get the specific events that you want in the feed. You can then customize secondary events and partitioning.  
8. Include secondary events. They are required for data stitching and enrichment.  
9. Optionally, in Flight Control deployments, edit the existing child CIDs included in the feed, and choose whether future CIDs are automatically included, by using the Include future CIDs option.  
10. Click Create feed.  
11. From the summary page that appears, copy and save all the information shown on the page somewhere safe, for later use. This page includes the credentials that are required for setting up an SQS consumer.  
    Ensure that you copy the Secret, and store it in a safe place. You will not be able to retrieve it later. If you need a new secret, you must reset the feed credentials.

###### Task 2: Configure CrowdStrike Falcon Data Replicator

1. Log in to CrowdStrike Falcon using an account that has view/create permission for the API clients and keys page.  
2. Navigate to cs-logo.pngSupport → API Clients and Keys.  
3. On the same line as FDR AWS S3 Credentials and SQS Queue, click Create new credentials.  
   CrowdStrike Falcon Data Replicator only supports one FDR credential configuration.  
4. Configure your new FDR credentials.  
   cs-fdr-credentials-created.png  
5. Copy the values for the CLIENT ID, SECRET, S3 IDENTIFIER, and SQS URL, and save them somewhere safe, because you will need them when you configure data collection in Cortex XSIAM.  
   Ensure that you save the SECRET value, because this is the only time that it is displayed. You can go back to this page later to copy the other credentials, but you will not have access to the secret again.  
6. Click DONE.

###### Task 3: Configure ingestion into Cortex XSIAM

1. In Cortex XSIAM, select Settings → Data Sources.  
2. On the Data Sources page, click Add Data Source, search for and select CrowdStrike Falcon Data Replicator, and click Connect.  
3. Set these parameters:  
   * Name: Specify a descriptive name for your log collection configuration.  
   * SQS URL: Specify the SQS URL you received when you created the FDR credential in CrowdStrike Falcon, as explained above.  
   * AWS Client ID: Specify the CLIENT ID you received when you created the FDR credential in CrowdStrike Falcon, as explained above.  
   * AWS Client Secret: Specify the SECRET you received when you created the FDR credential in CrowdStrike Falcon, as explained above.  
4. Click Test to validate access, and then click Enable.

When events start to come in, a green check mark appears below the CrowdStrike Falcon Data Replicator configuration, along with the amount of data received.

### Ingest raw EDR events from Microsoft Defender for Endpoint

Abstract

Ingest raw EDR event data from Microsoft Defender for Endpoint Events into Cortex XSIAM.

Cortex XSIAM enables ingestion of raw EDR event data from Microsoft Defender for Endpoint Events, streamed to Azure Event Hubs. In addition to all standard SIEM capabilities, this integration unlocks some advanced Cortex XSIAM features, enabling comprehensive analysis of data from all sources, enhanced detection and response, and deeper visibility into Microsoft Defender for Endpoint data. 

Key benefits include:

* Querying all raw event data received from Microsoft Defender for Endpoint using XQL.  
* Querying critical modeled and unified EDR data via the `xdr_data` dataset.  
* Enriching incident and alert investigations with relevant context.  
* Grouping alerts with alerts from other sources to accelerate the scoping process of incidents, and to cut investigation time.  
* Leveraging the data for analytics-based detection.  
* Utilizing the data for rule-based detection, including correlation rules, BIOC, and IOC.  
* Leveraging the data within playbooks for incident response.

When Cortex XSIAM begins receiving EDR events from Microsoft Defender for Endpoint Events, it automatically creates a new dataset labeled `msft_defender_raw`, allowing you to query all Microsoft Defender for Endpoint Events using XQL. For example XQL queries, refer to the in-app XQL Library.

In addition, Cortex XSIAM parses and maps critical data into the `xdr_data` dataset and XDM data model, enabling unified querying and investigation across all supported EDR vendors' data, and unlocking key benefits like stitching and advanced analytics. While mapped data from all supported EDR vendors, including Microsoft Defender for Endpoint Events, will be available in the `xdr_data` dataset, it's important to note that third-party EDR data present some limitations.

Third-party agents, including Microsoft Defender for Endpoint Events, typically provide less data compared to our native agents, and do not include the same level of optimization for causality analysis and cloud-based analytics. Furthermore, external EDR rate limits and filters might restrict the availability of critical data required for comprehensive analytics. As a result, only a subset of our analytics-based detectors will function with third-party EDR data.

We are continuously enhancing our support and using advanced techniques to enrich missing third-party data, while somehow replicating some proprietary functionalities available with our agents. This approach maximizes value for our customers using third-party EDRs within existing constraints. However, it’s important to recognize that the level of comprehensiveness achieved with our native agents cannot be matched, as much of the logic happens on the agent itself. These capabilities are unique, and are not found in typical SIEMs. Many of them, along with their underlying logic, are patented by Palo Alto Networks. Therefore, they should be regarded as added value beyond standard SIEM functionalities for customers who are not using our agents.

The generic Cortex XSIAM Azure Event Hub collector does not offer full functionality for EDR data (such as stitching), and is therefore not suitable for EDR data ingestion.

###### Task 1: Configure Microsoft Defender for Endpoint Events to stream raw data to Microsoft Azure Event Hub

Ensure that you do the following tasks before you begin configuring data collection.

* Create an Azure Event Hub. For more information, see [Quickstart: Create an event hub using Azure portal](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-create).  
  1. Create a resource group (optional if you already have a resource group configured).  
  2. Create an Event Hubs namespace.  
  3. Create an event hub within the namespace. On the Settings → Networking page → Public Access tab, ensure that you add Palo Alto Networks IP addresses to the Firewall allow list. Set Exception to Yes.  
  4. Ensure that you keep a copy of the Event Hub resource ID and the Event Hub name for use in the following procedures. To get your Event Hubs resource ID, go to your Azure Event Hub namespace page on Azure's Properties tab, and copy the text under Resource ID.  
  5. Create a storage account.  
* Ensure that you have Microsoft Defender user credentials to sign in as a Security Administrator.  
1. Enable raw data streaming:  
   * Sign in to the Microsoft Defender portal as a Security Administrator.  
   * Go to the data export settings page in the Microsoft Defender portal: System → Settings → Windows Defender XDR → Streaming API.  
   * Click \+Add.  
   * In the Name box, enter a name for your new data streaming settings.  
   * Select Forward events to Event Hub.  
   * In the Event-Hub Resource ID box, enter the Event Hub resource ID that you prepared in advance.  
   * In the Event-Hub box, enter the Event Hub name that you prepared in advance.  
   * For Event Types, select the event types that you want to stream.  
     If you select all event types and leave Event-Hub name empty, an event hub will be created for each category in the selected namespace. If you are not using a Dedicated Event Hubs ClusterEvent Hub, namespaces have a limit of 10 Event Hubs.  
   * Click Submit.  
   * Verify that the events that you selected are streaming by going to your Event Hubs namespace, Settings → Networking. Select the Event Hub name and the Consumer group, and then under Advanced properties, click View events. Check the Event body.  
2. In the Microsoft Azure console, open the Event Hubs page, and select the Azure Event Hub that you created for collection of Microsoft Defender logs.  
3. Save a copy of the following parameters from your configured event hub, because you will need them when configuring data collection in Cortex XSIAM:  
   * Your **event hub’s consumer** group:  
     1. Select Entities → Event Hubs, and select your event hub.  
     2. Select Entities → Consumer groups, and select your event hub.  
     3. In the Consumer group table, copy the applicable value listed in the Name column for your Cortex XSIAM data collection configuration.  
   * Your **event hub’s connection string** for the designated policy:  
     1. Select Settings → Shared access policies.  
     2. In the Shared access policies table, select the applicable policy.  
     3. Copy the Connection string-primary key.  
   * Your **storage account connection string** required for partitions lease management and checkpointing in Cortex XSIAM:  
     1. Open the Storage accounts page, and either create a new storage account or select an existing one, which will contain the storage account connection string.  
     2. Select Security \+ networking → Access keys, and click Show keys.  
     3. Copy the applicable Connection string.

###### Task 2: Configure the Microsoft Defender for Endpoint Events collector in Cortex XSIAM

1. Select Settings → Data Sources.  
2. On the Data Sources page, click Add Data Source, search for and select Microsoft Defender for Endpoint, and click Connect.  
3. Set these parameters:  
   * Name: Specify a unique descriptive name for your log collection configuration. You cannot change this name later.  
   * Event Hub Connection String: Specify your event hub’s connection string for the designated policy.  
   * Storage Account Connection String: Specify your storage account’s connection string for the designated policy.  
   * Consumer Group: Specify your event hub’s consumer group.  
4. Click Test to validate access, and then click Save.  
   When events start to come in, a green check mark appears beneath the Microsoft Defender for Endpoint configuration, with the amount of data received.

### Ingest raw EDR events from SentinelOne DeepVisibility

Abstract

Ingest raw EDR event data from SentinelOne DeepVisibility into Cortex XSIAM.

Cortex XSIAM enables ingestion of raw EDR event data from SentinelOne DeepVisibility, streamed via Cloud Funnel to Amazon S3. In addition to all standard SIEM capabilities, this integration unlocks some advanced Cortex XSIAM features, enabling comprehensive analysis of data from all sources, enhanced detection and response, and deeper visibility into SentinelOne data.

Key benefits include:

* Querying all raw event data received from SentinelOne using XQL.  
* Querying critical modeled and unified EDR data via the `xdr_data` dataset.  
* Enriching incident and alert investigations with relevant context.  
* Grouping alerts with alerts from other sources to accelerate the scoping process of incidents, and to cut investigation time.  
* Leveraging the data for analytics-based detection.  
* Utilizing the data for rule-based detection, including correlation rules, BIOC, and IOC.  
* Leveraging the data within playbooks for incident response.

When Cortex XSIAM begins receiving EDR events from SentinelOne, it automatically creates a new dataset labeled `sentinelone_deep_visibility_raw`, allowing you to query all SentinelOne events using XQL. For example XQL queries, refer to the in-app XQL Library.

In addition, Cortex XSIAM parses and maps critical data into the `xdr_data` dataset and XDM data model, enabling unified querying and investigation across all supported EDR vendors' data and unlocking key benefits like stitching and advanced analytics. While mapped data from all supported EDR vendors, including SentinelOne DeepVisibility, will be available in the `xdr_data` dataset, it's important to note that third-party EDR data present some limitations.

Third-party agents, including SentinelOne, typically provide less data compared to our native agents, and do not include the same level of optimization for causality analysis and cloud-based analytics. Furthermore, external EDR rate limits and filters might restrict the availability of critical data required for comprehensive analytics. As a result, only a subset of our analytics-based detectors will function with third-party EDR data.

We are continuously enhancing our support and using advanced techniques to enrich missing third-party data, while somehow replicating some proprietary functionalities available with our agents. This approach maximizes value for our customers using third-party EDRs within existing constraints. However, it’s important to recognize that the level of comprehensiveness achieved with our native agents cannot be matched, as much of the logic happens on the agent itself. These capabilities are unique, and are not found in typical SIEMs. Many of them, along with their underlying logic, are patented by Palo Alto Networks. Therefore, they should be regarded as added value beyond standard SIEM functionalities for customers who are not using our agents.

* The SentinelOne DeepVisibility logs that will be collected by your dedicated Amazon S3 bucket must adhere to the following guidelines:  
  * Each log file must use the 1 log per line format as multi-line format is not supported.  
  * The log format must be compressed as gzip or uncompressed.  
  * For best performance, we recommend limiting each file size to up to 50 MB (compressed).  
* The minimum AWS permissions required for an Amazon S3 bucket and Amazon Simple Queue Service (SQS) are:  
  * **Amazon S3 bucket**: `GetObject`  
  * **SQS**: `ChangeMessageVisibility`, `ReceiveMessage`, and `DeleteMessage`  
* Determine how you want to provide access to Cortex XSIAM to your logs and to perform API operations. You have the following options:  
  * Designate an AWS IAM user, where you will need to know the Account ID for the user and have the relevant permissions to create an access key/id for the relevant IAM user. If you do not have a designated AWS IAM user configured yet, instructions for this are included in the following procedures.  
  * Create an assumed role in AWS to delegate permissions to a Cortex XSIAM AWS service. This role grants Cortex XSIAM access to your flow logs. This is the Assumed Role option mentioned later in the procedures that follow. To create an assumed role for Cortex XSIAM, see [Create an assumed role](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-wPcVj~5r_xRuS_NmMalnOQ).  
    For more information about assumed roles, see [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).  
* To collect Amazon S3 logs that use server-side encryption (SSE), the user role must have an IAM policy that states that Cortex XSIAM has kms:Decrypt permissions. With this permission, Amazon S3 automatically detects if a bucket is encrypted and decrypts it. If you want to collect encrypted logs from different accounts, you must have the decrypt permissions for the user role also in the key policy for the master account Key Management Service (KMS). For more information, see [Allowing users in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html).

###### Task 1: Configure an Amazon S3 bucket

Task A: Create a dedicated Amazon S3 bucket to store SentinelOne DeepVisibility EDR data

This step provides general guidelines. For more information, see [Creating a bucket using the Amazon S3 Console](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html).

It is your responsibility to define a retention policy for your Amazon S3 bucket by creating a Lifecycle rule on the Management tab. We recommend setting the retention policy to at least 7 days to ensure that the data is retrieved under all circumstances.

1. Log in to the AWS Management Console and navigate to the S3 Service.  
2. Create a new S3 bucket:  
   1. Click Create bucket.  
   2. For Bucket Name, enter a unique name for the bucket (for example, `xsiam-s1-edr-data`).  
   3. Choose an appropriate AWS Region.  
   4. Set Block all public access to Enabled.  
   5. Click Create bucket.  
3. Set up the Bucket policy:  
   1. Click the Permissions tab of your new bucket.

Under Bucket policy, click Edit and add the following policy to allow SentinelOne DeepVisibility to write data there.  
Replace `your-sentinelone-account-id` with the relevant value for your environment; replace `xsiam-s1-edr-data` with the name of your new bucket.  
{  
    "Version": "2012-10-17",  
    "Statement": \[  
        {  
            "Effect": "Allow",  
            "Principal": {  
                "AWS": "your-sentinelone-account-id"  
            },  
            "Action": "s3:PutObject",  
            "Resource": "arn:aws:s3:::xsiam-s1-edr-data/\*"  
        }  
    \]

2. }

Task B: Configure an Amazon Simple Queue Service (SQS) and grant it permission to receive messages from S3

Ensure that you create your Amazon S3 bucket and Amazon SQS queue in the same region.

1. In the [Amazon SQS Console](https://console.aws.amazon.com/sqs/), click Create Queue.  
2. Configure the following settings, where the default settings should be configured unless otherwise indicated.  
   * Type: Select Standard queue (default).  
   * Name: Specify a descriptive name for your SQS queue.  
   * Configuration section: Keep the default settings for the various fields.

Access policy → Choose method: Select Advanced and update the Access policy code in the editor window to enable your Amazon S3 bucket to publish event notification messages to your SQS queue. Use this sample code as a guide for defining the `“Statement”` with the following definitions.  
**`“Resource”`**: Keep the automatically generated ARN for the SQS queue that is set in the code, which uses the format `“arn:sns:Region:account-id:topic-name”`.  
You can retrieve your bucket’s ARN by opening the [Amazon S3 Console](https://console.aws.amazon.com/s3/) in a browser window. In the Buckets section, select the bucket that you created for collecting the Amazon S3 flow logs, click Copy ARN, and paste the ARN in the field.  
bucket-copy-arn.png  
For more information on granting permissions to publish messages to an SQS queue, see [Granting permissions to publish event notification messages to a destination](https://docs.aws.amazon.com/AmazonS3/latest/userguide/grant-destinations-permissions-to-s3.html).  
{  
  "Version": "2012-10-17",  
  "Statement": \[  
    {  
      "Effect": "Allow",  
      "Principal": {  
        "Service": "s3.amazonaws.com"  
      },  
      "Action": "SQS:SendMessage",  
      "Resource": "\[Leave automatically generated ARN for the SQS queue defined by AWS\]",  
      "Condition": {  
        "ArnLike": {  
          "aws:SourceArn": "\[ARN of your Amazon S3 bucket\]"  
        }  
      }  
    }  
  \]

* }  
  * Dead-letter queue section: We recommend that you configure a queue for sending undeliverable messages by selecting Enabled, and then in the Choose queue field selecting the queue to send the messages. You may need to create a new queue for this, if you do not already have one set up. For more information, see [Amazon SQS dead-letter queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html).  
3. Click Create queue.  
   When the SQS is created, a message indicating that the queue was successfully configured is displayed at the top of the page.

Task C: Configure an event notification to your Amazon SQS whenever a file is written to your Amazon S3 bucket

1. Open the [Amazon S3 Console](https://console.aws.amazon.com/s3/) and in the Properties tab of your Amazon S3 bucket, scroll down to the Event notifications section, and click Create event notification.  
2. Configure the following settings:  
   * Event name: Specify a descriptive name for your event notification containing up to 255 characters.  
   * Prefix: Do not set a prefix, because the Amazon S3 bucket is meant to be a dedicated bucket for collecting only network flow logs.  
   * Event types: Select All object create events for the type of event notifications that you want to receive.  
   * Destination: Select SQS queue to send notifications to an SQS queue to be read by a server.  
   * Specify SQS queue: You can either select Choose from your SQS queues and then select the SQS queue, or select Enter SQS queue ARN and specify the ARN in the SQS queue field.  
     You can retrieve your SQS queue ARN by opening another instance of the AWS Management Console in a browser window, opening the [Amazon SQS Console](https://console.aws.amazon.com/sqs/), and selecting the Amazon SQS that you created. In the Details section, under ARN, click the copy icon (copy-icon.png)), and paste the ARN in the field.  
     sqs-arn2.png  
3. Click Save changes.  
   When the event notification is created, a message indicating that the event notification was successfully created is displayed at the top of the page.  
   If you receive an error when trying to save your changes, check that the permissions are set up correctly, and fix them if necessary.

Task D: Configure authentication\\authorization if you have not done so yet

For **Assumed Role**, follow these instructions: [Create an assumed role](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-wPcVj~5r_xRuS_NmMalnOQ), and then return to this page to [Configure SentinelOne DeepVisibility](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#UUID-5ee619e7-1356-3b31-3dab-5170f9747f7b_section-idm234481154153413).

For **IAM access key**:

1. Create an IAM Policy that grants permissions for SQS and S3:  
   1. In the AWS Console, navigate to the IAM service, and click Policies.  
   2. Click Create policy.  
   3. Select the JSON policy editor.

Use this sample code as a guide for defining the “Statement” with the following definitions:  
{  
    "Version": "2012-10-17",  
    "Statement": \[  
        {  
            "Sid": "S3ReadAccess",  
            "Effect": "Allow",  
            "Action": \[  
                "s3:GetObject",  
                "s3:ListBucket"  
            \],  
            "Resource": \[  
                "\[ARN for the S3 Bucket Name defined by AWS\]", \#example: "arn:aws:s3:::bucketname/xsiam-s1-edr-data/"  
                "\[ARN for the S3 Bucket path defined by AWS\]" \#example: "arn:aws:s3:::bucketname/xsiam-s1-edr-data/\*"  
            \]  
        },  
        {  
            "Sid": "SQSReceiveAccess",  
            "Effect": "Allow",  
            "Action": \[  
                "sqs:ReceiveMessage",  
                "sqs:GetQueueAttributes"  
            \],  
            "Resource": "\[ARN for the SQS queue defined by AWS\]"  
        }  
    \]

4. }  
   5. Click Next.  
   6. For Policy name, enter a name.  
   7. Click Create policy.  
2. Create an IAM User:  
   1. In the AWS Console, navigate to the IAM service, and click Users.  
   2. Click Create user.  
   3. For User name, enter a name (for example, `cortex-xsiam-s3`).  
   4. Attach the IAM Policy that you created in Step 1\.  
   5. Click Next.  
   6. Click Create user.  
3. Configure access keys for the AWS IAM User:  
   It is the responsibility of your organization to ensure that the user who creates the access key is assigned the relevant permissions. Otherwise, this can cause the process to fail with errors.  
   1. Open the [AWS IAM Console](https://console.aws.amazon.com/iam/), and in the navigation pane, select Access management → Users.  
   2. Select the User name of the AWS IAM user.  
   3. Select the Security credentials tab, scroll down to the Access keys section, and click Create access key.  
   4. Click the copy icon next to the Access key ID and Secret access key keys, where you must click Show secret access key to see the secret key, and save a copy of them somewhere safe before closing the window. You will need to provide these keys when you edit the Access policy of the SQS queue, and when setting the AWS Client ID and AWS Client Secret in Cortex XSIAM. If you forget to record the keys and close the window, you will need to generate new keys and repeat this process.  
      For more information, see [Managing access keys for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).  
4. Update the Access policy of your Amazon SQS queue:  
   1. In the [Amazon SQS Console](https://console.aws.amazon.com/sqs/), select the SQS queue that you created when you configured an Amazon Simple Queue Service (SQS).  
   2. Select the Access policy tab, and click Edit to edit the Access policy code in the editor window, to enable the IAM user to perform operations on the Amazon SQS with the permissions `SQS:ChangeMessageVisibility`, `SQS:DeleteMessage`, and `SQS:ReceiveMessage`. Use this sample code as a guide for defining the `“Sid”: “__receiver_statement”` with the following definitions.  
      * `“aws:SourceArn”`: Specify the ARN of the AWS IAM user. You can retrieve the User ARN from the Security credentials tab, which you accessed when you configured access keys for the AWS API user.

`“Resource”`: Keep the automatically generated ARN for the SQS queue that is set in the code, which uses the format `“arn:sns:Region:account-id:topic-name”`.  
For more information on granting permissions to publish messages to an SQS queue, see [Granting permissions to publish event notification messages to a destination](https://docs.aws.amazon.com/AmazonS3/latest/userguide/grant-destinations-permissions-to-s3.html).  
{  
  "Version": "2012-10-17",  
  "Statement": \[  
    {  
      "Effect": "Allow",  
      "Principal": {  
        "Service": "s3.amazonaws.com"  
      },  
      "Action": "SQS:SendMessage",  
      "Resource": "\[Leave automatically generated ARN for the SQS queue defined by AWS\]",  
      "Condition": {  
        "ArnLike": {  
          "aws:SourceArn": "\[ARN of your Amazon S3 bucket\]"  
        }  
      }  
    },  
   {  
      "Sid": "\_\_receiver\_statement",  
      "Effect": "Allow",  
      "Principal": {  
        "AWS": "\[Add the ARN for the AWS IAM user\]"  
      },  
      "Action": \[  
        "SQS:ChangeMessageVisibility",  
        "SQS:DeleteMessage",  
        "SQS:ReceiveMessage"  
      \],  
      "Resource": "\[Leave automatically generated ARN for the SQS queue defined by AWS\]"  
    }  
  \]

* }  
  3. Click Save.

###### Task 2: Configure SentinelOne DeepVisibility

1. In SentinelOne DeepVisibility, select Configure → Policy & Settings and in the Singularity Data Lake section, click Cloud Funnel.  
2. For Cloud Provider, select AWS (Amazon Web Services).  
3. For S3 Bucket Name, enter the name of the Amazon S3 bucket that you created for SentinelOne DeepVisibility log ingestion.  
4. For Telemetry Streaming, select Enable.  
5. In the Query Filters box, create a query that includes the agents that should send data to the S3 bucket.  
6. To validate the query, click Validate.  
7. For Fields to include, ensure that all fields are selected.  
8. Click Save.

###### Task 3: Configure ingestion into Cortex XSIAM

1. In Cortex XSIAM, select Settings → Data Sources.  
2. On the Data Sources page, click Add Data Source, search for and select **`SentinelOne - Deep Visibility`**, and click Connect.  
3. Use the toggle to select either Access Key or Assumed Role.  
4. Set these parameters, depending on your choice in the previous step:  
   * For the Access Key option:  
     * Name: Specify a descriptive name for your log collection configuration. This name must be unique in your environment.  
     * SQS URL: Specify the SQS URL that you received for the AWS S3 queue when you configured the Amazon Simple Queue Service (SQS), as explained above.  
     * AWS Client ID: Specify the Client ID that you received when you configured the AWS IAM user, as explained above.  
     * AWS Client Secret: Specify the Secret that you received when you configured the AWS IAM user, as explained above.  
   * For the Assumed Role option:  
     * Name: Specify a descriptive name for your log collection configuration. This name must be unique in your environment.  
     * SQS URL: Specify the SQS URL that you received for the AWS S3 queue when you configured the Amazon Simple Queue Service (SQS), as explained above.  
     * Role ARN: Specify the role ARN that you received when you created the assumed role.  
     * External Id: Specify the External ID that you received when you created the assumed role.  
5. Click Test to validate access, and then click Enable.  
   After events start to come in, a green check mark appears below the SentinelOne \- DeepVisibility configuration, along with the amount of data received.

## Ingest cloud assets

Abstract

You can ingest cloud assets from different third-party sources using Cortex XSIAM.

You can ingest cloud assets from different third-party sources.

### Ingest Cloud Assets from AWS

Abstract

Extend Cortex XSIAM visibility into cloud assets from AWS.

Cortex XSIAM provides a unified, normalized asset inventory for cloud assets in AWS. This capability provides deeper visibility to all the assets and superior context for incident investigation.

To receive cloud assets from AWS, you must configure the Data Sources settings in Cortex XSIAM using the Cloud Inventory data collector to configure the AWS wizard. The AWS wizard includes instructions to be completed both in AWS and the AWS wizard screens. After you set up data collection, Cortex XSIAM begins receiving new data from the source.

As soon as Cortex XSIAM begins receiving cloud assets, you can view the data in Assets → Cloud Inventory, where All Assets and Specific Cloud Assets pages display the data in a table format.

To configure the AWS cloud assets collection in Cortex XSIAM.

1. Open the AWS wizard in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select Cloud Inventory, and click Connect.  
   3. Click AWS.  
2. Define the Account Details screen of the wizard.  
   Setting the connection parameters on the right-side of the screen is dependent on certain configurations in AWS as explained below.  
   1. Select the Organization Level as either Account (default), Organization, or Organization Unit. The Organization Level that you select changes the instructions and fields displayed on the screen.  
   2. Sign in to your [AWS master account](https://us-east-1.signin.aws.amazon.com/oauth?SignatureVersion=4&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIX36KZ4MDWDXXIGA&X-Amz-Date=2021-11-02T20%3A56%3A17.707Z&X-Amz-Signature=21b438a41bc3e6a9688ebd09d095598c470003224fa04eee8a50e6455b9a182b&X-Amz-SignedHeaders=host&client_id=arn%3Aaws%3Aiam%3A%3A015428540659%3Auser%2Fcloudformation&code_challenge=Sy3gtQMJ2zZt8913FfHTuXXULPj_nLOIs77VSQ96Jnc&code_challenge_method=SHA-256&redirect_uri=https%3A%2F%2Fus-east-1.console.aws.amazon.com%2Fcloudformation%2Fhome%3Fregion%3Dus-east-1%26state%3DhashArgs%2523%252Fstacks%252Fcreate%252Freview%253FtemplateURL%253Dhttps%253A%252F%252Fcortex-xdr-xcloud-onboarding-scripts-dev.s3.us-east-2.amazonaws.com%252Fcortex-xdr-xcloud-master-dev-1.0.0.template%2526stackName%253DXDRCloudApp%2526param_ExternalID%253Dadbe79b2-4359-4dbe-a9a1-efebdb02e286%26isauthcode%3Dtrue&region=us-east-1&response_type=code&state=hashArgs%23%2Fstacks%2Fcreate%2Freview%3FtemplateURL%3Dhttps%3A%2F%2Fcortex-xdr-xcloud-onboarding-scripts-dev.s3.us-east-2.amazonaws.com%2Fcortex-xdr-xcloud-master-dev-1.0.0.template%26stackName%3DXDRCloudApp%26param_ExternalID%3Dadbe79b2-4359-4dbe-a9a1-efebdb02e286).  
      aws-sign-in.png  
   3. Create a stack called XDRCloudApp using the preset Cortex XSIAM template in AWS.  
      The following details are automatically filled in for you in the AWS CloudFormation stack template:  
      * Stack Name: The default name for the stack is XDRCloudApp.  
      * CortexXDRRoleName: The name of the role that will be used by Cortex XSIAM to authenticate and access the resources in your AWS account.  
      * External ID: The Cortex XSIAM Cloud ID, a randomly generated UUID that is used to enable the trust relationship in the role's trust policy.  
   4. To create the stack, accept the IAM acknowledgment for resource creation by selecting the I acknowledge that AWS CloudFormation might create IAM resources with custom names checkbox, and click Create Stack.  
   5. Wait for the Status to update to CREATE\_COMPLETE in the Stacks page that is displayed, and select the XDRCloudAPP stack under the Stack name column in the table.  
   6. Select the Outputs tab and copy the Value of the Role ARN.  
   7. Paste the Role ARN value in one of the following fields in the Account Details screen in Cortex XSIAM. The field name is dependent on the Organization Level that you selected.  
      * Account: Paste the value in the Account Role ARN field.  
      * Organization: Paste the value in the Master Role ARN field.  
      * Organization Unit: Paste the value in the Master Role ARN field.  
   8. Set the Root ID in Cortex XSIAM.  
      This step is only relevant if you’ve configured the Organization Level as Organization in the Account Details screen in Cortex XSIAM. Otherwise, you can skip this step if the Organization Level is set to Account or Organization Unit.  
      * From the main menu of the AWS Console, select \<your username\> → My Organization.  
      * Copy the Root ID displayed under the Root directory and paste it in the Root ID field in the Account Details screen in Cortex XSIAM.  
   9. Set the Organization Unit ID in Cortex XSIAM.  
      This step is only relevant if you’ve configured the Organization Level as Organization Unit in the Account Details screen in Cortex XSIAM. Otherwise, you can skip this step if the Organization Level is set to Account or Organization.  
      * On the main menu of the AWS Console, select your username, and then My Organization.  
      * Select the Organization Unit with an icon-ou (aws-ou-icon.png) beside it in the organizational structure that you want to configure.  
      * Copy the ID and paste it in the Organization Unit ID field in the Account Details screen in Cortex XSIAM.  
   10. Define the following remaining connection parameters in the Account Details screen in Cortex XSIAM:  
       * Account Role External ID / Master External ID: The name of this field is dependent on the Organization Level configured. This field is automatically populated with a value. You can either leave this value or replace it with another value.  
       * Cortex XDR Collection Name: Specify a name for your Cortex XSIAM collection that is displayed underneath the Cloud Inventory configuration for this AWS collection.  
   11. Click Next.  
3. Define the Configure Member Accounts screen of the wizard.  
   This wizard screen is only displayed if you’ve configured the Organization Level as Organization or Organization Unit in the Account Details screen in Cortex XSIAM. Otherwise, you can skip this step when the Organization Level is set to Account.  
   Configuring member accounts is dependent on creating a stack set and configuring stack instances in AWS, which can be performed using either the Amazon Command Line Interface (CLI) or Cloud Formation template via the AWS Console. Use one of the following methods:

###### Define the account credentials using Amazon CLI

1. On the Configure Member Accounts page, select the Amazon CLI tab, which is displayed by default.  
2. Open the Amazon CLI.  
   For more information on how to set up the AWS CLI tool, see the [AWS Command Line Interface Documentation](https://aws.amazon.com/cli/).  
3. Run the following command to create a stack set, which you can copy from the Configure Member Accounts screen by selecting the copy icon (gcp-copy.png), and paste in the Amazon CLI. This command includes the Role Name and External ID field values configured from the wizard screen.  
   aws cloudformation create-stack-set \--stack-set-name StackSetCortexXdr01 \--template-url https://cortex-xdr-xcloud-onboarding-scripts-dev.s3.us-east-2.amazonaws.com/cortex-xdr-xcloud-master-dev-1.0.0.template \--permission-model SERVICE\_MANAGED \--auto-deployment Enabled=true,RetainStacksOnAccountRemoval=true \--parameters ParameterKey=ExternalID,ParameterValue=c9a7024c-3f07-40ed-a4fb-c3a5eba778e2 \--capabilities CAPABILITY\_NAMED\_IAM  
4. Run the following command to add stack instances to your stack set, which you can copy from the Configure Member Accounts screen by selecting the copy icon (gcp-copy.png), and paste in the Amazon CLI. For the `--deployment-targets` parameter, specify the organization root ID to deploy to all accounts in your organization, or specify Organization Unit IDs to deploy to all accounts in these Organization Units. In this parameter, you will need to replace `<Org_OU_ID1>`, `<Org_OU_ID2>`, and `<Region>` according to your AWS settings.  
   aws cloudformation create-stack-instances \--stack-set-name StackSetCortexXdr01 \--deployment-targets OrganizationalUnitIds='\["\<Org\_OU\_ID1\>", "\<Org\_OU\_ID2\>"\]' \--regions '\["\<Region\>"\]'  
   In this example, the Organization Units are populated with `ou-rcuk-1x5j1lwo` and `ou-rcuk-slr5lh0a` IDs.  
   aws cloudformation create-stack-instances \--stack-set-name StackSet\_myApp \--deployment-targets OrganizationalUnitIds='\["ou-rcuk-1x5j1lwo", "ou-rcuk-slr5lh0a"\]' \--regions '\["eu-west-1"\]'  
   Once completed, in the AWS Console, select Services → CloudFormation → StackSets, and you can see the StackSet is now listed in the table.  
5. Review the Summary screen of the wizard.  
   If something needs to be corrected, click Back to correct it.  
6. Click Create.  
   Once cloud assets from AWS start to come in, a green check mark appears underneath the Cloud Inventory configuration with the Last collection time displayed. It can take a few minutes for the Last Collection time to display as the processing completes.  
   Whenever the Cloud Inventory data collector integrations are modified by using the Edit, Disable, or Delete options, it can take up to 10 minutes for these changes to be reflected in Cortex XSIAM.

###### Define the account credentials using AWS CloudFormation

1. On the Configure Member Accounts page, select the Cloud Formation tab.  
2. In the on-screen step Download the CloudFormation template, click template. Download the template file. The name of the downloaded file is `cortex-xdr-aws-master-ro-1.0.0.template`.  
3. Sign in to your AWS Master Account using the AWS console, select Services → CloudFormation → StackSets, and click Create StackSet.  
4. Define the following settings:  
   \-Select Template is ready.  
   \-Select Upload a template file, Choose file, and select the CloudFormation template that you downloaded.  
5. Click Next.  
6. Define the following settings.  
   \-StackSet name: Specify a name for the StackSet.  
   ExternalID: The ExternalID value specified here must be copied from the one populated in the External ID field on the right-side of the Configure Member Accounts screen in Cortex XSIAM .  
7. Click Next.  
8. Select Service-managed permissions, and click Next.  
9. Define the following settings.  
   Deployment targets  
   \-Select Deploy to the organization.  
   \-Select Enabled for Automatic deployments.  
   \-Select Delete stacks for Account removal behavior.  
   Specify regions  
   \-Select one region only. (It can be any region.)  
   Deployment options  
   \-For the Maximum concurrent accounts, select Percentage, and in the field specify 100\.  
   \-For the Failure tolerance, select Percentage, and in the field specify 100\.  
10. Click Next.  
11. To create the StackSet, accept the IAM acknowledgment for resource creation by selecting the I acknowledge that AWS CloudFormation might create IAM resources with custom names checkbox, and click Submit.  
    When the process completes, the Status of the StackSet is SUCCEEDED in the StackSet details page.  
12. Review the Summary screen of the wizard.  
    If something needs to be corrected, click Back to correct it.  
13. Click Create.  
    Once cloud assets from AWS start to come in, a green check mark appears underneath the Cloud Inventory configuration with the Last collection time displayed. It can take a few minutes for the Last Collection time to display as the processing completes.  
    Whenever the Cloud Inventory data collector integrations are modified by using the Edit, Disable, or Delete options, it can take up to 10 minutes for these changes to be reflected in Cortex XSIAM.

After Cortex XSIAM begins receiving AWS cloud assets, you can view the data in Assets → Cloud Inventory, where All Assets and Specific Cloud Assets pages display the data in a table format. For more information, see Cloud Inventory Assets.

### Ingest Cloud Assets from Google Cloud Platform

Abstract

Extend Cortex XSIAM visibility into cloud assets from Google Cloud Platform.

Cortex XSIAM provides a unified, normalized asset inventory for cloud assets in Google Cloud Platform (GCP). This capability provides deeper visibility to all the assets and superior context for incident investigation.

To receive cloud assets from GCP, you must configure the Data Sources settings in Cortex XSIAM using the Cloud Inventory data collector to configure the GCP wizard. The GCP wizard includes instructions to be completed both in GCP and the GCP wizard screens. After you set up data collection, Cortex XSIAM begins receiving new data from the source.

As soon as Cortex XSIAM begins receiving cloud assets, you can view the data in Assets → Cloud Inventory, where All Assets and Specific Cloud Assets pages display the data in a table format.

To configure the GCP cloud assets collection in Cortex XSIAM.

1. Open the GCP wizard in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select Cloud Inventory, and click Connect.  
   3. Click Google Cloud Platform.  
2. Define the Configure Account screen of the wizard.  
   Setting the connection parameters on the right-side of the screen is dependent on certain configurations in GCP as explained below.  
   1. Select the Organization Level as either Project (default), Folder, or Organization. The Organization Level that you select changes the instructions.  
   2. Register your application for [Cloud Asset API](https://console.cloud.google.com/flows/enableapi?apiid=cloudasset.googleapis.com&redirect=https://console.cloud.google.com&_ga=2.163236540.1261454100.1634719692-955775394.1626341431&_gac=1.238218932.1633517387.EAIaIQobChMI_Kmusc618wIVOIKDBx0wtQ9kEAAYASAAEgI8tvD_BwE) in Google Cloud Platform, Select a project where your application will be registered, and click Continue.  
      The Cloud Asset API is enabled.  
   3. Click Continue to open the [GCP Cloud Console](https://console.cloud.google.com/home/dashboard).  
   4. On the main menu, select the project menu.  
   5. In the window that opens, perform the following:  
      * From the Select from menu, select the organization that you want.  
      * The next steps to perform in Google Cloud Platform are dependent on the Organizational Level you selected in Cortex XSIAM \- Project, Folder, or Organization.  
        * **Project or Folder Organization Level**: In the table, copy one of the following IDs that you want to configure and paste it in the designated field in the Configure Account screen in Cortex XSIAM . The field in Cortex XSIAM is dependent on the Organizational Level you selected.  
          **\-Project**: Contains a project icon (gcp-project-icon.png) beside it, and the ID should be pasted in the Project ID field in Cortex XSIAM.  
          **\-Folder**: Contains a folder icon (gcp-folder-icon.png) beside it, and the ID should be pasted in the Folder ID field in Cortex XSIAM.  
          When you are finished, click CANCEL to close the window.  
        * **Organization is the Organization Level**: Select the ellipsis icon (gcp-ellipsis-icon.png) → Settings. In the Settings page, copy the Organization ID for the applicable organization that you want to configure and paste it in the Organization Id field in the Configure Account screen in Cortex XSIAM.  
   6. Select the menu icon → Storage → Cloud Storage → Browser.  
   7. You can either use an existing bucket from the list or create a new bucket. Copy the Name of the bucket and paste it in the Bucket Name field in the Configure Account screen in Cortex XSIAM.  
   8. Define the following remaining connection parameters in the Configure Account screen in Cortex XSIAM.  
      * Bucket Directory Name: You can either leave the default directory as Exported-Assets or define a new directory name that will be created for the exported assets collected for the bucket configured in GCP.  
      * Cortex XDR Collection Name: Specify a name for your Cortex XSIAM collection that is displayed underneath the Cloud Inventory configuration for this GCP collection.  
   9. Click Next.  
3. Define the Account Details screen of the wizard.  
   1. Download the Terraform script. The name of the file downloaded is dependent on the Organizational Level that you configured in the Configure Account screen of the wizard.  
      * Folder: `cortex-xdr-gcp-folder-ro.tf`  
      * Project: `cortex-xdr-gcp-project-ro.tf`  
      * Organization: `cortex-xdr-gcp-organization-ro.tf`  
   2. Login to the [Google Cloud Shell](https://shell.cloud.google.com/).  
      gcp-cloud-shell.png  
   3. Click Continue to open the Cloud Shell Editor.  
      gcp-cloud-shell-editor.png  
   4. Select File → Open, and Open the Terraform script that you downloaded from Cortex XSIAM.  
   5. Use the following commands to upload the Terraform script, which you can copy from the Account Details screen in Cortex XSIAM using the copy icon (gcp-copy.png).  
      * **`terraform init`**: Initializes the Terraform script. You need to wait until the initialization is complete before running the next command as indicated in the image below.

| gcp-terraform-init-complete.png |
| :---: |

      *   
        **`terraform apply`**: When running this command, you are asked to enter the following values.  
        * `var.assets_bucket_name`: Specify the GCP storage Bucket Name that you configured in the Configure Account screen of the wizard to contain GCP cloud asset data.  
        * `var.host_project_id`: Specify the GCP Project ID to host the XDR service account and bucket, which you registered your application. Ensure that you use a permanent project.  
        * `var.project_id`: Specify the Project ID, Folder ID, or Organization ID that you configured in the Configure Account screen of the wizard from GCP.  
          After specifying all the values, you need to Authorize gcloud to use your credentials to make this GCP API call in the Authorize Cloud Shell dialog box that is displayed.  
          Before the action completes, you need to confirm whether you want to perform these actions, and after the process finishes running an Apply complete indication is displayed.  
          gcp-terraform-apply-complete.png  
          You can view the output JSON file called `cortex-service-account-<GCP host project ID>.json` by running the `ls` command.  
   6. Download the JSON file from Google Cloud Shell.  
      * In the Google Cloud Shell console, select ellipsis icon (gcp-ellipsis-icon.png) → Download.

| gcp-download-file-folder.png |
| :---: |

      *   
        Select the JSON file produced after running the Terraform script, and click Download.  
   7. Upload the downloaded Service Account Key JSON file in the Configure Account screen in Cortex XSIAM. You can drag and drop the file, or Browse to the file.  
   8. Click Next.  
4. (Optional) Define the Change Asset Logs screen of the wizard.  
   You can skip this step if you’ve already configured a Google Cloud Platform data collector with a Pub/Sub asset feed collection.  
   1. In the [GCP Console](https://console.cloud.google.com/home/dashboard), search for Topics, and select the Topics link.  
   2. CREATE TOPIC.  
   3. Specify a Topic ID, and CREATE TOPIC.  
      A Topic name is automatically populated underneath the Topic ID field.  
      The new topic is listed in the table in the Topics page.  
   4. Run the following command to create a feed on an asset using the gcloud CLI tool, which you can copy from the Change Asset Logs screen in Cortex XSIAM by selecting the copy icon (gcp-copy.png), and paste in the gcloud CLI tool.  
      For more information on the gcloud CLI tool. see [gcloud tool overview](https://cloud.google.com/sdk/gcloud).  
      gcloud asset feeds create \<FEED\_ID\> \--project=xdr-cloud-projectid \--pubsub-topic="\<Topic name\>" \--content-type=resource \--asset-types="compute.googleapis.com/Instance,compute.googleapis.com/Image,compute.googleapis.com/Disk,compute.googleapis.com/Network,compute.googleapis.com/Subnetwork,compute.googleapis.com/Firewall,storage.googleapis.com/Bucket,cloudfunctions.googleapis.com/CloudFunction"  
      The command contains a parameter already populated and parameters that you need to replace before running the command.  
      * `<FEED_ID>`: Replace this placeholder text with a unique asset feed identifier of your choosing.  
      * `--project`: This parameter is automatically populated from the Project ID field in the Configure Account screen wizard in Cortex XSIAM.  
      * `<Topic name>`—Replace this placeholder text with the topic name you created in the Topic details page in the GCP console.  
   5. In the [GCP Console](https://console.cloud.google.com/home/dashboard), search for Subscription, and select the Subscriptions link.  
   6. CREATE SUBSCRIPTION for the topic you created.  
   7. Set the following parameters.  
      * Subscription ID: Specify a unique identifier for the subscription.  
      * Select a Cloud Pub/Sub topic: Select the topic you created.  
      * Delivery type: Select Pull.  
   8. Click CREATE.  
      The new subscription is listed in the table in the Subscriptions page.  
   9. Select the subscription that you created for your topic and add PERMISSIONS for the subscriber in the Subscription details page.  
   10. ADD PRINCIPAL to add permissions for the Service Account that you created the key for in the JSON file and uploaded to the Configure Account wizard screen in Cortex XSIAM. Set the following permissions for the Service Account.  
       * New principals: Select the designated Service Account Key you created in the JSON file.  
       * Select a role: Select Pub/Sub Subscriber.  
   11. Copy the Subscription name and paste it in the Subscription Name field on the right-side of the Change Asset Logs screen in Cortex XSIAM , and click Next.  
       The Subscription Name is the name of the new Google Cloud Platform data collector that is configured with a Pub/Sub asset feed collection.  
5. Review the Summary screen of the wizard.  
   If something needs to be corrected, you can go Back to correct it.  
6. Click Create.  
   Once cloud assets from GCP start to come in, a green check mark appears underneath the Cloud Inventory configuration with the Last collection time displayed. It can take a few minutes for the Last Collection time to display as the processing completes.  
   Whenever the Cloud Inventory data collector integrations are modified by using the Edit, Disable, or Delete options, it can take up to 10 minutes for these changes to be reflected in Cortex XSIAM.  
   In addition, if you created a Pub/Sub asset feed collection, a green check mark appears underneath the Google Cloud Platform configuration with the amount of data received.  
7. After Cortex XSIAM begins receiving GCP cloud assets, you can view the data in Assets → Cloud Inventory, where All Assets and Specific Cloud Assets pages display the data in a table format. For more information, see Cloud Inventory Assets.

### Ingest Cloud Assets from Microsoft Azure

Abstract

Extend Cortex XSIAM visibility into cloud assets from Microsoft Azure.

Cortex XSIAM provides a unified, normalized asset inventory for cloud assets in Microsoft Azure. This capability provides deeper visibility to all the assets and superior context for incident investigation.

To receive cloud assets from Microsoft Azure, you must configure the Data Sources settings in Cortex XSIAM using the Cloud Inventory data collector to configure the Microsoft Azure wizard. The Microsoft Azure wizard includes instructions to be completed both in Microsoft Azure and the Microsoft Azure wizard screens. After you set up data collection, Cortex XSIAM begins receiving new data from the source.

As soon as Cortex XSIAM begins receiving cloud assets, you can view the data in Assets → Cloud Inventory, where All Assets and Specific Cloud Assets pages display the data in a table format.

To configure the Microsoft Azure cloud assets collection in Cortex XSIAM.

1. Open the Microsoft Azure wizard in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select Cloud Inventory, and click Connect.  
   3. Click Azure.  
2. Define the Configure Account screen of the wizard.  
   Setting the connection parameters on the right-side of the screen are dependent on certain configurations in Microsoft Azure as explained below.  
   1. Select the Organization Level as either Subscription (default), Tenant, or Management Group. The Organization Level that you select changes the instructions and fields displayed on the screen.  
   2. Login to your [Microsoft Azure Portal](https://portal.azure.com/).  
   3. Search for Subscriptions, select Subscriptions, copy the applicable Subscription ID in Azure, and paste it in the Subscription ID field in the Configure Account screen wizard in Cortex XSIAM.  
      This step is only relevant if you’ve configured the Organization Level as Subscription in the Configure Account screen in Cortex XSIAM. Otherwise, you can skip this step if the Organization Level is set to Tenant or Management Group.  
   4. Search for Management groups, select Management groups, copy the applicable ID in Azure, and paste it in the Management Group ID field in the Configure Account screen wizard in Cortex XSIAM.  
      This step is only relevant if you’ve configured the Organization Level as Management Group in the Configure Account screen in Cortex XSIAM. Otherwise, you can skip this step if the Organization Level is set to Subscription or Tenant.  
   5. Search for Tenant properties, select Tenant properties, copy the Tenant ID in Azure, and paste it in the Tenant ID field in the Configure Account screen wizard in Cortex XSIAM.  
   6. Specify a Cortex XDR Collection Name to be displayed underneath the Cloud Inventory configuration for this Azure collection.  
   7. Click Next.  
3. Define the Account Details screen of the wizard.  
   1. Download the Terraform script. The name of the file downloaded is dependent on the Organization Level that you configured in the Configure Account screen of the wizard.  
      1. Subscription: `cortex-xdr-azure-subscription-ro.tf`  
      2. Management Group: `cortex-xdr-azure-group-ro.tf`  
      3. Tenant: `cortex-xdr-azure-org-ro.tf`  
         To run the Terraform script when configuring the Organization Level at the Tenant level, you must first ensure that you elevate user access to manage all Azure subscriptions and management groups for the User Access Administrator role. For more information, see the [Microsoft Azure documentation](https://learn.microsoft.com/en-us/azure/role-based-access-control/elevate-access-global-admin).  
   2. Login to the [Azure Cloud Shell portal](https://portal.azure.com/#cloudshell/), and select Bash.  
   3. Click the upload/download icon (azure-cloud-shell-upload-icon.png) to Upload the Terraform script to Cloud Shell, browse to the file, and click Open.  
      A notification with the Upload destination is displayed on the bottom-right corner of the screen.  
   4. Use the following commands to upload the Terraform script, which you can copy from the Account Details screen in Cortex XSIAM using the copy icon (gcp-copy.png).  
      1. `terraform init`: Initializes the Terraform script. You need to wait until the initialization is complete before running the next command as indicated in the image below.  
         azure-terraform-init-successful.png  
      2. `terraform apply`: When running this command you will be asked to enter the following values, which are dependent on the Organization Level that you configured.  
         Before running this command, ensure that your Azure CLI client is logged in by running `az login`. From the returned message from the login command, copy the code provided, go to the website mentioned in the message, and use the code to authenticate.  
         For more information, see [Sign in with Azure CLI](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli).  
         * `var.subscription_id`: Specify the Subscription ID that you configured in the Configure Account screen of the wizard from Microsoft Azure. This value only needs to be specified if the Subscription ID is set to Subscription.  
         * `var.management.group_id`: Specify the Management Group ID that you configured in the Configure Account screen of the wizard from Microsoft Azure. This value only needs to be specified if the Microsoft Group is set to Management Group.  
         * `var.tenant_id`: Specify the Tenant ID that you configured in the Configure Account screen of the wizard from Microsoft Azure.  
   5. Before the action completes, you need to confirm whether you want to perform these actions, and after the process finishes running an Apply complete indication is displayed.  
      azure-apply-complete.png  
   6. Copy the client\_id value displayed in the Cloud Shell window and paste it in the Application Client ID field in the Account Details screen in Cortex XSIAM.  
   7. Copy the secret value displayed in the Cloud Shell window and paste it in the Secret field in the Account Details screen in Cortex XSIAM.  
   8. Download the JSON file from Cloud Shell using the upload/download icon (azure-cloud-shell-upload-icon.png), so you have output field values for future reference.  
   9. Click Next.  
4. Review the Summary screen of the wizard.  
   If something needs to be corrected, you can go Back to correct it.  
5. Click Create.  
   Once cloud assets from Azure start to come in, a green check mark appears underneath the Cloud Inventory configuration with the Last collection time displayed. It can take a few minutes for the Last Collection time to be displayed.  
   Whenever the Cloud Inventory data collector integrations are modified by using the Edit, Disable, or Delete options, it can take up to 10 minutes for these changes to be reflected in Cortex XSIAM.  
6. After Cortex XSIAM begins receiving Azure cloud assets, you can view the data in Assets → Cloud Inventory, where All Assets and Specific Cloud Assets pages display the data in a table format. For more information, see Cloud Inventory Assets.

## Ingest data from third-party pipeline solutions

Abstract

Ingest data from third-party pipeline solutions into Cortex XSIAM.

Ingest data from third-party pipeline solutions into Cortex XSIAM.

### Ingest data from Cribl

Abstract

Ingest third-party data collected by Cribl.

The Cribl data collector is a beta feature.

The Cribl data collector is an out-of-the-box native integration which ingests data that Cribl collects from multiple data sources and streams to Cortex XSIAM, while ensuring that all downstream capabilities, including analytics, are available in Cortex XSIAM. 

The onboarding process in Cribl has an impact on the output that is sent to Cortex XSIAM. Therefore, the onboarding process of some sources in Cribl might have to be implemented in a certain way in order to adhere to Cortex XSIAM requirements. These processes are described in more detail in Tasks 1 and 3, below.

Raw data must be collected by Cribl and streamed as-is from the passed through source, because any changes made by Cribl might affect the way that Cortex XSIAM handles the data.

For best results, we recommend ingesting data from Palo Alto Networks products, such as Next-Generation Firewall (NGFW) using the dedicated Cortex XSIAM data collectors, instead of source collectors provided by Cribl. Although you can ingest FW data through Cribl, ingesting it that way will omit a layer of data (EAL).

We do not support email data collection via Cribl.

Workflow high-level overview:

1. Task 1: In Cribl, onboard data collection from your data sources.  
2. Task 2: In Cortex XSIAM, create a Cribl data collector instance, and obtain the authorization token and the API URL.  
3. Task 3: In Cribl, for each source, configure the destination, using the Cortex XSIAM authorization token, the Cortex XSIAM API URL, and the source UUID.  
4. Task 4: Verify that data is streamed to Cortex XSIAM as expected, and perform ongoing maintenance.

Perform the following tasks in the order that they appear.

Task 1 (in Cribl, create new data sources)

Ensure that you have the credentials and IDs for each data source, such as Tenant ID, App ID and Client secret.

General guidelines specifically for Cortex XSIAM (for more information, refer to  [Cribl documentation](https://docs.cribl.io/stream/destinations-xsiam/)):

* If you have not already done so, create source collectors to onboard the desired data sources.  
* For some data sources, Cribl includes specific collectors in its catalog. If you can't find one in the catalog specifically for your source, use a generic collector.  
* Although some native Cribl source collectors allow you to ingest several data types using the same source collector, we do not recommend this approach. To ensure optimal Cortex XSIAM performance, configure a separate Cribl source collector for each data type. For reference purposes, [this data source UUID list](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-WSLSYEBc8TgYlqHPJqFAnQ) shows all the data types that can be onboarded.  
  For example, Microsoft 365 has several data types, such as users, groups, and contacts.

Cortex XSIAM

Only one Cribl data collector instance can be configured in Cortex XSIAM.

1. Go to Settings → Configuration → Data Collection → Data Sources.  
2. Search for Cribl.  
3. Click the Cribl integration, and then click Connect.  
4. In the Name field, enter a meaningful name for the integration.  
5. Click Save & generate token.  
6. Click the Copy icon to copy the authorization token.  
7. Save the authorization token copy in a safe place for future use. You cannot access this token again, so take care to copy it and save it before you close the dialog box.  
8. Click Close.  
9. On the Data Sources page, in the row for the Cribl instance, click the link icon (Copy API URL). Save the API URL copy in a safe place for future use.

Cortex XSIAM

Ensure that you have the copies of the Cortex XSIAM authorization token and API URL obtained in Task 2\.

The following table includes guidelines that are relevant specifically for Cortex XSIAM. While you are configuring Cortex XSIAM destinations for your sources, configure the items listed in the table below as described.

For general information about configuring destinations, refer to  [Cribl documentation.](https://docs.cribl.io/stream/destinations-xsiam/)

| Item | Setting | Details |
| ----- | ----- | ----- |
| Cortex XSIAM URL | XSIAM Endpoint field | Paste the API URL obtained from Cortex XSIAM. |
| Authorization token | Authorization Token field | Paste the authorization token obtained from Cortex XSIAM. |
| Advanced Settings | Compress toggle | Ensure that Compress is disabled. |
| HTTP headers | Extra HTTP headers | Add extra HTTP headers for each data source: Source-identifier: Search the table supplied in this topic for the vendor and product.[The Data source UUIDs table](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-WSLSYEBc8TgYlqHPJqFAnQ) lists the data sources that can be identified by Cortex XSIAM, using their corresponding UUIDs. These UUIDs are required to map data collected by Cribl to the Cortex XSIAM destination. If you find the desired vendor and product, copy the corresponding UUID from the table and paste here. This UUID will allow Cortex XSIAM to leverage all the data ingested from the data source, such as identifiers, pipeline sources such as IP addresses, devices, and so on. Data from sources known to Cortex XSIAM are saved in the appropriate datasets–the same datasets as those used by dedicated data collectors in Cortex XSIAM.**Note:** Do not use the generic UUID for a data source that is known to Cortex XSIAM and appears in the table. If you can’t find the desired vendor and product source in the table, copy the generic UUID provided in the first row of the table, and paste here. Data from unknown sources are saved in a separate searchable dataset. The dataset name will reflect the Vendor and Product names that you enter next. Format: json Vendor: When using the UUID for unknown data sources, you must enter the vendor name. Product: When using the UUID for unknown data sources, you must enter the product name. |
| Mapping | Passthru option | Map the data source(s) that you created in Task 1 to the XSIAM data destination created in this task. Ensure that you select the Passthru option. |
| Deployment | Commit & Deploy Deploy | When mapping is complete, click Commit & Deploy, and then click Deploy. |

Cortex XSIAM

Verify that data is streaming as expected from Cribl to Cortex XSIAM.

* In the Cribl user interface, click the Source collector, click Configure, and then the Charts tab. Check the charts to verify that streaming is in progress.  
* In Cortex XSIAM, on the Data Sources page, when streaming begins, a green check mark appears below the Cribl configuration, along with the amount of data received.

Other optional tasks

Use the Disable and Delete options with extreme caution.

* Disabling the integration will cease streaming from Cribl.  
* Deleting the integration will erase the integration completely and will require reconfiguration, because the original authorization token will be lost.

Disable the integration with Cribl

1. To disable the integration, in Cortex XSIAM, search for the Cribl integration on the Data Sources page, and clear the Enable checkbox.  
2. In the Are you sure? dialog box, type `disable`, and then click Disable.

Delete the integration with Cribl

1. To delete the Cribl integration, in Cortex XSIAM, search for the integration on the Data Sources page, and click the integration's Delete icon.  
2. In the Are you sure? dialog box, type `delete`, and then click Delete.

#### Data source UUIDs

Abstract

Data source UUIDs

| Vendor | Product | UUID |
| ----- | ----- | ----- |
|  |  | af01292940d7426594d3d3e55ae17ee0 Do not use this generic UUID when your data source is listed in this table. |
| Salesforce | Salesforce logs | ab109687acd24978aabcb7ad8b5742e3 |
| Salesforce | Salesforce snapshots | addbf31a6372491e88d45934dff5b5b0 |
| Dropbox | Events | a6322b2fd9e545e0a4223ba754c48fb9 |
| Dropbox | Directory | e8d2c52bc9594621924fab0507264586 |
| Workday | Workday | 00d4e740702d4eb2939a87c2318513dd |
| Google | Cloud Logging | 00a8322c85e14beabfa7ad5f3d62db73 |
| Okta | SSO | 5faf4c1fdb8443d9920d6a54815432c1 |
| Microsoft | Azure AD | c00d6d52e5b141a8baa8db9d9345423d |
| PingID | PingONE | 924951a8394b4605b1725f943292ab4f |
| CrowdStrike | Falcon incident | 230b2b0233bf4327806af72e6e5769f3 |
| CrowdStrike | Hosts | 8b673ac8e2f34b4a8dc14c22f0e6063b |
| CrowdStrike | Falcon Data Replicator | 6cd7d60f0ff5497baecf6b9073c8000e |
| SentinelOne | Deep Visibility | b9fa55e6fa564c709358425ce0f61517 |
| Microsoft | Azure | fce13a1d51294f84bae4a37851503060 |
| Microsoft | Defender | ce9e8cf36e0742c38aa89787a256855f |
| ServiceNow | CMDB | 8b3e767247e44471a95e563378d0b9be |
| Prisma | Cloud | f8c3403a02fd4147862ee293bf4e74e2 |
| Prisma | Assets | 6a61c1cba1b64cd2a977c76c41f7950d |
| Proofpoint | TAP | 3eefce0f791e4391a3643b8cf860a361 |
| Microsoft | Office 365 Exchange Online | dee8e85ce7db4573a8bc21b807e1d73a |
| Microsoft | Azure AD audit | 0e076d5abe864bf78e8145ea9e0d749e |
| Microsoft | Azure AD sign-ins | f56dcfdf6bca43e793a4b6e9290e7b12 |
| Microsoft | Graph security alerts | 5619f2f691fc46c4b202587fdaa031c3 |
| Palo Alto Networks | IOT Security devices | 80cee50bfc6e4ac5b34b19794b767acd |
| Palo Alto Networks | IOT Security alerts | e772949c88ec4107ad81ec38061d35c0 |
| Google | Gsuite reports | 3ddd43030db142839568943e0a2fe785 |
| Google | Gmail | 8607490288d1407ba82b5c5ad9dc64a0 |
| Box | Box | 3ef05d14ae9349f8bbd48c8a4797334a |
| OneLogin | Events | 22b23a3f9f1e49998645b683d5dc3a6f |
| OneLogin | OneLogin | 88cfbd3e7b974d999b10edac83995b8a |
| Google | Workspace alerts | 4f263650cd29475c81f2ff953cf19827 |
| Microsoft | Office 365 devices | de229685f708413fad46289657ea09de |
| Microsoft | Office 365 rules | 6b925df8923d4038bf78998d1ffde77c |
| Microsoft | Office 365 users | dcfb7a412e654efd868de0b8cf81766a |
| Microsoft | Office 365 groups | 0b0499ac0d984145b201c6d674771dbf |
| Microsoft | Office 365 contacts | de1b694a6c8341958bc08c4b7c140874 |
| Microsoft | Office 365 domains | cae29fd87b554bd9a5694afb225e8dc9 |
| Microsoft | Office 365 mailboxes | 9855a03559ce4263b568671e695d1fa8 |
| Google | Workspace ChromeOS devices | e82ae276e6b9442fa80920a03d2a38d6 |
| Google | Workspace groups | 689ae8ef14e848e3855b81e91d8af9bc |
| Google | Workspace domains | 2738e963ac3141afaad05885e060a73c |
| Google | Workspace profiles | f2aed57ff13c439eb93153ba7309fe87 |
| Google | Workspace rules | 2621aaf3334a4147ae727afe84db31a9 |
| Google | Workspace organization | 4e342367057d46c7b38ce7d40682fd1e |
| Google | Workspace group members | 8a0140fc47b643838d0fcf096773c0a1 |
| Google | Workspace contacts | d20d6cfea3e943d5a5a6bc005c429ef4 |
| Google | Workspace users | 359ecd845fa54caab6ddb4b7c7a2764d |
| Google | Workspace mailboxes | 328796d692f343c38f07351e8c783f80 |
| Google | Workspace users send as aliases | 3b8f9e65f8ed43f4a4e5679236691fe2 |
| Google | Workspace schemas | c978986a6b3846c7b6fdbe15bef14f69 |
| Google | Workspace mailbox settings | 3c4beffadfac40a18aaf4d143a19dc27 |
| Google | Workspace privileges | 462ebcbfce9341ac8c006e5aa45ccf44 |
| Google | Workspace mobile devices | 149b58ec938d4d1a8568359483e50800 |
| Google | Workspace roles | 82170b42b9684b79bda124c712bcbdc0 |
| Google | Workspace contact groups | 5a42004787064021a462bb2120160514 |
| Google | Workspace apps | 5a617df8827d461db66a10d084c7b39f |
| Amazon | AWS EKS | fb8a9d4922cb4095b76d71e921d2d999 |
| Microsoft | DHCP | b55819e8959c49728d5d98a6d87eafb6 |
| Amazon | AWS flow logs | 667083aa68544eee8b67cdd2d4cc327b |
| Amazon | AWS audit logs | c19f87b6262f48259b3d5d2a2c691802 |
| Amazon | AWS generic logs | 0498f8a24de04b3e85102e742f6783f8 |
| Amazon | AWS Route 53 logs | d57ae82c1e2a4d138fc34084d159b09e |
| Amazon | AWS prompt logs | a53edad7ef0c46ffb5037fb2e21520cb |
| Microsoft | Office 365 Sharepoint Online | 3a37f519e9094a3f8c4185fa572cd111 |
| Microsoft | Office 365 Azure AD | e1f109f886ea42fbb96be6ec0cc597a9 |
| Microsoft | Office 365 DLP | 8f052782739d4b8389644cca23b994ac |
| Microsoft | Office 365 General | c7655e83805b4a058e66043a6715156c |

## Additional log ingestion methods

Abstract

Cortex XSIAM supports custom log ingestion methods.

In addition to native log ingestion support, Cortex XSIAM also supports a number of custom log ingestion methods.

### Ingest logs from Forcepoint DLP

Abstract

Extend Cortex XSIAM visibility into logs from Forcepoint DLP.

If you use Forcepoint DLP to prevent data loss over endpoint channels, you can take advantage of Cortex XSIAM investigation and detection capabilities by forwarding your logs to Cortex XSIAM. This enables Cortex XSIAM to help you expand visibility into data violation by users and hosts in the organization, correlate and detect DLP incidents, and query Forcepoint DLP logs using XQL Search.

As soon as Cortex XSIAM starts to receive logs, Cortex XSIAM can analyze your logs in XQL Search and you can create new Correlation Rules.

To integrate your logs, you first need to set up an applet in a Broker VM within your network to act as a Syslog Collector. You then configure forwarding on your log devices to send logs to the Syslog Collector in a CEF or LEEF format.

Configure Forcepoint DLP collection in Cortex XSIAM.

1. Verify that your Forcepoint DLP meet the following requirements.  
   * Must use version 8.8.0.347 or a later release.  
   * On premise installation only.  
2. Activate the Syslog Collector applet on a Broker VM in your network.  
   Ensure the Broker VM is configured with the following settings.  
   * Format: Select either a CEF or LEF Syslog format.  
   * Vendor: Specify the Vendor as `forcepoint`.  
   * Product: Specify the Product as `dlp_endpoint`.  
3. Increase log storage for Forcepoint DLP logs.  
   As an estimate for initial sizing, note the average Forcepoint DLP log size. For proper sizing calculations, test the log sizes and log rates produced by your Forcepoint DLP. For more information, see Manage Your Log Storage.  
4. Configure the log device that receives Forcepoint DLP logs to forward syslog events to the Syslog Collector in a CEF or LEEF format.  
   For more information, see the [Forcepoint DLP documentation](https://www.websense.com/content/support/library/web/v85/siem/siem.pdf).  
5. After Cortex XSIAM begins receiving data from Forcepoint DLP, you can use XQL Search to search your logs using the `forcepoint_dlp_endpoint` dataset.

### Ingest logs from a Syslog receiver

Abstract

To extend visibility, Cortex XSIAM can receive Syslog from additional vendors that use CEF or LEEF formatted over Syslog (TLS not supported).

Cortex XSIAM can receive Syslog from a variety of supported vendors (see External data ingestion vendor support). In addition, Cortex XSIAM can receive Syslog from additional vendors that use CEF, LEEF, CISCO, CORELIGHT, or RAW formatted over Syslog.

After Cortex XSIAM begins receiving logs from the third-party source, Cortex XSIAM automatically parses the logs in CEF, LEEF, CISCO, CORELIGHT, or RAW format and creates a dataset with the name `<vendor>_<product>_raw`. You can then use XQL Search queries to view logs and create new IOC, BIOC, and Correlation Rules.

To receive Syslog from an external source:

1. Set up your Syslog receiver to forward logs.  
2. Activate the Syslog Collector applet on a Broker VM within your network.  
3. Use the XQL Search to search your logs.

### Ingest Apache Kafka events as datasets

Abstract

Cortex XSIAM can receive logs and data from Apache Kafka directly to your log repository for query and visualization purposes.

Cortex XSIAM can receive events from Apache Kafka clusters directly to your log repository for query and visualization purposes. After you activate the Kafka Collector applet on a Broker VM in your network, which includes defining the connection details and settings related to the list of subscribed topics to monitor and upload to Cortex XSIAM, you can collect events as datasets.

After Cortex XSIAM begins receiving topic events from the Kafka clusters, Cortex XSIAM automatically parses the events and creates a dataset with the specific name you set as the target dataset when you configured the Kafka Collector, and adds the data in these files to the dataset. You can then use XQL Search queries to view events and create new Correlation Rules.

Configure Cortex XSIAM to receive events as datasets from topics in Kafka clusters.

1. Activate the Kafka Collector applet on a Broker VM within your network.  
2. Use the XQL Search to query and review logs.

### Ingest CSV files as datasets

Abstract

Cortex XSIAM can receive CSV log files from a shared Windows directory, where the CSV log files must conform to specific guidelines.

Cortex XSIAM can receive CSV log files from a shared Windows directory directly to your log repository for query and visualization purposes. After you activate the CSV Collector applet on a Broker VM in your network, which includes defining the list of folders mounted to the Broker VM and setting the list of CSV files to monitor and upload to Cortex XSIAM (using a username and password), you can ingest CSV files as datasets.

The ingested CSV log files must conform to the following guidelines:

* Header field names must contain only letters (a-z, A-Z) or numbers (0-9) and must start with a letter. Spaces are converted to underscores (\_).  
* Date values can be in either of the following formats:  
  * YYYY-MM-DD (optionally including HH:MM:SS)  
  * Unix Epoch time. For example, 1614858795\.

After Cortex XSIAM begins receiving logs from the shared Windows directory, Cortex XSIAM automatically parses the logs and creates a dataset with the specific name you set as the target dataset when you configured the CSV Collector. The CSV Collector checks for any changes in the configured CSV files, as well as any new CSV files added to the configuration folders, in the Windows directory every 10 minutes and replaces the data in the dataset with the data from those files. You can then use XQL Search queries to view logs and create new Correlation Rules.

Configure Cortex XSIAM to receive CSV files as datasets from a shared Windows directory.

1. Ensure that you share the applicable CSV files in your Windows directory.  
2. Activate the CSV Collector applet on a Broker VM within your network.  
3. Use the XQL Search to locate and review logs.

### Ingest database data as datasets

Abstract

Cortex XSIAM can receive data from a client relational database directly to your log repository.

Cortex XSIAM can receive data from a client relational database directly to your log repository for query and visualization purposes. After you activate the Database Collector applet on a Broker VM in your network, which includes defining the database connection details and settings related to the query details for collecting the data from the database to monitor and upload to Cortex XSIAM, you can collect data as datasets. For more information about activating this collector applet, see Activate the Database Collector.

After Cortex XSIAM begins receiving data from a client relational database, Cortex XSIAM automatically parses the logs and creates a dataset with the specific name you set as the target dataset when you configured the Database Collector using the format `<Vendor>_<Product>_raw`. The Database Collector checks for any changes in the configured database based on the SQL Query defined in the database connection according to the execution frequency of collection that you configured and appends the data to the dataset. You can then use XQL Search queries to view data and create new Correlation Rules.

Configure Cortex XSIAM to receive data as datasets data from a client relational database.

1. Activate the Database Collector applet on a Broker VM within your network.  
2. Use the XQL Search to query and review logs.

### Ingest logs in a network share as datasets

Abstract

Cortex XSIAM can receive logs from files and folders in a network share directly to your log repository for query and visualization purposes.

Cortex XSIAM can receive logs from files and folders in a network share directly to your log repository for query and visualization purposes. After you activate the Files and Folders Collector applet on a Broker VM in your network, which includes defining the connection details and settings related to the list of files to monitor and upload to Cortex XSIAM, you can collect files as datasets.

After Cortex XSIAM begins receiving logs from files and folders in a network share, Cortex XSIAM automatically parses the logs and creates a dataset with the specific name you set as the target dataset when you configured the Files and Folders Collector using the format `<Vendor>_<Product>_raw`. The Files and Folders Collector reads and processes the configured files one by one, as well as any new files added to the configured files and folders, in the network share according to the execution frequency of collection that you configured and adds the data in these files to the dataset. You can then use XQL Search queries to view logs and create new Correlation Rules.

The Files and Folders Collector applet only starts to collect files that are more than 256 bytes.

Configure Cortex XSIAM to receive logs as datasets from files and folders in a network share.

1. Activate the Files and Folders Collector applet on a Broker VM within your network.  
2. Use the XQL Search to query and review logs.

### Ingest FTP files as datasets

Abstract

Cortex XSIAM can receive logs from files and folders via FTP, FTPS, and SFTP directly to your log repository for query and visualization purposes.

Cortex XSIAM can receive logs from files and folders via FTP, FTPS, or SFTP directly to your log repository for query and visualization purposes. After you activate the FTP Collector applet on a Broker VM in your network, which includes defining the connection details and settings related to the list of files to monitor and upload to Cortex XSIAM, you can collect files as datasets.

After Cortex XSIAM begins receiving logs from files and folders via FTP, FTPS, or SFTP, Cortex XSIAM automatically parses the logs and creates a dataset with the specific name you set as the target dataset when you configured the FTP Collector using the format `<Vendor>_<Product>_raw`. The FTP Collector reads and processes the configured FTP files one by one, as well as any new FTP files added to the configured files and folders, in the FTP directory according to the execution frequency of collection that you configured, and adds the data in these files to the dataset. You can then use XQL Search queries to view logs and create new Correlation Rules.

Configure Cortex XSIAM to receive logs as datasets from files and folders via FTP, FTPS, or SFTP.

1. Activate the FTP Collector applet on a Broker VM within your network.  
2. Use the XQL Search to query and review logs.

### Ingest NetFlow flow records as datasets

Abstract

Cortex XSIAM can receive NetFlow flow records and IPFIX from a UDP port directly to your log repository for query and visualization purposes.

Cortex XSIAM can receive NetFlow flow records and IPFIX from a UDP port directly to your log repository for query and visualization purposes. After you activate the NetFlow Collector applet on a Broker VM in your network, which includes configuring your NetFlow Collector settings, you can ingest NetFlow flow records and IPFIX as datasets.

The ingested NetFlow flow record format must include, at the very least:

* Source and Destination IP addresses  
* TCP/UDP source and destination port numbers

After Cortex XSIAM begins receiving flow records from the UDP port, Cortex XSIAM automatically parses the flow records and creates a dataset with the specific name you set as the target dataset when you configured the NetFlow Collector. The NetFlow Collector adds the flow records to the dataset. You can then use XQL Search queries to view those flow records and create new IOC, BIOC, and Correlation Rules. Cortex XSIAM can also analyze your logs to raise Analytics alerts.

Configure Cortex XSIAM to receive NetFlow flow records as datasets from the routers and switches that support NetFlow.

1. Set up your NetFlow exporter to forward flow records to the IP address of the Broker VM that runs the NetFlow collector applet.  
2. Activate the NetFlow Collector applet on a Broker VM within your network.  
3. Use the XQL Search to query your flow records, using your designated dataset.

### Set up an HTTP Log Collector to Receive Logs

Abstract

You can set up Cortex XSIAM to receive logs from third-party sources, and automatically parse and process these logs.

In addition to logs from supported vendors, you can set up a custom HTTP log collector to receive logs in Raw, JSON, CEF, or LEEF format. The HTTP Log Collector can ingest up to 80,000 events per sec.

After Cortex XSIAM begins receiving logs from the third-party source, Cortex XSIAM automatically parses the logs and creates a dataset with the name `<Vendor>_< Product>_raw`. You can then use XQL Search queries to view logs and create new Correlation rules.

To set up an HTTP log collector to receive logs from an external source.

1. Create an HTTP Log collector in Cortex XSIAM.  
   1. Select Settings → Data Sources.  
   2. On the Data Sources page, click Add Data Source, search for and select HTTP, and click Connect.  
   3. Specify a descriptive Name for your HTTP log collection configuration.  
   4. Select the data object Compression, either gzip or uncompressed.  
   5. Select the Log Format as Raw, JSON, CEF, or LEEF.  
      Cortex XSIAM supports logs in single line format or multiline format. For a JSON format, multiline logs are collected automatically when the Log Format is configured as JSON. When configuring a Raw format, you must also define the Multiline Parsing Regex as explained below.  
      \-The Vendor and Product defaults to Auto-Detect when the Log Format is set to CEF or LEEF.  
      \-For a Log Format set to CEF or LEEF, Cortex XSIAM reads events row by row to look for the Vendor and Product configured in the logs. When the values are populated in the event log row, Cortex XSIAM uses these values even if you specified a value in the Vendor and Product fields in the HTTP collector settings. However, when the values are blank in the event log row, Cortex XSIAM uses the Vendor and Product that you specified in the HTTP collector settings. If you did not specify a Vendor or Product in the HTTP collector settings, and the values are blank in the event log row, the values for both fields are set to unknown.  
   6. Specify the Vendor and Product for the type of logs you are ingesting.  
   7. (Optional) Specify the Multiline Parsing Regex for logs with multilines.  
      This option is only displayed when the Log Format is set to Raw, so you can set the regular expression that identifies when the multiline event starts in logs with multilines. It is assumed that when a new event begins, the previous one has ended.  
   8. Save & Generate Token.  
      Click the copy icon next to the key and record it somewhere safe. You will need to provide this key when you configure your HTTP POST request and define the api\_key. If you forget to record the key and close the window you will need to generate a new key and repeat this process.  
      Click Done when finished.  
2. Send data to your Cortex XSIAM HTTP log collector.

Send an HTTP POST request to the URL for your HTTP Log Collector.  
You can view a sample curl or python request on an HTTP collector instance by selecting table-settings.pngView Example.  
Here is a CURL example:  
curl \-X POST https://api-{tenant external URL}/logs/v1/event \-H 'Authorization: {api\_key}' \-H 'Content-Type: text/plain' \-d '{"example1": "test", "timestamp": 1609100113039}  
{"example2": \[12321,546456,45687,1\]}'  
Python 3 example:  
import requests  
def test\_http\_collector(api\_key):  
    headers \= {  
        "Authorization": api\_key,  
        "Content-Type": "text/plain"  
    }  
    \# Note: the logs must be separated by a new line  
    body \= "{'example1': 'test', 'timestamp': 1609100113039}" \\  
           "{'example2': \[12321,546456,45687,1\]}"  
    res \= requests.post(url="https://api-{tenant external URL}/logs/v1/event",  
                        headers=headers,  
                        data=body)

1.     return res  
   2. Substitute the values specific to your configuration.  
      * `url`: You can copy the URL for your HTTP log collector from the Custom Collectors page. For example: `https://api-{tenant external URL}/logs/v1/event`.  
      * `Authorization`: Paste the `api_key` you previously recorded for your HTTP log collector, which is defined in the header.  
      * `Content-Type`: Depending on the data object format you selected during setup, this will be `application/json` for JSON format or `text/plain` for Text format. This is defined as part of the header.  
      * `Body`: The body contains the records you want to send to Cortex XSIAM. Separate records with a `\n` (new line) delimiter. The request body can contain up to 10 Mib records, but 1 Mib is recommended. In the case of a curl command, the records are contained in the `-d ‘<records>’` parameter.  
        Each record cannot exceed 5 MB in size.  
   3. Review the possible success and failure code responses to your HTTP Post requests.  
      The following table provides the various success and failure code responses to your HTTP Post requests, which can help you troubleshoot any problems with your HTTP Collector configuration.

| Success/failure response code | Description | Output code displayed (if applicable) |
| :---- | :---- | :---- |
| 200 | Success code that indicates there are no errors and the request was successful. | {    "error": "false"} |
| 401 | Unauthorized error code that indicates either an incorrect authorization token is being used or that the HTTP Collector is deleted/disabled. |  |
| 404 | Error code 404 page not found that indicates a wrong URL. |  |
| 413 | Error code indicating the payload is too large as the request size limit is 10 MB. |  |
| 500 | Error code indicating the request was not able to be processed due to an incorrect log format between the request and the HTTP collector configuration. | {    "error": "error processing request, error: failed to process the request"} |
| 429 | Error code indicating too many requests as the rate limit is 400 requests per second per customer per endpoint. |  |

3.   
   Monitor your HTTP Log Collection integration.  
   You can return to the Settings → Data Sources page to monitor the status of your HTTP Log Collection configuration. For each instance, Cortex XSIAM displays the number of logs received in the last hour, day, and week. You can also use the Data Ingestion Dashboard to view general statistics about your data ingestion configurations.  
4. After Cortex XSIAM begins receiving logs, use the XQL Search to search your logs.

### Ingest logs from BeyondTrust Privilege Management Cloud

Abstract

Extend Cortex XSIAM visibility into logs from BeyondTrust Privilege Management Cloud.

If you use BeyondTrust Privilege Management Cloud, you can take advantage of Cortex XSIAM investigation and detection capabilities by forwarding your logs to Cortex XSIAM. This enables Cortex XSIAM to help you expand visibility into computer, activity, and authorization requests in the organization, correlate and detect access violations, and query BeyondTrust Endpoint Privilege Management logs using XQL Search.

As soon as Cortex XSIAM starts to receive logs, Cortex XSIAM can analyze your logs in XQL Search and you can create new Correlation Rules.

To integrate your logs, you first need to configure SIEM settings and an AWS S3 Bucket according to the specific requirements provided by BeyondTrust. You can then configure data collection in Cortex XSIAM by configuring an Amazon S3 data collector for a generic log type using the Beyondtrust Cloud ECS log format.

Before you begin configuring data collection verify that you are using BeyondTrust Privilege Management Cloud version 21.6.339 or later.

Configure BeyondTrust Privilege Management Cloud collection in Cortex XSIAM.

1. Configure SIEM settings and an AWS S3 Bucket according to the requirements provided in the [BeyondTrust documentation](https://www.beyondtrust.com/docs/privilege-management/console/pm-cloud/configuration/configure-siem-settings.htm).  
   Ensure that when you add the AWS S3 bucket in the PMC and set the SIEM settings, you select ECS \- Elastic Common Schema as the SIEM Format.  
2. Configure BeyondTrust logs collection with Cortex XSIAM using an [Amazon S3 data collector for generic data](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#topic-7GfGi4BtWsa7fe23UhBbMQ).  
   Ensure your Amazon S3 data collector is configured with the following settings.  
   * Log Type: Select Generic to configure your log collection to receive generic logs from Amazon S3.  
   * Log Format: Select the log format type as Beyondtrust Cloud ECS.  
     For a Log Format set to Beyondtrust Cloud ECS, the following fields are automatically set and not configurable.  
     * Vendor: Beyondtrust  
     * Product: Privilege Management  
     * Compression: Uncompressed  
3. After Cortex XSIAM begins receiving data from BeyondTrust Privilege Management Cloud, you can use XQL Search to search your logs using the `beyondtrust_privilege_management_raw` dataset that you configured when setting up your Amazon S3 data collector.

### Ingest Logs and Data from Box

Abstract

Ingest logs and data from Box enterprise accounts via the Box REST APIs.

Cortex XSIAM can ingest different types of data from Box enterprise accounts using the Box data collector. To receive logs and data from Box enterprise accounts via the Box REST APIs, you must configure the Data Sources settings in Cortex XSIAM based on your Box enterprise account credentials. After you set up data collection, Cortex XSIAM begins receiving new logs and data from the source.

When Cortex XSIAM begins receiving logs, the app creates a new dataset for the different types of data that you are collecting, which you can use to initiate XQL Search queries. For example queries, refer to the in-app XQL Library. For all logs, Cortex XSIAM can raise Cortex XSIAM alerts (Analytics, Correlation Rules, IOC, and BIOC), when relevant from Box logs. While Correlation Rules alerts are raised on non-normalized and normalized logs, Analytics, IOC, and BIOC alerts are only raised on normalized logs.

The following table provides a brief description of the different types of data you can collect, the collection method and fetch interval for new data collected, the name of the dataset to use in Cortex XSIAM to query the data using XQL Search, and whether the data is normalized.

The Fetch Intervals are non-configurable.

| Type of data | Description | Collection method | Fetch interval | Dataset name | Normalized data |
| ----- | ----- | ----- | ----- | ----- | ----- |
| **Events and security alerts** |  |  |  |  |  |
| Events (admin\_logs) | Retrieves events related to file/folder management, permission changes, access and login activities, user/groups management, folder collaboration, file/folder sharing, security settings changes, tasks, permission changes on folders, storage expiration and data retention, and workflows. | Appends data | 60 seconds | `box_admin_logs_raw` | When relevant, Cortex XSIAM normalizes SaaS audit event logs into stories, which are collected in a dataset called `saas_audit_logs`. |
| Box Shield Alerts | Retrieves security alerts related to suspicious locations, suspicious sessions, anomalous download, and malicious content. Collecting Box Shield Alerts requires implementing [Box Shield](https://www.box.com/shield), | Appends data | 60 seconds | `box_shield_alerts_raw` | — |
| **Directory and metadata** |  |  |  |  |  |
| Users | Lists user data. | Overwrites data | 10 minutes | `box_users_raw` | — |
| Groups | Lists user group data. | Overwrites data | 10 minutes | `box_groups_raw` | — |

1.   
   Set up an [Enterprise](https://www.box.com/pricing) Box plan.  
   To collect Box Shield Alerts, you must purchase [Box Shield](https://www.box.com/shield) and it must be enabled on Box enterprise.  
2. Create a valid Box account that is assigned to a role with sufficient permissions for the data you want to collect. For example, create an account assigned to an Admin role to enable Cortex XSIAM to collect all metadata for all files, folders, and enterprise events for the entire organization.  
3. Enable two-factor authentication for the Box account. For more information, see the [Box documentation](https://support.box.com/hc/en-us/articles/360043697154-Two-Factor-Authentication-Set-Up-for-Your-Account).

Configure Cortex XSIAM to receive logs and data from Box.

1. Complete the prerequisites mentioned above for your Box enterprise account.  
2. Create a new app in your Box account.  
   * Log in to your Box account, and in the [Dev Console](https://account.box.com/login?redirect_url=%2Fdevelopers%2Fconsole), click Create New App.  
   * Select Custom App.  
   * Set these settings in the Custom App dialog:  
     * Select Server Authentication (Client Credentials Grant).  
     * Specify an App Name.  
     * Click Create App.  
   * The new app is created and the opened in the Configuration tab.  
   * In the Configuration tab of the new app, scroll down to the following sections and configure the app.  
     * In the App Access Level section, select App \+ Enterprise Access.  
     * In the Application Scopes section, set the following Administrative Action permissions depending on the type of data you want to collect.

| Administrative action | Data type |
| :---- | :---- |
| Manage users | Users |
| Manage groups | Groups There is a current bug with the Groups API from Box. If you don't configure the Box app with the proper permissions for managing groups data, the Groups API from Box won't return an error message to Cortex XSIAM indicating that the API failed to receive the data, and the Groups data will not be collected. |
| Manage enterprise properties | Events (admin\_logs) Box Shield Alerts |

   *   
     Once completed, scroll up in the tab to Save Changes.  
   * In the Authorization tab, click Review and Submit to send your changes to the administrator for approval.  
     In the Review App Authorization Submission dialog that is displayed, you can add a Description of the app changes, and then click Submit.  
3. Ensure the new app changes are approved by an administrator in the Admin Console of the Box account.  
   * Select Apps → Customer Apps Manager → Server Authentication Apps.  
   * In the table, look for the Name of the Box app with the changes, where the Authorization Status is set to Pending Authorization, and select the options menu → Authorize App.  
   * Click Authorize.  
4. For any future change that you make to your Box app, ensure that you send the changes for approval to the administrator, who will need to approve them as explained above.  
5. In Cortex XSIAM, select Settings → Data Sources.  
6. On the Data Sources page, click Add Data Source, search for and select Box, and click Connect.  
7. Set the following parameters, where some values require you to log in to your Box account to copy and paste the values to the applicable fields:  
   * Name: Specify a descriptive name for this Box instance.  
   * Enterprise ID: Specify the unique identifier for your organization's Box instance, which is used to access the token request. This field can't be edited once the Box data collector instance is created.  
     You can retrieve this value from your Box account in the the General Settings tab, and scrolling to the App Info section. Copy the Enterprise ID and paste it in this field in Cortex XSIAM.  
   * Client ID: Specify the client ID or API key for the Box app you created.  
     You can retrieve this value from your Box account in the Configuration tab, and scrolling down to the OAuth 2.0 Credentials section. COPY the Client ID and paste it into this field in Cortex XSIAM.  
   * Client Secret: The client secret or API secret fort he Box app you created.  
     You can retrieve this value from your Box account in the Configuration tab, and scrolling down to the OAuth 2.0 Credentials section. Click Fetch Client Secret, where you will need to authenticate yourself according to the [two-factor authentication method](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#UUID-159d4615-51ac-efc5-5783-d836746388f4_listitem-idm53336178838098) defined in your Box app before the Client Secret is displayed. Copy this value and paste it in this field in Cortex XSIAM.  
   * Collect: Select the types of data you want to collect from Box. All the options are selected by default.  
     * Events and security alerts  
       * Events (admin\_logs): Collects events related to file/folder management, permission changes, access and login activities, user/groups management, folder collaboration, file/folder sharing, security settings changes, tasks, permission changes on folders, storage expiration and data retention, and workflows.  
       * Box Shield Alerts: Collects security alerts related to suspicious locations, suspicious sessions, anomalous download, and malicious content.  
     * Directory and metadata  
       Inventory data snapshots are collected every 10 minutes.  
       * Users: Collects user data.  
       * Groups: Collects user group data.  
8. Test the connection settings.  
9. If successful, Enable Box log collection.  
   Once events start to come in, a green check mark appears underneath the Box configuration.

### Ingest Logs and Data from Dropbox

Abstract

Ingest logs and data from Dropbox Business accounts via the Dropbox Business API.

Cortex XSIAM can ingest different types of data from Dropbox Business accounts using the Dropbox data collector. To receive logs and data from Dropbox Business accounts via the Dropbox Business API, you must configure the Data Sources settings in Cortex XSIAM based on your Dropbox Business Account credentials. After you set up data collection, Cortex XSIAM begins receiving new logs and data from the source.

When Cortex XSIAM begins receiving logs, the app creates a new dataset for the different types of data that you are collecting, which you can use to initiate XQL Search queries. For example queries, refer to the in-app XQL Library. For all logs, Cortex XSIAM can raise Cortex XSIAM alerts (Analytics, Correlation Rules, IOC, and BIOC), when relevant from Dropbox Business logs. While Correlation Rules alerts are raised on non-normalized and normalized logs, Analytics, IOC, and BIOC alerts are only raised on normalized logs.

The following table provides a brief description of the different types of data you can collect, the collection method and fetch interval for new data collected, the name of the dataset to use in Cortex XSIAM to query the data using XQL Search, and whether the data is normalized.

The Fetch Interval is non-configurable.

| Type of data | Description | Collection method | Fetch interval | Dataset name | Normalized data |
| ----- | ----- | ----- | ----- | ----- | ----- |
| **Log collection** |  |  |  |  |  |
| Events | Retrieves team events, including access events, administrative events, file/folders events, security settings events, and more. [team\_log/get\_events](https://www.dropbox.com/developers/documentation/http/teams#team_log-get_events) | Appends data | 60 seconds | `dropbox_events_raw` | When relevant, Cortex XSIAM normalizes SaaS audit event logs into stories, which are collected in a dataset called `saas_audit_logs`. |
| **Directory and metadata** |  |  |  |  |  |
| Member Devices | Lists all device sessions of a team. [team/devices/list\_members\_devices](https://www.dropbox.com/developers/documentation/http/teams#team-devices-list_members_devices) | Overwrites data | 10 minutes | `dropbox_members_devices_raw` | — |
| Users | Lists members of a group. [team/members/list\_v2](https://www.dropbox.com/developers/documentation/http/teams#team-members-list) | Overwrites data | 10 minutes | `dropbox_users_raw` | — |
| Groups | Lists groups on a team. [team/groups/list](https://www.dropbox.com/developers/documentation/http/teams#team-groups-list) | Overwrites data | 10 minutes | `dropbox_groups_raw` | — |

1.   
   Set up an [Advanced](https://www.dropbox.com/plans) Dropbox plan.  
2. Create a Dropbox Business [admin account](https://help.dropbox.com/account-access) with Security admin permissions, which is required to authorize Cortex XSIAM to access the Dropbox Business account and generate the OAuth 2.0 access token.

Configure Cortex XSIAM to receive logs and data from Dropbox.

1. Complete the prerequisite steps mentioned above for your Dropbox Business account.  
2. Log in to Dropbox using an admin account designated with Security admin level permissions.  
3. In the Dropbox App console, ensure that you either create a new app, or your existing app is created, with the following settings:  
   * Choose an API: Select Scoped access.  
   * Choose the type of access you need: Select Full dropbox for access to all files and folders in a user's Dropbox.  
4. In the Permissions tab of your app, ensure that the applicable permissions are selected under the relevant section heading for the type of data you want to collect:

| Section heading | Permission | Data to collect |
| :---- | :---- | :---- |
| Account Info | account\_info.read | All types of data |
| Team Data | team\_data.member | All types of data |
| Members | members.read | Users |
|  | groups.read | Groups |
| Sessions | sessions.list | Member Devices |
|  | events.read | Events |

5.   
   In the Settings tab of your app, copy the App key and App secret , where you must click Show to see the App secret and record them somewhere safe. You will need to provide these keys when you configure the Dropbox data collector in Cortex XSIAM.  
6. In Cortex XSIAM, select Settings → Data Sources.  
7. On the Data Sources page, click Add Data Source, search for and select Dropbox and click Connect.  
8. Set the following parameters:  
   * Name: Specify a descriptive name for this Dropbox instance.  
   * App Key: Specify the App key, which is taken from the [Settings tab](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#UUID-6f7b5768-7f59-a1c0-2844-2d7042a73a15_N1667467209646) of your Dropbox app.  
   * App Secret: Specify the App secret, which is taken from the [Settings tab](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#UUID-6f7b5768-7f59-a1c0-2844-2d7042a73a15_N1667467209646) of your Dropbox app.  
   * Access Code: After specifying an App Key, you can obtain the access code by hovering over the Access Code tooltip, clicking the here link, and signing in with your Dropbox Business account credentials. The URL link is `https://www.dropbox.com/oauth2/authorize?client_id=%APP_KEY%&amp;token_access_type=offline&amp;response_type=code`, where the `%APP_KEY%` is replaced with the App Key value specified.  
     When the App Key field is empty, the here link in the tooltip is disabled. When an incorrect App Key is entered, clicking the link results in a 404 error.  
     To obtain the Access Code complete the following steps in the page that opens in your browser:  
     * Read the disclaimer and click Continue.  
     * Review the permissions listed, which should match the permissions you configured in your Dropbox app in the [Permissions tab](https://docs-cortex.paloaltonetworks.com/internal/api/webapp/print/cb076985-8d07-4d5c-adf1-069a5fb562c4#UUID-6f7b5768-7f59-a1c0-2844-2d7042a73a15_N1667490419389) according to the type of data you want to collect, and click Allow.  
     * Copy the Access Code Generated and paste it in the Access Code field in Cortex XSIAM. The access code is valid for around four minutes from when it is generated.  
   * Whenever you change the permissions of the Dropbox app, we recommend that you generate a new Access Code for the Dropbox data collector instance so that the permissions match the updates.  
   * Collect: Select the types of data you want to collect from Dropbox. All the options are selected by default.  
     * Log collection  
       * Events (get\_events}: Retrieves team events, including access events, administrative events, file/folders events, security settings events and more.  
     * Event data is collected every 60 seconds with a 10 minute lag time.  
     * Directory and metadata  
       * Member Devices: Collects all device sessions of a team.  
       * Users: Collects all members of a group.  
       * Groups: Collects all groups on a team.  
     * Inventory data snapshots are collected every 10 minutes.  
9. Test the connection settings.  
10. If successful, Enable Dropbox log collection.  
    Once events start to come in, a green check mark appears underneath the Dropbox configuration.

### Ingest Logs from Elasticsearch Filebeat

Abstract

Cortex XSIAM can ingest logs from Elasticsearch Filebeat, a file system logger that logs file activity on your endpoints and servers.

If you want to ingest logs about file activity on your endpoints and servers and do not use the Cortex XDR agent, you can install Elasticsearch Filebeat as a system logger and then forward those logs to Cortex XSIAM. To facilitate log ingestion, Cortex XSIAM supports the same protocols that Filebeat and Elasticsearch use to communicate. Cortex XSIAM supports using Filebeat up to version 8.2 with the Filebeat data collector. Cortex XSIAM also supports logs in single line format or multiline format. For more information on handling messages that span multiple lines of text in Elasticsearch Filebeat, see [Manage Multiline Messages](https://www.elastic.co/guide/en/beats/filebeat/current/multiline-examples.html).

Cortex XSIAM supports all sections in the `filebeat.yml` configuration file, such as support for Filebeat fields and tags. As a result, this enables you to use the [add\_fields](https://www.elastic.co/guide/en/beats/filebeat/current/add-fields.html) processor to identify the product/vendor for the data collected by Filebeat so the collected events go through the ingestion flow (Parsing Rules). To configure the product/vendor ensure that you use the default `fields` attribute, as opposed to the `target` attribute, as shown in the following example.

processors:  
  \- add\_fields:  
      fields:  
        vendor: \<Vendor\>  
        product: \<Product\>

To provide additional context during investigations, Cortex XSIAM automatically creates a new Cortex Query Language (XQL) dataset from your Filebeat logs. You can then use the XQL dataset to search across the logs Cortex XSIAM received from Filebeat.

To receive logs, you configure collection settings for Filebeat in Cortex XSIAM and output settings in your Filebeat installations. As soon as Cortex XSIAM begins receiving logs, the data is visible in XQL Search queries.

1. In Cortex XSIAM, set up Data Collection.  
   * Select Settings → Data Sources.  
   * On the Data Sources page, click Add Data Source, search for and select Filebeat, and click Connect.  
   * Specify a descriptive Name for your Filebeat log collection configuration.  
   * Specify the Vendor and Product for the type of logs you are ingesting.  
     The vendor and product are used to define the name of your XQL dataset (`<vendor>_<product>_raw`). If you do not define a vendor or product, Cortex XSIAM examines the log header to identify the type and uses that to define the vendor and product in the dataset. For example, if the type is Acme and you opt to let Cortex XSIAM determine the values, the dataset name would be `acme_acme_raw`.  
   * Save & Generate Token.  
     Click the copy icon next to the key and record it somewhere safe. You will need to provide this key when you set up output settings on your Filebeat instance. If you forget to record the key and close the window you will need to generate a new key and repeat this process.  
2. Set up Filebeat to forward logs.  
   After installing the Filebeat agent, configure an Elasticsearch output:  
   * Under the output.elasticsearch section, configure the following entities:  
     filebeat-setup.png  
     * `hosts`: Copy the API URL from your Filebeat configuration and paste it in this field.  
     * `compression_level`: 5 (recommended)  
     * `bulk_max_size`: 1000 (recommended)  
     * `api_key`: Paste the key you created in when you configured Filebeat Log Collection in Cortex XSIAM.  
     * `proxy_url`: (Optional) `<server_ip>:<port_number>`. You can specify your own `<server_ip>` or use the Broker VM to proxy Filebeat communication using the format `<Broker_VM_ip>:<port_number>`. When using the Broker VM, ensure that you activate the Local Agent Settings applet with the Agent Proxy enabled.  
   * Save the changes to your output file.  
3. After Cortex XSIAM begins receiving logs from Filebeat, they will be available in XQL Search queries.  
4. (Optional) Monitor your Filebeat integration.  
   You can return to the Settings → Configurations → Data Collection → Data Sources page to monitor the status of your Filebeat configuration. For each instance, Cortex XSIAM displays the number of logs received in the last hour, day, and week. You can also use the Data Ingestion Dashboard to view general statistics about your data ingestion configurations.  
5. (Optional) Set up alert notifications to monitor the following events.  
   * A Filebeat agent status changes to disconnected.  
   * A Filebeat module has stopped sending logs.

### Ingest logs from Forcepoint DLP

Abstract

Extend Cortex XSIAM visibility into logs from Forcepoint DLP.

If you use Forcepoint DLP to prevent data loss over endpoint channels, you can take advantage of Cortex XSIAM investigation and detection capabilities by forwarding your logs to Cortex XSIAM. This enables Cortex XSIAM to help you expand visibility into data violation by users and hosts in the organization, correlate and detect DLP incidents, and query Forcepoint DLP logs using XQL Search.

As soon as Cortex XSIAM starts to receive logs, Cortex XSIAM can analyze your logs in XQL Search and you can create new Correlation Rules.

To integrate your logs, you first need to set up an applet in a Broker VM within your network to act as a Syslog Collector. You then configure forwarding on your log devices to send logs to the Syslog Collector in a CEF or LEEF format.

Configure Forcepoint DLP collection in Cortex XSIAM.

1. Verify that your Forcepoint DLP meet the following requirements.  
   * Must use version 8.8.0.347 or a later release.  
   * On premise installation only.  
2. Activate the Syslog Collector applet on a Broker VM in your network.  
   Ensure the Broker VM is configured with the following settings.  
   * Format: Select either a CEF or LEF Syslog format.  
   * Vendor: Specify the Vendor as `forcepoint`.  
   * Product: Specify the Product as `dlp_endpoint`.  
3. Increase log storage for Forcepoint DLP logs.  
   As an estimate for initial sizing, note the average Forcepoint DLP log size. For proper sizing calculations, test the log sizes and log rates produced by your Forcepoint DLP. For more information, see Manage Your Log Storage.  
4. Configure the log device that receives Forcepoint DLP logs to forward syslog events to the Syslog Collector in a CEF or LEEF format.  
   For more information, see the [Forcepoint DLP documentation](https://www.websense.com/content/support/library/web/v85/siem/siem.pdf).  
5. After Cortex XSIAM begins receiving data from Forcepoint DLP, you can use XQL Search to search your logs using the `forcepoint_dlp_endpoint` dataset.

### Ingest Logs from Proofpoint Targeted Attack Protection

Abstract

Ingest logs from Proofpoint Targeted Attack Protection (TAP).

To receive logs from Proofpoint Targeted Attack Protection (TAP), you must first configure TAP service credentials in the TAP dashboard, and then the Collection Integrations settings in Cortex XSIAM based on your Proofpoint TAP configuration. After you set up data collection, Cortex XSIAM begins receiving new logs and data from the source.

When Cortex XSIAM begins receiving logs, the app creates a new dataset (`proofpoint_tap_raw`) that you can use to initiate XQL Search queries. For example queries, refer to the in-app XQL Library.

Configure the Proofpoint TAP collection in Cortex XSIAM.

1. Generate TAP Service Credentials in Proofpoint TAP.  
   TAP service credentials can be generated in the TAP Dashboard, where you will receive a Proofpoint Service Principal for authentication and Proofpoint API Secret for authentication. Record these credentials as you will need to provide them when configuring the Proofpoint Targeted Attack Protection data collector in Cortex XSIAM. For more information on generating TAP service credentials, see [Generate TAP Service Credentials](https://ptr-docs.proofpoint.com/ptr-guides/integrations-files/ptr-tap/).  
2. Configure the Proofpoint TAP collection in Cortex XSIAM.  
   * Select Settings → Data Sources.  
   * On the Data Sources page, click Add Data Source, search for and select Proofpoint Targeted Attack Protection, and click Connect.  
   * Set these parameters:  
     * Name: Specify a descriptive name for your log collection configuration.  
     * Proofpoint Endpoint: All Proofpoint endpoints are available on the `tap-api-v2.proofpoint.com` host. You can leave the default configuration or specify another host.  
     * Service Principal: Specify the Proofpoint Service Principal for authentication. TAP service credentials can be generated in the TAP Dashboard.  
     * API Secret: Specify the Proofpoint API Secret for authentication. TAP service credentials can be generated in the TAP Dashboard.  
   * Click Test to validate access, and then click Enable.  
     Once events start to come in, a green check mark appears underneath the Proofpoint Targeted Attack Protection configuration with the amount of data received.  
3. (Optional) Manage your Proofpoint Targeted Attack Protection data collector.  
   After you enable the Proofpoint Targeted Attack Protection data collector, you can make additional changes as needed.  
   You can perform any of the following:  
   * Edit the Proofpoint Targeted Attack Protection data collector settings.  
   * Disable the Proofpoint Targeted Attack Protection data collector.  
   * Delete the Proofpoint Targeted Attack Protection data collector.

### Ingest logs and data from Salesforce.com

Abstract

Use the Cortex XSIAM data collector to collect Audit Trail and Security Monitoring event logs from Salesforce.com.

The Cortex XSIAM data collector can collect Audit Trail and Security Monitoring event logs from Salesforce.com. During setup of this data collector, you can choose to accept the default collection settings, or exclude the collection of content metadata and accounts.

The Salesforce.com data collector fetches events, and objects and metadata, including:

* Login history  
* Setup audit trail  
* Flow Execution events  
* Transaction Security events  
* Content Distribution events  
* Package Install events

You can create multiple Salesforce.com data collector instances in Cortex XSIAM, for different parts of your organization.

Logs are collected from Salesforce.com every 30 seconds. When Cortex XSIAM begins receiving logs, it creates new datasets for them, called `salesforce_<object>_raw`.  Examples of `<object>` include:

* connectedapplication  
* permissionset  
* profile  
* groupmember  
* group  
* user  
* userrole  
* document  
* contentfolder  
* attachment  
* contentdistribution  
* tenantsecuritylogin  
* useraccountteammember  
* tenantsecurityuserperm  
* account  
* audit  
* login  
* eventlogfile

You can use these datasets to perform XQL search queries. For example queries, refer to the in-app XQL Library.

To manage collection integration in Cortex XSIAM, ensure that you have the privilege to View/Edit Log Collections (for example, Instance Administrator).

To avoid errors, the minimum required  Salesforce.com editions are Professional Edition with API access enabled, or Enterprise Edition, or higher.

To use the client credentials flow required for Salesforce.com–Cortex XSIAM integration, you must create a connected app for Cortex XSIAM in Salesforce.com, and configure its OAuth settings and access policies. Following these activities, configure Cortex XSIAM.

For more detailed reference information, see [Configure a Connected App for the OAuth 2.0 Client Credentials Flow](https://help.salesforce.com/s/articleView?id=sf.connected_app_client_credentials_setup.htm&type=5).

Unlike other data collector setups, in this case, the setup includes obtaining an OAuth 2.0 code from Salesforce.com, and this code is only valid for 15 minutes. Therefore, make sure that you enable the data collector within 15 minutes of obtaining the authorization code.

Perform the following procedures in the order that they appear, below.

###### Task 1\. Configure Salesforce Connected App

1. On the Setup page, in Quick Find, type `App Manager`.  
2. Click New Connected App.  
3. Enter a meaningful name for the connected application and for the API. For example, you could name it panw\_cortex\_integration.  
4. Enter your email address. This address will be used to retrieve the Consumer Key and Consumer Secret.  
5. Select the Enable OAuth Settings checkbox.  
6. In Callback URL, type  
   `https://login.salesforce.com/services/oauth2/callback`  
   and  
   `https://{tenant external URL}.paloaltonetworks.com/configuration/data-sources`  
   on separate lines, where `{tenant external URL}` is the name of your tenant as it appears in the URL of your Cortex XSIAM tenant.  
7. For OAuth Scopes, select Full access (full) and Perform requests at any time (refresh\_token, offline\_access).  
8. In the next options after OAuth Scopes, ensure that only the following checkboxes are selected:  
   * Require Secret for Web Server Flow  
   * Require Secret for Refresh Token Flow  
   * Enable Credentials Flow  
9. Click Save, and then Continue.

###### Task 2\. Retrieve the Consumer Key and Consumer Secret

Consumer Key will be used for client\_id, and Consumer Secret will be used for client\_secret in OAuth 2.0.

1. On the Setup page, in Quick Find, type `App Manager`.  
2. Find your connected application (the one that you defined for Cortex XSIAM). In the last column, click the arrow button and then click View.  
3. In the API (Enable OAuth Settings) area, click Manage Consumer Details.  
4. When you are asked to verify your identity, open the email that Salesforce sent to you, and copy the verification code. Go back to the Salesforce Verify Your Identity page, paste the code in the Verification Code box, and click Verify. One of the following will happen:  
   * The Consumer Key and Consumer Secret will be sent to the email address that you configured earlier for the Cortex XSIAM connected app.  
   * On the Salesforce Connected App Name page, the Consumer Details area will display the Consumer Key and Consumer Secret, and you will be able to copy them from here when required in the following procedures.

###### Task 3\. Configure the Refresh Token expiration policy

1. On the Setup page, in Quick Find, type `App Manager`.  
2. Find your connected application (the one that you defined for Cortex XSIAM). In the last column, click the arrow button and then click Manage.  
3. Click Edit Policies.  
4. In the OAuth Policies area:  
   * Under Permitted Users, select All users may self-authorize.  
   * Choose your refresh token policy. We recommend: Expire refresh token if not used for \_ Day(s). For example, select this option and set it for 7 days.

###### Task 4\. Configure OAuth 2.0

* Configure the OAuth 2.0 application to call the Salesforce.com API using client\_id and client\_secret.  
  References: [https://help.salesforce.com/s/articleView?id=sf.remoteaccess\_oauth\_client\_credentials\_flow](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_client_credentials_flow)

###### Task 5\. Configure Cortex XSIAM

1. In Cortex XSIAM, create a Salesforce.com data collector instance:  
   * Select Settings → Data Sources.  
   * On the Data Sources page, click Add Data Source, search for and select Salesforce.com, and click Connect.  
2. Enter a unique Name for the instance, enter the Salesforce Domain Name, and the Consumer Key and the Consumer Secret credentials obtained earlier in this workflow. For example, the domain could be the API URL from which logs are received, such as `https://MyDomainName.my.salesforce.com/services/data/vXX.X/resource/`  
3. (Optional) Clear options that you do not require:  
   * Content metadata: when selected (default), collects documents’ metadata.   
   * Accounts: when selected (default), collects account objects.  
4. When these options are cleared, only these data types will be omitted from collection. All other data will be collected as usual.  
5. Click Enable. A popup which redirects you to your Salesforce instance appears, to get OAuth 2.0 authorization credentials and access.  
6. Click OK.  
   In Salesforce.com, a new tab appears.  
7. Enter your username and password, and Log In.   
8. When you are asked to allow access, select Allow.  
   A Salesforce data collection instance is created, and an authorization token is created and returned to Cortex XSIAM. Data collection begins.

###### Task 6\. (Optional) Edit or test existing Salesforce.com collector settings

You can edit and test an existing collector instance after a successful initial connection between Salesforce.com and Cortex XSIAM. Do this by clicking Edit (pencil icon) for the collector instance. The log collection window will be displayed, where you can make changes or test, by clicking Test.

###### Troubleshooting

If for any reason, the token is not created and sent to Cortex XSIAM, after a timeout period, an authorization failure error will be returned for the collector instance. In this case, try again by clicking Edit (pencil icon) for the collector instance. The log collection window will be displayed again, where you can edit settings and retry getting the authorization code.

### Ingest Data from ServiceNow CMDB

Abstract

Extend Cortex XSIAM visibility into data from ServiceNow CMDB.

To receive data from the ServiceNow CMDB database, you must first configure data collection from ServiceNow CMDB. ServiceNow CMDB is a logical representations of assets, services, and the relationships between them that comprise the infrastructure of an organization. It is built as a series of connected tables that contain all the assets and business services controlled by a company and its configurations. You can configure the Collection Integration settings in Cortex XSIAM for the ServiceNow CMDB database, which includes selecting the specific tables containing the data that you want to collect, in the ServiceNow CMDB Collector. You can select from the list of default tables and also specify custom tables. By default, the ServiceNow CMDB Collector is configured to collect data from the following tables, which you can always change depending on your system requirements.

* `cmdb_ci`  
* `cmdb_ci_computer`  
* `cmdb_rel_ci`  
* `cmdb_ci_application_software`

As soon as Cortex XSIAM begins receiving data, the app automatically creates a ServiceNow CMDB dataset for each table using the format `servicenow_cmdb_<table name>_raw`. You can then use XQL Search queries to view the data and create new Correlation Rules.

You can only configure a single ServiceNow CMDB Collector, which is automatically configured every 6 hours to reload the data from the configured tables and replace the existing data. You can always use the Sync Now option to reload the data and replace the existing data whenever you want.

Complete the following task before you begin configuring Cortex XSIAM to receive data from ServiceNow CMDB.

* Create a ServiceNow CMDB user with SNOW credentials, who is designated to access the tables from ServiceNow CMDB for data collection in Cortex XSIAM. Record the credentials for this user as you will need them when configuring the ServiceNow CMDB Collector in Cortex XSIAM.

Configure Cortex XSIAM to receive data from ServiceNow CMDB:

1. Select Settings → Data Sources.  
2. On the Data Sources page, click Add Data Source, search for and select ServiceNow CMDB, and click Connect.  
3. Set the following parameters.  
   * Domain: Specify your ServiceNow CMDB domain URL.  
   * User Name: Specify the username for your ServiceNow CMDB user designated in Cortex XSIAM.  
   * Password: Specify the password for your ServiceNow CMDB user designated in Cortex XSIAM.  
   * Tables: You can do any of the following actions to configure the tables whose data is collected from ServiceNow CMDB.  
     * Select the tables from the list of default ServiceNow CMDB tables that you want to collect from. After each table selection, select blue-arrow.png to add the table to the tables already listed below for data collection.  
     * Specify any custom tables that you want to configure for data collection.  
     * From the default list of tables already configured, you can delete any of them by hovering over the table and selecting the X icon.  
4. Click Test to validate access, and then click Enable.  
   Once events start to come in, a green check mark appears underneath the ServiceNow CMDB Collector configuration with the data and time that the data was last synced.  
5. (Optional) Manage your ServiceNow CMDB Collector.  
   After you enable the ServiceNow CMDB Collector, you can make additional changes as needed. To modify a configuration, select any of the following options:  
   * Edit the ServiceNow CMDB Collector settings.  
   * Disable the ServiceNow CMDB Collector.  
   * Delete the ServiceNow CMDB Collector.  
   * Sync Now to get the latest data from the tables configured. The data is replaced automatically every 6 hours, but you can always get the latest data as needed.  
6. After Cortex XSIAM begins receiving data from ServiceNow CMDB, you can use the XQL Search to search for logs in the new datasets, where each dataset name is based on the table name using the format `servicenow_cmdb_<table name>_raw`.

### Ingest Report Data from Workday

Abstract

Extend Cortex XSIAM visibility into reports data from Workday.

To receive Workday report data, you must first configure data collection from Workday using a Workday custom report to ingest the appropriate data. This is configured by setting up a Workday Collector in Cortex XSIAM and configuring report data collection via this Workday custom report that you set up.

As soon as Cortex XSIAM begins receiving data, the app automatically creates a Workday Cortex Query Language (XQL) dataset (`workday_workday_raw`). You can then use XQL Search queries to view the data and create new Correlation Rules. In addition, Cortex XSIAM adds the workday fields next to each user in the Key Assets list in the Incident View, and in the User node in the Causality View of Identity Analytics alerts.

Any user with permissions to view alerts and incidents can view the Workday data.

You can only configure a single Workday Collector, which is automatically configured to run the report every 6 hours. You can always use the Sync Now option to run the report whenever you want.

1. Create an Integration System User that is designated to access the custom report from Workday for data collection in Cortex XSIAM.  
2. Create an Integration System Security Group for the Integration System User created in Step 1 for accessing the report. When setting this group ensure to define the following:  
   * Type of Tenanted Security Group: Select either Integration System Security Group (Constrained) or Integration System Security Group (Unconstrained) depending on how your data is configured. For more information, see the Workday documentation.  
   * Integration System User: Select the user that you defined in step 1 for accessing the custom report.  
3. Create the Workday credentials for the Integration System User created in Step 1 so that the username and password can be used to access the report in Cortex XSIAM. Record these credentials as you will need them when configuring the Workday Collector in Cortex XSIAM.

For more information on completing any of the prerequisite steps, see the Workday documentation.

Configure Cortex XSIAM to receive report data from Workday:

1. Configure a Workday custom report to use for data collection.  
   * Login to the [Workday Resource Center](https://signin.resourcecenter.workday.com/).  
   * In the search field, specify Create Custom Report to open the wizard.  
   * Configure the following Create Custom Report settings:  
     workday-create-custom-report.png  
     * Report Name: Specify the name of the report.  
     * Report Details section:  
       * Report Type: Select Advanced. When you select this option, the Enable As Web Service checkbox is displayed.  
       * Enable As Web Service: Select this checkbox, so that you will be able to generate a URL of the report to configure in Cortex XSIAM.  
     * Data Source section:  
       * Optimized for Performance: Select whether the data should be optimized for performance. The way this checkbox is configured determines the Data Source options available to choose from.  
       * Date Source: Select the applicable data source containing the data that is used to configure data collection from Workday to Cortex XSIAM.  
   * Click OK, and configure the following Additional Info settings.  
     The Additional Info table in the Columns tab is where you can perform the following.  
     * For the incident and card views in Cortex XSIAM, map the required fields from the Data Source configured by selecting the applicable Field that you want to map to the Cortex XSIAM field name required for data collection in the Column Heading Override XML Alias column.  
     * (Optional) You can map any additional fields from the Data Source configured that you want to be able to query in XQL Search using the `workday_workday_raw` dataset. This is configured by selecting the applicable Field and leaving the default field name that is displayed in the Column Heading Override XML Alias column. This default field name is what is used in XQL Search and the dataset to view and query the data.  
   * workday-additional-info.png  
     The Business Object changes depending on the Data Source selected.  
     For the incident and card views in Cortex XSIAM, map the following fields in the table by selecting the applicable Field that contains the data representing the Cortex XSIAM field name as provided below that should be added to the Column Heading Override XML Alias. For example, for `full_name`, select the applicable Field from the Business Object defined that contains the full name of the user and in the Column Heading Override XML Alias specify `full_name` to map the set Field to the Cortex XSIAM field name.  
     Cortex XSIAM uses a structured schema when integrating Workday data. To get the best Analytics results, specify all the fields marked with an asterisk from the recommended schema.  
     * `workday_user_id*`  
     * `full_name*`  
     * `workday_manager_user_id*`  
     * `manager*`  
     * `worker_type*`  
     * `position_title*`  
     * `department*`  
     * `private_email_address*`  
     * `business_email_address*`  
     * `employment_start_date*`  
     * `employment_end_date`  
     * `phone_number`  
     * `mailing_address`  
   * (Optional) Filter out any employees that you do not want included in the Filter tab.  
   * Share access to the report with the designated Integration System User that you created by setting the following settings in the Share tab:  
     * Report Definition Sharing Options: Select Share with specific authorized groups and users.  
     * Authorized Users: Select the designated Integration System User that you created for accessing the custom report.  
   * Ensure that the following Web Services Options settings in the Advanced tab are configured.  
     Here is an example of the configured settings, where the Web Service API Version and Namespace are automatically populated and dependent on your report.  
     workday-web-services-options.png  
   * (Optional) Test the report to ensure all the fields are populated.  
   * Get the URL for the report.  
     * In the related actions menu, select Actions → Web Service → View URLs.  
     * Click OK.  
     * Scroll down to the JSON section.  
     * Hover over the JSON link and click the icon, which open a new tab in your browser with the URL for the report. You need to use the designated user credentials to open the report.  
     * Copy the URL for the report and record them somewhere as this URL needs to be provided when setting up the Workday Collector in Cortex XSIAM.  
   * Complete the report by clicking Done.  
2. Configure the Workday collection in Cortex XSIAM.  
   * Select Settings → Data Sources.  
   * On the Data Sources page, click Add Data Source, search for and select Workday, and click Connect.  
   * Set the following parameters.  
     * Name: Specify the name for the Workday Collector that is displayed in Cortex XSIAM.  
     * URL: Specify the URL of the custom report you configured in Workday.  
     * User Name: Specify the username for the designated Integration System User that you created for accessing the custom report in Workday.  
     * Password: Specify the password for the designated Integration System User that you created for accessing the custom report in Workday.  
   * Click Test to validate access, and then click Enable.  
     A notification appears confirming that the Workday Collector was saved successfully, and closes on its own after a few seconds.  
     Once report data starts to come in, a green check mark appears underneath the Workday Collector configuration with the data and time that the data was last synced.  
3. (Optional) Manage your Workday Collector.  
   After you enable the Workday Collector, you can make additional changes as needed. To modify a configuration, select any of the following options.  
   * Edit the Workday Collector settings.  
   * Disable the Workday Collector.  
   * Delete the Workday Collector.  
   * Sync Now to run the report to get the latest report data. The report is run automatically every 6 hours, but you can always get the latest data as needed.  
4. After Cortex XSIAM begins receiving report data from Workday, you can use the XQL Search to search for logs in the new dataset (`workday_workday_raw`).

### Ingest external alerts

Abstract

For a more complete and detailed picture of the activity involved in an incident, Cortex XSIAM can ingest alerts from any external source.

For a more complete and detailed picture of the activity involved in an incident, Cortex XSIAM can ingest alerts from any external source. Cortex XSIAM stitches the external alerts together with relevant endpoint data and displays alerts from external sources in relevant incidents and alerts tables. You can also see external alerts and related artifacts and assets in Causality views.

To ingest alerts from an external source, you configure your alert source to forward alerts (in Auto-Detect (default), CEF, LEEF, CISCO, or CORELIGHT format) to the Syslog collector. You can also ingest alerts from external sources using the Cortex XSIAM APIs.

After Cortex XSIAM begins receiving external alerts, you must map the following required fields to the Cortex XSIAM format.

* TIMESTAMP  
* SEVERITY  
* ALERT NAME

In addition, these optional fields are available, if you want to map them to the Cortex XSIAM format.

* SOURCE IP  
* SOURCE PORT  
* DESTINATION IP  
* DESTINATION PORT  
* DESCRIPTION  
* DIRECTION  
* EXTERNAL ID  
* CATEGORY  
* ACTION  
* PROCESS COMMAND LINE  
* PROCESS SHA256  
* DOMAIN  
* PROCESS FILE PATH  
* HOSTNAME  
* USERNAME

If you send pre-parsed alerts using the Cortex XSIAM API, additional mapping is not required.

Storage of external alerts is determined by your Cortex XSIAM tenant retention policy. For more information, see Dataset Management.

1. Send alerts from an external source to Cortex XSIAM.  
   There are two ways to send alerts:  
   1. API: Use the **Insert CEF Alerts API** to send the raw Syslog alerts or use the **Insert Parsed Alerts API** to convert the Syslog alerts to the Cortex XSIAM format before sending them to Cortex XSIAM. If you use the API to send logs, you do not need to perform the additional mapping step in Cortex XSIAM.  
   2. Activate the Syslog collector and then configure the alert source to forward alerts to the Syslog collector. Then configure an alert mapping rule as follows.  
2. In Cortex XSIAM, select Settings → Configurations → Data Collection.  
3. Right-click the Vendor Product for your alerts and select Filter and Map.  
4. Use the filters at the top of the table to narrow the results to only the alerts you want to map.  
   Cortex XSIAM displays a limited sample of results during the mapping rule creation. As you define your filters, Cortex XSIAM applies the filter to the limited sample but does not apply the filters across all alerts. As a result, you might not see any results from the alert sample during the rule creation.  
5. Click Next to begin a new mapping rule.  
   On the left, configure the following:  
   1. Rule Information: Define the NAME and optional DESCRIPTION to identify your mapping rule.  
   2. Alerts Field: Map each required and any optional Cortex XSIAM field to a field in your alert source.  
      If needed, use the field converter (field-converter.png) to translate the source field to the Cortex XSIAM syntax.  
      For example, if you use a different severity system, you need to use the converter to map your severities fields to the Cortex XSIAM risks of Critical, High, Medium, and Low.  
      You can also use regex to convert the fields to extract the data to facilitate matching with the Cortex XSIAM format. For example, if you need to map the port, but your source field contains both the IP address and port (`192.168.1.200:8080`), to extract everything after the `:`, use the following regex:  
      `^[^:]*_`  
      For additional context when you are investigating an incident, you can also map additional optional fields to fields in your alert source.  
6. Submit your alert filter and mapping rule when finished.