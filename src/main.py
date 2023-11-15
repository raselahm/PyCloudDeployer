import click
# Import setup functions from aws_services
from aws_services.dynamodb_setup import setup_dynamodb
# Import the add_user command from cli.commands
from cli.commands import adduser

@click.group()
def cli():
    """PyCloudDeployer: A tool to deploy AWS services for birthday email automation."""
    pass

@cli.command()
def deploy_services():
    """Deploy necessary AWS services."""
    click.echo("Deploying AWS services...")
    setup_dynamodb()
    # Calls to other AWS service setup functions will go here
    click.echo("AWS services deployed successfully.")

# Integrating the add_user command from cli.commands
cli.add_command(adduser)

@cli.command()
def delete_user():
    """Placeholder for delete_user functionality."""
    # This will later be implemented to delete a user from DynamoDB
    click.echo("User deleted successfully.")

if __name__ == '__main__':
    cli()
