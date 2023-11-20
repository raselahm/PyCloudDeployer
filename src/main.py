import click
import time
from aws_services.dynamodb_setup import setup_dynamodb
from aws_services.iam_setup import create_lambda_execution_role
from aws_services.lambda_setup import deploy_all_lambda_functions
from aws_services.cloudwatch_setup import setup_cloudwatch_event
from aws_services.ses_setup import setup_ses
from cli.commands import adduser, uploadcsv, deletecsv, deleteuser, settriggertime, setupses, validate_email as validate_email_command, teardown

@click.group()
def cli():
    """PyCloudDeployer: A tool to deploy AWS services for birthday email automation."""
    pass

@cli.command()
def deployservices():
    """Deploy necessary AWS services."""
    click.echo("Deploying AWS services...")
    setup_dynamodb()
    lambda_role_arn = create_lambda_execution_role()

    # Deploy all lambda functions and get their ARNs
    birthday_email_function_arn, email_verification_function_arn = deploy_all_lambda_functions(lambda_role_arn)

    # Wait for a longer time to ensure Lambda functions are available
    time.sleep(60)

    # Set up CloudWatch event for the birthday email function
    setup_cloudwatch_event(birthday_email_function_arn)

    # Prompt for email
    email = click.prompt("Please enter your email for SES", type=str)
    # Validate email
    if not validate_email_command(None, None, email):
        click.echo("Invalid email format.")
        return

    setup_ses(email)
    click.echo("AWS services deployed successfully.")

cli.add_command(adduser)
cli.add_command(uploadcsv)
cli.add_command(deletecsv)
cli.add_command(deleteuser)
cli.add_command(settriggertime)
cli.add_command(setupses)
cli.add_command(teardown)

if __name__ == '__main__':
    cli()