'''
    Add or update analysis results for samples from bioinfo_processed into bioinf_sample collection
'''
import logging
import click

from flask.cli import with_appcontext
from flask.cli import current_app

from vogue.tools.cli_utils import add_doc as doc
from vogue.build.bioinfo_analysis import build_bioinfo_sample
from vogue.load.bioinfo_analysis import load_analysis

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOG = logging.getLogger(__name__)


@click.command(
    "sample",
    short_help=
    "Process stats and results from bioinfo process and load sample info in DB."
)
@click.option('-c',
              '--analysis-case',
              required=True,
              help='''The case that this sample belongs.
        It can be specified multiple times.''')
@click.option('--dry', is_flag=True, help='Load from sample or not. (dry-run)')
@doc(f"""
    Load samples analysis results from bioinfo processed collection
    into bioinfo sample collection.
    """)
@with_appcontext
def bioinfo_sample(dry, analysis_case):

    current_processed_analysis = current_app.adapter.bioinfo_processed(
        analysis_case)
    LOG.info("Loading following samples to bioinfo_samples: %s",
             ", ".join(current_processed_analysis['samples']))

    for sample in current_processed_analysis['samples']:
        sample_analysis = build_bioinfo_sample(
            analysis_dict=current_processed_analysis,
            process_case=True,
            sample_id=sample)
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
