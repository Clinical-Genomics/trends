

def get_sample_summary_data(sample_id, adapter):

    latest_mip_pipe  = [{
            '$match': {
                '_id': sample_id}
            }, {
            '$unwind': {
                'path': '$cases.livingox.mip'}
            }, {
            '$project': {
            '_id': '$cases.livingox.mip.added', 
            'latest_mip': '$cases.livingox.mip'}
            }, {
            '$sort': {'_id': -1}
            }]

    aggregate_results = adapter.sample_analysis_aggregate(latest_mip_pipe)
  
    if not aggregate_results:
        return None
    try:
        aggregate_result = next(aggregate_results)
    except:
        return

    latest_mip = aggregate_result.get('latest_mip')
    multiqc_picard_insertSize = latest_mip.get('multiqc_picard_insertSize')
    multiqc_picard_HsMetrics = latest_mip.get('multiqc_picard_HsMetrics')

    mip_latest_insert_size = multiqc_picard_insertSize.get('MEDIAN_INSERT_SIZE')
    mip_latest_pct_target = [(k, multiqc_picard_HsMetrics[k]) for k in multiqc_picard_HsMetrics if k.find('PCT_TARGET_BASES') != -1]

    sample = {'mip_latest_insert_size': mip_latest_insert_size,
            'mip_latest_pct_target':mip_latest_pct_target,
            'latest_mip': latest_mip}

    return sample