import click
# Import setup functions from aws_services
from aws_services.dynamodb_setup import setup_dynamodb
# Import the add_user command from cli.commands
from cli.commands import adduser, uploadcsv, deletecsv

@click.group()
def cli():
    """PyCloudDeployer: A tool to deploy AWS services for birthday email automation."""
    pass

@cli.command()
def deployservices():
    """Deploy necessary AWS services."""
    click.echo("Deploying AWS services...")
    setup_dynamodb()
    click.echo("AWS services deployed successfully.")

cli.add_command(adduser)
cli.add_command(uploadcsv)
cli.add_command(deletecsv)

# Placeholder for delete_user command...

if __name__ == '__main__':
    cli()
