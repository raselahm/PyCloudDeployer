import boto3

def add_user_to_db(email, name, date_of_birth):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')

    try:
        response = table.put_item(
            Item={
                'email': email,
                'name': name,
                'date_of_birth': date_of_birth
            }
        )
        return True
    except Exception as e:
        print(f"Error adding user: {e}")
        return False