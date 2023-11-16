import boto3
from datetime import datetime

def lambda_handler(event, context):
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')

    # Get today's date in the format stored in DynamoDB
    today_date = datetime.now().strftime('%Y-%m-%d')

    # Scan the table with a filter for today's date
    response = table.scan(
        ProjectionExpression='email, date_of_birth',
        FilterExpression='date_of_birth = :today',
        ExpressionAttributeValues={':today': today_date}
    )

    # Process and print each item that matches today's date
    for item in response.get('Items', []):
        print(f"Email: {item.get('email')} - DOB: {item.get('date_of_birth')}")

    return {
        'statusCode': 200,
        'body': 'Processed DynamoDB records for today successfully'
    }
