import csv
import boto3

def is_valid_csv(file_path, required_fields):
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not all(field in row for field in required_fields):
                    return False
            return True
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return False

def email_exists_in_db(table, email):
    response = table.get_item(Key={'email': email})
    return 'Item' in response

def batch_write_items(dynamodb_client, table_name, items, operation_type):
    request_items = []
    for item in items:
        if operation_type == 'PutRequest':
            
            formatted_item = {k: {'S': str(v)} for k, v in item.items()}
            request_items.append({'PutRequest': {'Item': formatted_item}})
        elif operation_type == 'DeleteRequest':
            
            request_items.append({'DeleteRequest': {'Key': {'email': {'S': item['email']}}}})
    
    dynamodb_client.batch_write_item(RequestItems={table_name: request_items})

def upload_users_from_csv(file_path):
    dynamodb_client = boto3.client('dynamodb')
    table_name = 'Users'  
    required_fields = ['email', 'name', 'date_of_birth']

    if not is_valid_csv(file_path, required_fields):
        print("Invalid CSV file or missing fields.")
        return []

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    items_to_upload = []
    uploaded_users = []

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            email = row['email']
            if email_exists_in_db(table, email):
                print(f"Email already exists in database: {email}")
                continue
            items_to_upload.append(row)
            uploaded_users.append(row)

            if len(items_to_upload) == 25:
                batch_write_items(dynamodb_client, table_name, items_to_upload, 'PutRequest')
                items_to_upload.clear()

    if items_to_upload:
        batch_write_items(dynamodb_client, table_name, items_to_upload, 'PutRequest')

    return uploaded_users

def delete_users_from_csv(file_path):
    dynamodb_client = boto3.client('dynamodb')
    table_name = 'Users'  
    required_fields = ['email']

    if not is_valid_csv(file_path, required_fields):
        print("Invalid CSV file or missing email field.")
        return

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    items_to_delete = []

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            email = row['email']
            if not email_exists_in_db(table, email):
                print(f"Email not found in database: {email}")
                continue
            items_to_delete.append({'email': email})

            if len(items_to_delete) == 25:
                batch_write_items(dynamodb_client, table_name, items_to_delete, 'DeleteRequest')
                items_to_delete.clear()

    if items_to_delete:
        batch_write_items(dynamodb_client, table_name, items_to_delete, 'DeleteRequest')
