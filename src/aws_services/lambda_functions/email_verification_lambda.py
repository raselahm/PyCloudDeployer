import boto3
from botocore.exceptions import ClientError

def send_verification_email(email):
    ses_client = boto3.client('ses')
    try:
        response = ses_client.verify_email_identity(EmailAddress=email)
        return response
    except ClientError as error:
        print(f"Error sending verification email: {error}")
        return None

def lambda_handler(event, context):
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')

    # Scan the table for unverified email addresses
    response = table.scan(
        ProjectionExpression='email, email_verified',
        FilterExpression='attribute_not_exists(email_verified) or email_verified = :val',
        ExpressionAttributeValues={':val': False}
    )

    # Process each unverified email
    for item in response.get('Items', []):
        email = item.get('email')
        if email:
            verification_response = send_verification_email(email)
            if verification_response:
                print(f"Sent verification email to: {email}")
            else:
                print(f"Failed to send verification email to {email}")

    return {
        'statusCode': 200,
        'body': 'Processed unverified emails successfully'
    }

