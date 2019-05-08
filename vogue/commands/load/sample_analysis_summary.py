import logging
import click
from vogue.load.sample_analysis_summary import load_one, load_all
from flask.cli import with_appcontext, current_app


from genologics.lims import Lims
from genologics.config import BASEURI,USERNAME,PASSWORD
from vogue.constants.constants import RUN_TYPES

LOG = logging.getLogger(__name__)

@click.command("sample_analysis_summary", short_help = "load sample_analysis_summary into db.")
@click.option('-a', '--all', is_flag = True, help = 'Loads all lims samples ids')
@click.option('-s', '--sample-lims-id', help = 'Input sample lims id')
@click.option('--dry', is_flag = True, help = 'Load sample_analysis_summary or not. (dry-run)')

@with_appcontext
def sample_analysis_summary(sample_lims_id, all, dry):
    """fetch sample level data from case analysis colleciton."""

    if all:
        load_all(current_app.adapter)
        return

    load_one(current_app.adapter, sample_lims_id = sample_lims_id) 