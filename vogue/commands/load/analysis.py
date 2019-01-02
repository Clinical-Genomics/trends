import logging

import click

import yaml
import json

from vogue.tools.cli_utils import json_read
from vogue.tools.cli_utils import yaml_read
from vogue.tools.cli_utils import check_file
from vogue.build.analysis import validate_conf

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOG = logging.getLogger(__name__)

@click.command("analysis", short_help = "Read files from analysis workflows")
@click.option(
    '-s',
    '--sample-id',
    required=True,
    help='Input sample id'
)
@click.option(
    '-a',
    '--analysis-config',
    type=click.Path(),
    required=True,
    help='Input config file. Accepted format: JSON, YAML')
@click.pass_context

def analysis(context, sample_id, analysis_config):
    """
    Read and load analysis results. These are either QC or analysis output files.
    """
    LOG.info("Reading and validating config file.")
    try:
        check_file(analysis_config)
    except FileNotFoundError as e:
        context.abort()

    LOG.info("Trying JSON format")
    analysis_dict = json_read(analysis_config)
    if not isinstance(analysis_dict,dict):
        LOG.info("Trying YAML format")
        analysis_dict = yaml_read(analysis_config)
        if not isinstance(analysis_dict,dict):
            LOG.error("Cannot read input analysis config file. Type unknown.")
            context.abort()

    LOG.info("Validating config file")
    if not validate_conf(analysis_dict):
        LOG.error("Input config file is not valid format")
        context.abort()
