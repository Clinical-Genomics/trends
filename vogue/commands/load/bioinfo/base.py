#!/usr/bin/env python
import logging

import click

from mongo_adapter import get_client
from vogue.adapter import VougeAdapter

LOG = logging.getLogger(__name__)

# commands
from vogue.commands.load.bioinfo.bioinfo_raw import bioinfo_raw as bioinfo_raw_command 
from vogue.commands.load.bioinfo.bioinfo_process import bioinfo_process as bioinfo_process_command 
from vogue.commands.load.bioinfo.bioinfo_sample import bioinfo_sample as bioinfo_sample_command 

# Get version and doc decorator
from vogue import __version__
from vogue.tools.cli_utils import add_doc as doc

@click.group()
@click.version_option(version=__version__)
@doc("Vogue {version}: A trending package".format(version=__version__))
def bioinfo():
    """Main entry point of load commands"""
    pass

bioinfo.add_command(bioinfo_raw_command)
bioinfo.add_command(bioinfo_process_command)
bioinfo.add_command(bioinfo_sample_command)
