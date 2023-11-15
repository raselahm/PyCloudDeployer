import boto3
from botocore.exceptions import ClientError

def setup_dynamodb():
    # Create a DynamoDB service client
    dynamodb = boto3.client('dynamodb')

    # Define the table name and schema
    table_name = 'Users'
    attribute_definitions = [
        {'AttributeName': 'email', 'AttributeType': 'S'}  # Only key attribute is 'email'
    ]
    key_schema = [
        {'AttributeName': 'email', 'KeyType': 'HASH'}  # Partition key
    ]
    provisioned_throughput = {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }

    # Create the DynamoDB table
    try:
        response = dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=attribute_definitions,
            KeySchema=key_schema,
            ProvisionedThroughput=provisioned_throughput
        )
        print(f"Table {table_name} created successfully.")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table {table_name} already exists.")
        else:
            print(f"An error occurred: {e.response['Error']['Message']}")
        return None

if __name__ == '__main__':
    setup_dynamodb()

