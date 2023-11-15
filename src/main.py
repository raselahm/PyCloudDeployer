import click
# Import setup functions from aws_services
from aws_services.dynamodb_setup import setup_dynamodb
from aws_services.iam_setup import create_lambda_execution_role  # Import for IAM role creation
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
    lambda_role_arn = create_lambda_execution_role()  # Create IAM role for Lambda
    # Future integration for Lambda deployment will use lambda_role_arn
    click.echo("AWS services deployed successfully.")

cli.add_command(adduser)
cli.add_command(uploadcsv)
cli.add_command(deletecsv)
cli.add_command(deleteuser)

if __name__ == '__main__':
    cli()


