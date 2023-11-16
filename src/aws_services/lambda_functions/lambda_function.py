import boto3
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')

    # Scan the table
    response = table.scan(
        ProjectionExpression='email, date_of_birth'  # Only fetch these attributes
    )

    # Process and print each item's date of birth
    for item in response.get('Items', []):
        print(f"Email: {item.get('email')} - DOB: {item.get('date_of_birth')}")

    return {
        'statusCode': 200,
        'body': 'Processed DynamoDB records successfully'
    }
