import boto3
import zipfile
import io
import os

def deploy_lambda_function(lambda_role_arn):
    lambda_client = boto3.client('lambda')

    # Path to Lambda function code
    lambda_function_path = os.path.join(os.path.dirname(__file__), 'lambda_functions', 'lambda_function.py')

    # Zip Lambda function code
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a') as zf:
        zf.writestr('lambda_function.py', open(lambda_function_path, 'rb').read())
    zip_buffer.seek(0)

    # Check if the function already exists
    try:
        lambda_client.get_function(FunctionName='BirthdayEmailFunction')
        print("Lambda function already exists.")
    except lambda_client.exceptions.ResourceNotFoundException:
        # Deploy the Lambda function if it doesn't exist
        lambda_client.create_function(
            FunctionName='BirthdayEmailFunction',
            Runtime='python3.11',  
            Role=lambda_role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_buffer.read()},
        )
        print("Lambda function deployed successfully.")