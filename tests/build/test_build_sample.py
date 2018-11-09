from vogue.load.lims import build_sample

def test_build_sample(lims_sample):
    ## GIVEN a lims sample
    ## WHEN building a mongo sample
    mongo_sample = build_sample(lims_sample)
    ## THEN the sample should have been parsed in the correct way
    assert mongo_sample['lims_id'] == lims_sample.id

def test_build_sample_family(sample):
    ## GIVEN a lims sample with a family
    ## WHEN building a mongo sample
    mongo_sample = build_sample(sample)
    ## THEN the sample should have been parsed in the correct way
    assert mongo_sample['family'] == sample.udf.get('Family')


def test_build_received_date(sample):
    ## GIVEN a lims sample
    ## WHEN building a mongo sample
    mongo_sample = build_sample(sample)
    ## THEN the sample should ..
    