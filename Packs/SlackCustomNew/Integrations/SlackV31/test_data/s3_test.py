import boto3

# Define the role ARN, external ID, and your session name
role_arn = 'arn:aws:iam::764001573281:role/cortex-xsiam-log-role'
external_id = '2ab8f8a8-4d65-402a-b525-049f0fee5b01'
session_name = 'my-session'

# Create an STS client and assume the role
sts_client = boto3.client('sts')
assumed_role = sts_client.assume_role(
    RoleArn=role_arn,
    ExternalId=external_id,
    RoleSessionName=session_name
)

# Get temporary credentials
aws_access_key_id = assumed_role['Credentials']['AccessKeyId']
aws_secret_access_key = assumed_role['Credentials']['SecretAccessKey']
aws_session_token = assumed_role['Credentials']['SessionToken']

# Use the temporary credentials to create an S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

print(aws_access_key_id)