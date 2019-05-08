
from vogue.parse.sample_analysis_summary import get_sample_summary_data


def build_sample_analysis_summary(sample_id, adapter)-> dict:
    """Parse lims sample"""
    
    sample = get_sample_summary_data(sample_id, adapter)
    if not sample:
        return

    mongo_sample = {'_id' : sample_id}
    mongo_sample['mip_latest_insert_size'] = sample['mip_latest_insert_size']
    mongo_sample['mip_latest_pct_target'] = sample['mip_latest_pct_target']
    mongo_sample['latest_mip'] = sample['latest_mip']

    for key in list(mongo_sample.keys()):
        if mongo_sample[key] is None:
            mongo_sample.pop(key)

    return mongo_sample
