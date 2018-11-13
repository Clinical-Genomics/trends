from genologics.lims import Lims
from genologics.entities import Sample, Artifact

from datetime import datetime as dt
import operator
import logging
LOG = logging.getLogger(__name__)


def str_to_datetime(date: str)-> dt:
    if date is None:
        return None
    return dt.strptime(date, '%Y-%m-%d')

PROCESS = {
    'sequenced': {
        'process_types': [
                     'CG002 - Illumina Sequencing (HiSeq X)', 
                     'CG002 - Illumina Sequencing (Illumina SBS)'
                 ],
        'udf': None,
        'sample_udf': 'Passed Sequencing QC',
        'operator': max
    },
    'received': {
        'process_types': [
            'CG002 - Reception Control'
        ],
        'udf': 'date arrived at clinical genomics',
        'parent_process': True,
    },
    'prepared': {
        'process_types': [
                     'CG002 - Aggregate QC (Library Validation)'
                 ],
        'udf': None,
        'operator': max,
    },
    'delivery': {
        'process_types': [
                     'CG002 - Delivery'
                 ],
        'udf': 'Date delivered',
        'parent_process': True,
        'operator': min,
        'warn_if_many': True,
    }
    
}

def get_process_date(sample: Sample, lims: Lims, process: str)-> dt:
    """Get dates for a certain kind of process
    
    Args:
        sample(Sample): A Lims Sample object
        lims(Lims): A connection to the Lims database
        process(str): What type of process should be checked
    
    Returns:
        date(datetime.datetime): The relevant date or None
    """
    try:
        process_info = PROCESS[process]
    except KeyError as err:
        LOG.error("Process %s does not exist", process)
        raise SyntaxError(err.message)

    # Each process will have one or more process types
    # These are used to search the correct artifacts
    process_types = process_info['process_types']
    # Some process have a udf
    udf = process_info['udf']
    # Some process require that we look at the parent process of the artifacts
    parent_process = process_info.get('parent_process')
    # If there are multiple dates we need to know which one to return
    operator = process_info.get('operator', min)
    
    # If we need to check sample udfs
    if process_info.get('sample_udf'):
        sample_udfs = sample.udf.get(process_info['sample_udf'])
        # If there where no sample udf of the relevant type we return None
        if not sample_udfs:
            return None
    
    # Get all artifacts for a sample and the relevant process type(s)
    artifacts = lims.get_artifacts(process_type = process_types, samplelimsid = sample.id)
    
    date = None
    dates = []
    for art in artifacts:
        if not art.parent_process:
            continue
        if parent_process:
            # Check if there are relevant udfs for the parent
            parent_udf = artifact.parent_process.udf.get(udf)
            if not parent_udf:
                continue
            # Get the date of these
            dates.append(str_to_datetime(parent_udf.isoformat()))
            continue

        dates.append(str_to_datetime(art.parent_process.date_run))
    
    if dates:
        if (process_info.get('warn_if_many') and len(dates) > 1):
            LOG.warning("Multiple % days found for: %s.", process_type, sample.id)
            

        date = operator(dates)
    
    return date

def get_number_of_days(first_date: dt, second_date : dt) -> int:
    """Get number of days between different time stamps."""

    days = None
    if first_date and second_date:
        time_span = second_date - first_date
        days = time_span.days

    return days

def _get_latest_output_artifact(process_type: str, lims_id: str, lims: Lims) -> Artifact:
    """Returns the output artifact related to lims_id and the step that was latest run."""

    latest_output_artifact = None
    artifacts = lims.get_artifacts(samplelimsid = lims_id, process_type = process_type)
    # Make a list of tuples (<date the artifact was generated>, <artifact>): 
    date_art_list = list(set([(a.parent_process.date_run, a) for a in artifacts]))

    if date_art_list:
        #Sort on date:
        date_art_list.sort(key = operator.itemgetter(0)) 
        #Get latest:
        dummy, latest_output_artifact = date_art_list[-1] 

    return latest_output_artifact


def _get_latest_input_artifact(process_type: str, lims_id: str, lims: Lims) -> Artifact:
    """Returns the input artifact related to lims_id and the step that was latest run."""

    latest_input_artifact = None
    artifacts = lims.get_artifacts(samplelimsid = lims_id, process_type = process_type) 
    # Make a list of tuples (<date the artifact was generated>, <artifact>): 
    date_art_list = list(set([(a.parent_process.date_run, a) for a in artifacts]))

    if date_art_list:
        #Sort on date:
        date_art_list.sort(key = operator.itemgetter(0))
        #Get latest:
        dummy, latest_outart = date_art_list[-1] #get latest
        #Get the input artifact related to our sample
        for inart in latest_outart.input_artifact_list():
            if lims_id in [sample.id for sample in inart.samples]:
                latest_input_artifact = inart 
                break        

    return latest_input_artifact


