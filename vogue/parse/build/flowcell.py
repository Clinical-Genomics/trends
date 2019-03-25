from vogue.constants.constants import LANE_UDFS
import numpy as np
import datetime as dt
import math

def filter_none(mongo_dict):
    """Function to filter out Nones and NaN from a dict."""
    for key in list(mongo_dict.keys()):
        val = mongo_dict[key]
        if isinstance(val,(dict, str, dt.datetime)):
            continue
        if val is None or math.isnan(val):
            mongo_dict.pop(key)
    return mongo_dict


def run_data(run):
    """Function to get run info from lanes in a lims sequecing process.
    Reformates the data to be part of a document in the flowcell database.
    
    Arguments:
        run (Process): lims Process instance of sequencing type
    Returns: 
        lane_data (dict): run info per lane. 
            eq: {'Lane 1': {'% Aligned R2': 0.94, '% Bases >=Q30 R1': 90.67, '% Bases >=Q30 R2': 88.84,...}, 
                'Lane 2': {'% Aligned R2': 0.92, '% Bases >=Q30 R1': 91.67, '% Bases >=Q30 R2': 83.84,...}}
        avg_data (dict): average run info over all lanes. 
            eg: {'% Phasing R2': 0.09, '% Bases >=Q30': 89.755, ...}
        """
    lane_data = {}
    avg_data = {}

    for lane in run.all_outputs():
        name=lane.name
        if not 'Lane' in name.split():
            lane = lane.input_artifact_list()[0]
            if not lane.location:
                continue
            name = lane.location[1]

        lane_data[name] ={}
        for udf in LANE_UDFS:
            value = lane.udf.get(udf)
            lane_data[name][udf] = value
            if not avg_data.get(udf):
                avg_data[udf] = []
            if isinstance(value, int) or isinstance(value, float):
                avg_data[udf].append(value)

    for udf, values in avg_data.items():
        avg_data[udf]= round(np.mean(values),2)

    q30_r1 = '% Bases >=Q30 R1'
    q30_r2 = '% Bases >=Q30 R2'
    if q30_r1 in avg_data.keys() and  q30_r2 in avg_data.keys():
        Q30 = np.mean([avg_data[q30_r1],avg_data[q30_r2]])
        avg_data.pop(q30_r1)
        avg_data.pop(q30_r2)
        avg_data['% Bases >=Q30'] = Q30

    return lane_data, avg_data 