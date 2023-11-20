import boto3
from botocore.exceptions import ClientError

def delete_dynamodb_table(table_name):
    dynamodb = boto3.client('dynamodb')
    try:
        dynamodb.delete_table(TableName=table_name)
        print(f"DynamoDB table '{table_name}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting DynamoDB table '{table_name}': {e}")

def delete_lambda_function(function_name):
    lambda_client = boto3.client('lambda')
    try:
        lambda_client.delete_function(FunctionName=function_name)
        print(f"Lambda function '{function_name}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting Lambda function '{function_name}': {e}")

def delete_cloudwatch_event(rule_name):
    events_client = boto3.client('events')
    try:
        # Remove targets
        events_client.remove_targets(Rule=rule_name, Ids=['1'])
        # Delete the rule
        events_client.delete_rule(Name=rule_name)
        print(f"CloudWatch event '{rule_name}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting CloudWatch event '{rule_name}': {e}")

def delete_iam_role(role_name):
    iam = boto3.client('iam')
    try:
        # Detach all managed policies
        policies = iam.list_attached_role_policies(RoleName=role_name)
        for policy in policies.get('AttachedPolicies', []):
            iam.detach_role_policy(RoleName=role_name, PolicyArn=policy['PolicyArn'])
        
        # Delete inline policies
        inline_policies = iam.list_role_policies(RoleName=role_name)
        for policy_name in inline_policies.get('PolicyNames', []):
            iam.delete_role_policy(RoleName=role_name, PolicyName=policy_name)

        # Delete the role
        iam.delete_role(RoleName=role_name)
        print(f"IAM role '{role_name}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting IAM role '{role_name}': {e}")

def bucket_exists(bucket_name):
    s3 = boto3.resource('s3')
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError:
        return False

def create_s3_bucket(bucket_name):
    s3_client = boto3.client('s3')
    region = boto3.session.Session().region_name

    try:
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                'LocationConstraint': region
            })
    except ClientError as e:
        print(f"Error creating S3 bucket '{bucket_name}': {e}")
        raise e

def export_dynamodb_to_s3(table_name, s3_bucket_name):
    dynamodb_client = boto3.client('dynamodb')

    if not bucket_exists(s3_bucket_name):
        if not create_s3_bucket(s3_bucket_name):
            print(f"Unable to create or access S3 bucket '{s3_bucket_name}'.")
            return

    try:
        response = dynamodb_client.export_table_to_point_in_time(
            TableArn=f'arn:aws:dynamodb:{boto3.session.Session().region_name}:{boto3.client("sts").get_caller_identity().get("Account")}:table/{table_name}',
            S3Bucket=s3_bucket_name,
            ExportFormat='DYNAMODB_JSON'
        )
        print(f"Export job initiated for DynamoDB table '{table_name}' to S3 bucket '{s3_bucket_name}'.")
    except Exception as e:
        print(f"Error exporting DynamoDB table '{table_name}' to S3: {e}")

def teardown_services(export_to_s3=False, s3_bucket_name=None):
    if export_to_s3 and s3_bucket_name:
        export_dynamodb_to_s3('Users', s3_bucket_name)
    
    delete_dynamodb_table('Users')
    delete_lambda_function('lambda_function') 
    delete_lambda_function('email_verification_lambda') 
    delete_cloudwatch_event('PyCloudDeployerDailyTrigger')
    delete_iam_role('PyCloudDeployerLambdaExecutionRole')