def get_concentration_and_nr_defrosts(application_tag: str, lims_id: str, lims: Lims) -> dict:
    """Get concentration and nr of defrosts for wgs illumina PCR-free samples.

    Find the latest artifact that passed through a concentration_step and get its 
    concentration_udf. --> concentration
    Go back in history to the latest lot_nr_step and get the lot_nr_udf from that step. --> lotnr
    Find all steps where the lot_nr was used. --> all_defrosts
    Pick out those steps that were performed before our lot_nr_step --> defrosts_before_this_process
    Count defrosts_before_this_process. --> nr_defrosts"""

    if not application_tag[0:6] in ['WGSPCF', 'WGTPCF']:
        return {}

    lot_nr_step = 'CG002 - End repair Size selection A-tailing and Adapter ligation (TruSeq PCR-free DNA)'
    concentration_step = 'CG002 - Aggregate QC (Library Validation)'
    lot_nr_udf = 'Lot no: TruSeq DNA PCR-Free Sample Prep Kit'
    concentration_udf = 'Concentration (nM)'

    return_dict = {}
    concentration_art = _get_latest_input_artifact(concentration_step, lims_id, lims)

    if concentration_art:
        concentration = concentration_art.udf.get(concentration_udf)
        lotnr = concentration_art.parent_process.udf.get(lot_nr_udf)
        this_date = str_to_datetime(concentration_art.parent_process.date_run)

        # Ignore if multiple lot numbers:
        if lotnr and len(lotnr.split(',')) == 1 and len(lotnr.split(' ')) == 1:
            all_defrosts = lims.get_processes(type = lot_nr_step, udf = {lot_nr_udf : lotnr})
            defrosts_before_this_process = []

            # Find the dates for all processes where the lotnr was used (all_defrosts),
            # and pick the once before or equal to this_date
            for defrost in all_defrosts:  
                if str_to_datetime(defrost.date_run) <= this_date:
                    defrosts_before_this_process.append(defrost)

            nr_defrosts = len(defrosts_before_this_process)

            return_dict = {'nr_defrosts' : nr_defrosts, 'concentration' : concentration, 
                            'lotnr' : lotnr}

    return return_dict


def get_final_conc_and_amount_dna(application_tag: str, lims_id: str, lims: Lims) -> dict:
    """Find the latest artifact that passed through a concentration_step and get its 
    concentration. Then go back in history to the latest amount_step and get the amount."""

    if not application_tag[0:6] in ['WGSLIF', 'WGTLIF']:
        return {}

    return_dict = {}
    amount_udf = 'Amount (ng)'
    concentration_udf = 'Concentration (nM)'
    concentration_step = 'CG002 - Aggregate QC (Library Validation)'
    amount_step = 'CG002 - Aggregate QC (DNA)'

    concentration_art = _get_latest_input_artifact(concentration_step, lims_id, lims)

    if concentration_art:
        amount_art = None
        step = concentration_art.parent_process
        # Go back in history untill we get to an output artifact from the amount_step
        while step and not amount_art:
            art = _get_latest_input_artifact(step.type.name, lims_id, lims)
            if amount_step in [p.type.name for p in lims.get_processes(inputartifactlimsid=art.id)]:
                amount_art = art
            step = art.parent_process
        
        amount = amount_art.udf.get(amount_udf) if amount_art else None
        concentration = concentration_art.udf.get(concentration_udf)
        return_dict = {'amount' : amount, 'concentration':concentration}

    return return_dict


def get_microbial_library_concentration(application_tag: str, lims_id: str, lims: Lims) -> float:
    """Check only samples with mictobial application tag.
    Get concentration_udf from concentration_step."""

    if not application_tag[3:5] == 'NX':
        return None

    concentration_step = 'CG002 - Aggregate QC (Library Validation)'
    concentration_udf = 'Concentration (nM)'

    concentration_art = _get_latest_input_artifact(concentration_step, lims_id, lims)

    if concentration_art:
        return concentration_art.udf.get(concentration_udf)
    else:
        return None



# The following two functions will get the udf Size (bp) that in fact is set on the 
# aggregate qc librar validation step.
# But since the same qc protocol is used both for pre-hyb and post-hyb, there is no way to 
# distiguish from within the aggregation step, wether it is pre-hyb or post-hyb qc. 
# Because of that, we instead look for the inpus atrifact to the aggregation step. 
# For pre hyb, the input artifact will come from 'CG002 - Amplify Adapter-Ligated Library (SS XT)'. 
# For post hyb, it will come from 'CG002 - Amplify Captured Libraries to Add Index Tags (SS XT)'.

def get_library_size_pre_hyb(application_tag: str, lims_id: str, lims: Lims) -> int:
    """Check only 'Targeted enrichment exome/panels'.
    Get size_udf from size_step."""

    if not application_tag[0:3] in ['EXO', 'EFT', 'PAN']:
        return None

    size_step = 'CG002 - Amplify Adapter-Ligated Library (SS XT)'
    size_udf = 'Size (bp)'

    size_art = _get_latest_output_artifact(size_step, lims_id, lims)

    if size_art:
        return size_art.udf.get(size_udf)
    else:
        None


def get_library_size_post_hyb(application_tag: str, lims_id: str, lims: Lims) -> int:
    """Check only 'Targeted enrichment exome/panels'.
    Get size_udf from size_step."""

    if not application_tag[0:3] in ['EXO', 'EFT', 'PAN']:
        return None

    size_step = 'CG002 - Amplify Captured Libraries to Add Index Tags (SS XT)'
    size_udf = 'Size (bp)'

    size_art = _get_latest_output_artifact(size_step, lims_id, lims)

    if size_art:
        return size_art.udf.get(size_udf)
    else:
        return None
