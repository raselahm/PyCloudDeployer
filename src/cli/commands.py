import json
import click
import re
from datetime import datetime
import boto3
import pytz
from aws_services.user_management.adduser import add_user_to_db
from aws_services.user_management.deleteuser import delete_user
from aws_services.user_management.csvoperations import upload_users_from_csv, delete_users_from_csv
from aws_services.ses_setup import setup_ses, check_email_verification_status
from aws_services.teardown import create_s3_bucket, bucket_exists, teardown_services

def validate_email(ctx, param, value):
    pattern = r'[^@]+@[^@]+\.[^@]+'
    if not re.match(pattern, value):
        raise click.BadParameter('Email format is invalid.')
    return value

def validate_date(ctx, param, value):
    try:
        datetime.strptime(value, '%Y-%m-%d')
        return value
    except ValueError:
        raise click.BadParameter('Date must be in YYYY-MM-DD format.')

@click.command()
@click.option('--email', prompt='User email', help='Email of the user.', callback=validate_email)
@click.option('--name', prompt='User name', help='Name of the user.')
@click.option('--dob', prompt='Date of Birth (YYYY-MM-DD)', help='Date of birth of the user.', callback=validate_date)
def adduser(email, name, dob):
    if add_user_to_db(email, name, dob):
        click.echo('User added successfully.')
        # Invoke email verification lambda function
        lambda_client = boto3.client('lambda')
        lambda_client.invoke(
            FunctionName='email_verification_lambda', 
            InvocationType='Event',
            Payload=json.dumps({'email': email})
        )
    else:
        click.echo('Failed to add user.')

@click.command()
@click.argument('file_path')
def uploadcsv(file_path):
    uploaded_users = upload_users_from_csv(file_path)
    click.echo(f"Attempted to upload users from {file_path}.")

    # Invoke email verification lambda for each uploaded user
    lambda_client = boto3.client('lambda')
    for user in uploaded_users:
        lambda_client.invoke(
            FunctionName='email_verification_lambda', 
            InvocationType='Event',
            Payload=json.dumps({'email': user['email']})
        )

@click.command()
@click.argument('file_path')
def deletecsv(file_path):
    """Delete users from a CSV file."""
    delete_users_from_csv(file_path)
    click.echo(f"Attempted to delete users from {file_path}.")

@click.command()
@click.option('--email', prompt='User email', help='Email of the user to delete.')
def deleteuser(email):
    success, message = delete_user(email)
    click.echo(message)

def create_cron_expression(hour, minute, timezone='America/New_York'):
    local = pytz.timezone(timezone)
    naive = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return f'cron({utc_dt.minute} {utc_dt.hour} * * ? *)'

@click.command(name='settriggertime')
@click.option('--hour', type=int, prompt='Hour (0-23)')
@click.option('--minute', type=int, prompt='Minute (0-59)')
def settriggertime(hour, minute):
    cloudwatch_events_client = boto3.client('events')
    cron_expression = create_cron_expression(hour, minute)
    cloudwatch_events_client.put_rule(
        Name='PyCloudDeployerDailyTrigger',
        ScheduleExpression=cron_expression,
        State='ENABLED'
    )
    click.echo(f"Trigger time set to {hour}:{minute} (local time). Cron expression: {cron_expression}")

@click.command(name='setupses')
def setupses():
    email = click.prompt("Please enter your email for SES", type=str, callback=validate_email)
    if check_email_verification_status(email):
        if not click.confirm(f"The email {email} is already verified. Do you want to resend the verification email?"):
            return
    setup_ses(email)

@click.command()
def teardown():
    """Safely remove all deployed AWS services."""
    if click.confirm('Do you want to export DynamoDB data to an S3 bucket before tearing down services?'):
        export_attempted = False
        while not export_attempted:
            bucket_name = click.prompt('Enter the S3 bucket name', type=str)

            # Check if the S3 bucket exists
            if bucket_exists(bucket_name):
                if click.confirm(f"S3 bucket '{bucket_name}' already exists. Would you like to use this existing bucket?"):
                    export_attempted = True
                else:
                    click.echo("Please enter a different bucket name.")
            else:
                # Attempt to create the bucket
                try:
                    create_s3_bucket(bucket_name)
                    click.echo(f"S3 bucket '{bucket_name}' created successfully.")
                    export_attempted = True
                except Exception as e:
                    click.echo(f"Error creating S3 bucket '{bucket_name}': {e}")
                    if not click.confirm("Do you want to try a different bucket name?"):
                        if click.confirm("Do you want to proceed with teardown without exporting data?"):
                            export_attempted = True
                        else:
                            click.echo("Teardown aborted. Please resolve the issue and try again.")
                            return

        teardown_services(export_to_s3=export_attempted, s3_bucket_name=bucket_name)
    else:
        teardown_services(export_to_s3=False)