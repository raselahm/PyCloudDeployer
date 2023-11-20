import boto3
import json
from botocore.exceptions import ClientError

def create_lambda_execution_role():
    iam_client = boto3.client('iam')
    role_name = 'PyCloudDeployerLambdaExecutionRole'
    assume_role_policy = json.dumps({
        'Version': '2012-10-17',
        'Statement': [{
            'Effect': 'Allow',
            'Principal': {'Service': 'lambda.amazonaws.com'},
            'Action': 'sts:AssumeRole'
        }]
    })

    try:
        response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=assume_role_policy
        )
        role_arn = response['Role']['Arn']

        # Attach the AWSLambdaBasicExecutionRole policy for basic Lambda execution
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )

        # Inline policy to grant access to DynamoDB, CloudWatch, SES, SSM, and S3
        policy = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Effect': 'Allow',
                    'Action': [
                        'dynamodb:*',
                        'cloudwatch:*',
                        'ses:SendEmail', 'ses:SendRawEmail', 'ses:VerifyEmailIdentity',
                        'ssm:GetParameter',
                        's3:*',  # Permission to perform all actions on S3
                        'dynamodb:ExportTableToPointInTime'  # Permission to export DynamoDB data
                    ],
                    'Resource': '*'  
                }
            ]
        }

        iam_client.put_role_policy(
            RoleName=role_name,
            PolicyName='PyCloudDeployerAdditionalPermissions',
            PolicyDocument=json.dumps(policy)
        )

        print(f"Created role: {role_name}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print(f"Role {role_name} already exists.")
            role_arn = iam_client.get_role(RoleName=role_name)['Role']['Arn']
        else:
            raise e

    return role_arn

if __name__ == '__main__':
    create_lambda_execution_role()


