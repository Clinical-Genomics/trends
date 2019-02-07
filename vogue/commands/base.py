#!/usr/bin/env python
import logging

import click
import coloredlogs

from flask.cli import FlaskGroup, with_appcontext
from flask import current_app

# commands
from vogue.commands.load import load as load_command
from vogue.server import create_app
from .load import load

# Get version and doc decorator
from vogue import __version__
from vogue.tools.cli_utils import add_doc as doc

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOG = logging.getLogger(__name__)

cli = FlaskGroup(create_app=create_app)

@click.group()
def test():
    """Test server using CLI"""
    click.echo("test")
    pass

@cli.command()
@with_appcontext
def name():
    """Returns the app name, for testing purposes, mostly"""
    click.echo(current_app.name)
    return current_app.name

cli.add_command(test)
cli.add_command(load)
test.add_command(name)