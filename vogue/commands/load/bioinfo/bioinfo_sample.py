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
from vogue.build.bioinfo_analysis import build_analysis
from vogue.build.bioinfo_analysis import build_bioinfo_sample
from vogue.load.bioinfo_analysis import load_analysis
from vogue.parse.load.bioinfo_analysis import inspect_analysis_result
import vogue.models.case_analysis as analysis_model

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOG = logging.getLogger(__name__)

@click.command("sample", short_help="Process stats and results from bioinfo process and load sample info in DB.")
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
def bioinfo_sample(dry, analysis_type, analysis_case,
             analysis_workflow, workflow_version,
             case_analysis_type):

    current_processed_analysis = current_app.adapter.bioinfo_processed(analysis_case)
    LOG.info("Loading following samples to bioinfo_samples: %s",
             ", ".join(current_processed_analysis['samples']))

    for sample in current_processed_analysis['samples']:
        sample_analysis = build_bioinfo_sample(analysis_dict=current_processed_analysis,
                process_case=True, sample_id=sample)
        load_res = load_analysis(adapter=current_app.adapter,
                      lims_id=sample,
                      processed=True,
                      is_sample=True,
                      dry_run=dry,
                      analysis=sample_analysis)
        if load_res:
            LOG.info("Sample %s is loaded into database", sample)
        else:
            LOG.warning("Loading failed for sample %s", sample)
