import click
import re
from datetime import datetime
from aws_services.user_management.adduser import add_user_to_db

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