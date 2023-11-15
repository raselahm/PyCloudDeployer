import click
import re
from datetime import datetime
from aws_services.user_management.adduser import add_user_to_db
from aws_services.user_management.deleteuser import delete_user
from aws_services.user_management.csvoperations import upload_users_from_csv, delete_users_from_csv

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
    else:
        click.echo('Failed to add user.')

@click.command()
@click.argument('file_path')
def uploadcsv(file_path):
    """Upload users from a CSV file."""
    upload_users_from_csv(file_path)
    click.echo(f"Attempted to upload users from {file_path}.")

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
