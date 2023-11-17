import boto3
from botocore.exceptions import ClientError

def check_email_verification_status(email):
    ses_client = boto3.client('ses')
    try:
        response = ses_client.get_identity_verification_attributes(
            Identities=[email]
        )
        verification_attributes = response['VerificationAttributes']
        if email in verification_attributes:
            return verification_attributes[email]['VerificationStatus'] == 'Success'
        return False
    except ClientError as error:
        print(f"Error checking verification status: {error}")
        return False

def setup_ses(email):
    ses_client = boto3.client('ses')
    ssm_client = boto3.client('ssm')

    if not check_email_verification_status(email):
        try:
            ses_client.verify_email_identity(EmailAddress=email)
            print(f"Verification email sent to {email}. Please verify it.")
            # Save email to Parameter Store after sending verification
            ssm_client.put_parameter(
                Name='PyCloudDeployerVerifiedEmail',
                Value=email,
                Type='String',
                Overwrite=True
            )
        except ClientError as error:
            print(f"Error sending verification email: {error}")
    else:
        print(f"Email {email} is already verified.")
        # Update Parameter Store with the already verified email
        ssm_client.put_parameter(
            Name='PyCloudDeployerVerifiedEmail',
            Value=email,
            Type='String',
            Overwrite=True
        )
