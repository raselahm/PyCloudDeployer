import click
# Import setup functions from aws_services
from aws_services.dynamodb_setup import setup_dynamodb
from aws_services.iam_setup import create_lambda_execution_role  # Import for IAM role creation
from aws_services.lambda_setup import deploy_lambda_function
from aws_services.cloudwatch_setup import setup_cloudwatch_event
# Import commands from cli.commands
from cli.commands import adduser, uploadcsv, deletecsv, deleteuser

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
    deploy_lambda_function(lambda_role_arn)
    setup_cloudwatch_event('BirthdayEmailFunction')  
    click.echo("AWS services deployed successfully.")

cli.add_command(adduser)
cli.add_command(uploadcsv)
cli.add_command(deletecsv)
cli.add_command(deleteuser)

if __name__ == '__main__':
    cli()


