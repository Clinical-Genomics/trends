from vogue.build.sample_analysis_summary import build_sample_analysis_summary
from vogue.constants.constants import RUN_TYPES, INSTRUMENTS
import logging
LOG = logging.getLogger(__name__)



def load_one(adapter, sample_lims_id):
    """Function to load analysis date for one lims sample from the case collection 
    into the sample_analysis_summary"""

    mongo_sample_analysis_summary = build_sample_analysis_summary(sample_lims_id, adapter)
    if mongo_sample_analysis_summary:
        adapter.add_or_update_sample_analysis_summary(mongo_sample_analysis_summary)


def load_all(adapter):
    """Function to load all samples"""
    for sample in adapter.sample_collection.find():
        load_one(adapter, sample.get('_id'))