import logging
import copy
import click

from flask.cli import with_appcontext, current_app
from flask import abort as flaskabort

from vogue.tools.cli_utils import json_read
from vogue.tools.cli_utils import dict_replace_dot
from vogue.tools.cli_utils import yaml_read
from vogue.tools.cli_utils import check_file
from vogue.tools.cli_utils import concat_dict_keys
from vogue.tools.cli_utils import add_doc as doc
from vogue.tools.cli_utils import recursive_default_dict
from vogue.tools.cli_utils import convert_defaultdict_to_regular_dict
from vogue.build.case_analysis import build_analysis
from vogue.build.case_analysis import build_bioinfo_sample
from vogue.load.case_analysis import load_analysis
from vogue.parse.load.case_analysis import validate_conf
import vogue.models.case_analysis as analysis_model

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOG = logging.getLogger(__name__)

@click.command("sample", short_help="Process stats and results from bioinfo process and load sample info in DB.")
@click.option('--sample-list',
              help='Input list of comma separated sample names.')
@click.option('-a',
              '--analysis-result',
              type=click.Path(),
              multiple=True,
              help='Input file for bioinfo analysis results. Accepted format: JSON, YAML')
@click.option(
    '-t',
    '--analysis-type',
    type=click.Choice(list(analysis_model.ANALYSIS_DESC.keys()) + ['all']),
    multiple=True,
    default=['all'],
    help='Type of analysis results to load.')
@click.option('-c',
              '--analysis-case',
              required=True,
              help='''The case that this sample belongs.
        It can be specified multiple times.''')
@click.option('-w',
              '--analysis-workflow',
              type=click.Choice(['mip','balsamic','microsalt']),
              required=True,
              help='Analysis workflow used.')
@click.option('--workflow-version',
              required=True,
              help='Analysis workflow used.')
@click.option(
    '--processed/--not-processed',
    is_flag=True,
    help=
    'Specify this flag if input json should be processed and to be added to bioinfo_processed.'
)
@click.option(
    '--cleanup/--not-cleanup',
    is_flag=True,
    help=
    'Specify this flag if input json should be cleanup based on analysis-type and models.'
)
@click.option('--load-sample/--not-load-sample',
              is_flag=True,
              default=True,
              help='Specify this flag to load samples during loading processed')
@click.option(
    '--case-analysis-type',
    type=click.Choice(['multiqc', 'microsalt', 'custom']),
    default='multiqc',
    help=
    'Specify the type for the case analysis. i.e. if it is multiqc output, then choose multiqc'
)
@click.option('--dry', is_flag=True, help='Load from sample or not. (dry-run)')
@doc(f"""
    Read and load analysis results. These are either QC or analysis output files.

    The inputs are unique ID with an analysis config file (JSON/YAML) which includes analysis results matching the
    analysis model. Analysis types recognize the following keys in the input file: {" ".join(concat_dict_keys(analysis_model.ANALYSIS_SETS,key_name=""))}
        """)
@with_appcontext
def bioinfo_sample(dry, analysis_result, analysis_type, analysis_case,
             analysis_workflow, workflow_version, processed,
             case_analysis_type, sample_list, cleanup, load_sample):
    pass
