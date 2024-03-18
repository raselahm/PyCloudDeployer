import boto3
import zipfile
import os
import sys
import time

def create_zip_file(function_name, pytz_path):
    lambda_function_path = os.path.join(os.path.dirname(__file__), 'lambda_functions', function_name)
    zip_file_name = f'{function_name[:-3]}_package.zip'

    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(lambda_function_path, function_name)

        if function_name == 'lambda_function.py':
            # Add entire pytz directory, including zoneinfo
            for folder, subfolders, files in os.walk(pytz_path):
                for file in files:
                    full_path = os.path.join(folder, file)
                    rel_path = os.path.relpath(full_path, start=os.path.dirname(pytz_path))  # Change start path to include pytz
                    zf.write(full_path, rel_path)
    
    return zip_file_name

def deploy_lambda_function(lambda_role_arn, function_name, handler):
    lambda_client = boto3.client('lambda')

    site_packages_path = next(p for p in sys.path if 'site-packages' in p)
    pytz_path = os.path.join(site_packages_path, 'pytz')

    zip_file_name = create_zip_file(function_name, pytz_path)

    with open(zip_file_name, 'rb') as zip_file:
        zip_buffer = zip_file.read()

    try:
        response = lambda_client.get_function(FunctionName=function_name[:-3])
        print(f"Lambda function {function_name} already exists.")
        return response['Configuration']['FunctionArn']
    except lambda_client.exceptions.ResourceNotFoundException:
        time.sleep(10)  # Wait to ensure IAM role is available
        response = lambda_client.create_function(
            FunctionName=function_name[:-3],
            Runtime='python3.11',
            Role=lambda_role_arn,
            Handler=handler,
            Code={'ZipFile': zip_buffer},
        )
        print(f"Lambda function {function_name} deployed successfully.")
        return response['FunctionArn']

def deploy_all_lambda_functions(lambda_role_arn):
    lambda_client = boto3.client('lambda')

    birthday_email_function_arn = deploy_lambda_function(lambda_role_arn, 'lambda_function.py', 'lambda_function.lambda_handler')
    email_verification_function_arn = deploy_lambda_function(lambda_role_arn, 'email_verification_lambda.py', 'email_verification_lambda.lambda_handler')

    # Add permissions to the functions
    for function_arn in [birthday_email_function_arn, email_verification_function_arn]:
        try:
            lambda_client.add_permission(
                FunctionName=function_arn.split(':function:')[1],
                StatementId='EventBridgeInvoke',
                Action='lambda:InvokeFunction',
                Principal='events.amazonaws.com'
            )
            print(f"Permission for EventBridge to invoke Lambda function added for {function_arn.split(':function:')[1]}.")
        except Exception as e:
            print(f"Failed to add permission for Lambda function {function_arn.split(':function:')[1]}: {e}")

    print("All Lambda functions deployed and permissions set.")
    return birthday_email_function_arn, email_verification_function_arn

