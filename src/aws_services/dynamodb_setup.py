import boto3
from botocore.exceptions import ClientError
import time

def setup_dynamodb():
    dynamodb = boto3.client('dynamodb')

    table_name = 'Users'
    attribute_definitions = [{'AttributeName': 'email', 'AttributeType': 'S'}]
    key_schema = [{'AttributeName': 'email', 'KeyType': 'HASH'}]
    provisioned_throughput = {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}

    try:
        dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=attribute_definitions,
            KeySchema=key_schema,
            ProvisionedThroughput=provisioned_throughput
        )
        print(f"Table {table_name} created successfully.")

        # Wait for the table to be created
        print("Waiting for table to become active...")
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName=table_name)

        # Enable point-in-time recovery
        dynamodb.update_continuous_backups(
            TableName=table_name,
            PointInTimeRecoverySpecification={'PointInTimeRecoveryEnabled': True}
        )
        print(f"Point-in-time recovery enabled for table {table_name}.")

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table {table_name} already exists.")
        else:
            print(f"An error occurred: {e.response['Error']['Message']}")

if __name__ == '__main__':
    setup_dynamodb()


