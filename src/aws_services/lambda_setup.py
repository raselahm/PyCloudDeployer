import boto3
import zipfile
import os
import sys
import time

def deploy_lambda_function(lambda_role_arn):
    lambda_client = boto3.client('lambda')
    lambda_function_path = os.path.join(os.path.dirname(__file__), 'lambda_functions', 'lambda_function.py')

    # Find the site-packages directory
    site_packages_path = next(p for p in sys.path if 'site-packages' in p)

    # Locate the pytz directory within site-packages
    pytz_path = os.path.join(site_packages_path, 'pytz')

    zip_file_name = 'lambda_function_package.zip'

    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add lambda_function.py
        zf.write(lambda_function_path, 'lambda_function.py')

        # Add pytz library
        for folder, subfolders, files in os.walk(pytz_path):
            for file in files:
                full_path = os.path.join(folder, file)
                rel_path = os.path.relpath(full_path, site_packages_path)
                zf.write(full_path, rel_path)

    with open(zip_file_name, 'rb') as zip_file:
        zip_buffer = zip_file.read()

    try:
        lambda_client.get_function(FunctionName='BirthdayEmailFunction')
        print("Lambda function already exists.")
    except lambda_client.exceptions.ResourceNotFoundException:
        time.sleep(10)
        lambda_client.create_function(
            FunctionName='BirthdayEmailFunction',
            Runtime='python3.11',  
            Role=lambda_role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_buffer},
        )
        print("Lambda function deployed successfully.")

        lambda_client.add_permission(
            FunctionName='BirthdayEmailFunction',
            StatementId='EventBridgeInvoke',
            Action='lambda:InvokeFunction',
            Principal='events.amazonaws.com'
        )
        print("Permission for EventBridge to invoke Lambda function added.")

