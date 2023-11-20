import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

def check_aws_config():
    try:
        # Attempt to list S3 buckets as a test of AWS credentials and configuration
        boto3.client('s3').list_buckets()
        print("AWS configuration and credentials are set up correctly.")
        return True
    except (NoCredentialsError, PartialCredentialsError, ClientError) as e:
        print(f"Error with AWS configuration/credentials: {e}")
        return False

if __name__ == '__main__':
    check_aws_config()
