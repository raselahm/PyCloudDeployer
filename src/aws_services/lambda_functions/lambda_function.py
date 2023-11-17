import boto3
import pytz
from datetime import datetime

def lambda_handler(event, context):
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')

    # Convert UTC time to Eastern Time Zone
    eastern = pytz.timezone('America/New_York')
    today_date = datetime.now(pytz.utc).astimezone(eastern).strftime('%Y-%m-%d')

    # Scan the table with a filter for today's date
    response = table.scan(
        ProjectionExpression='email, date_of_birth',
        FilterExpression='date_of_birth = :today',
        ExpressionAttributeValues={':today': today_date}
    )

    # SES client and SSM client
    ses_client = boto3.client('ses')
    ssm_client = boto3.client('ssm')

    # Retrieve the verified email from Parameter Store
    sender_email = ssm_client.get_parameter(Name='PyCloudDeployerVerifiedEmail')['Parameter']['Value']

    # Process each item that matches today's date
    for item in response.get('Items', []):
        recipient_email = item.get('email')
        email_subject = 'Happy Birthday!'
        email_body = f"Happy Birthday {item.get('name', 'User')}!"

        # Send email using SES
        try:
            ses_client.send_email(
                Source=sender_email,
                Destination={'ToAddresses': [recipient_email]},
                Message={
                    'Subject': {'Data': email_subject},
                    'Body': {'Text': {'Data': email_body}}
                }
            )
            print(f"Sent birthday email to: {recipient_email}")
        except Exception as e:
            print(f"Failed to send email to {recipient_email}: {e}")

    return {
        'statusCode': 200,
        'body': 'Processed DynamoDB records and sent emails successfully'
    }