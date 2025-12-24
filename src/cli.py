import click

from commands.database import database

from log import setup_logging

@click.group()
def cli():
    pass



cli.add_command(database)

if __name__ == '__main__':
    setup_logging()
    cli()