import boto3

def delete_user(email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')
    
    # Check if the user exists
    response = table.get_item(Key={'email': email})
    if 'Item' not in response:
        return False, "User not found."

    # Delete the user
    table.delete_item(Key={'email': email})
    return True, "User deleted successfully."
