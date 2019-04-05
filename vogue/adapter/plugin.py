import logging

from mongo_adapter import MongoAdapter
from datetime import datetime as dt
LOG = logging.getLogger(__name__)


class VougeAdapter(MongoAdapter):

    def setup(self, db_name : str):
        """Setup connection to a database"""

        if self.client is None:
            raise SyntaxError("No client is available")
        self.db = self.client[db_name]
        self.db_name = db_name
        self.sample_collection = self.db.sample
        self.analysis_collection = self.db.analysis
        self.app_tag_collection = self.db.application_tag
        self.flowcell_collection = self.db.flowcell
        
        LOG.info("Use database %s.", db_name)

    def add_or_update_sample(self, sample_news: dict):
        """Adds/updates a sample in the database"""

        lims_id = sample_news['_id']
        update_result = self.db.sample.update_one({'_id' : lims_id}, {'$set': sample_news}, upsert=True)

        if not update_result.raw_result['updatedExisting']:
            self.db.sample.update_one({'_id' : lims_id}, 
                {'$set': {'added': dt.today()}})
            LOG.info("Added sample %s.", lims_id)
        elif update_result.modified_count:
            self.db.sample.update_one({'_id' : lims_id}, 
                {'$set': {'updated': dt.today()}})
            LOG.info("Updated sample %s.", lims_id)
        else:
            LOG.info("No updates for sample %s.", lims_id)

    def add_or_update_run(self, run_news: dict):
        """Adds/updates a flowcell in the database"""

        lims_id = run_news['_id']
        update_result = self.db.flowcell.update_one({'_id' : lims_id}, {'$set': run_news}, upsert=True)

        if not update_result.raw_result['updatedExisting']:
            self.db.flowcell.update_one({'_id' : lims_id}, 
                {'$set': {'added': dt.today()}})
            LOG.info("Added flowcell %s.", lims_id)
        elif update_result.modified_count:
            self.db.flowcell.update_one({'_id' : lims_id}, 
                {'$set': {'updated': dt.today()}})
            LOG.info("Updated flowcell %s.", lims_id)
        else:
            LOG.info("No updates for flowcell %s.", lims_id)

    def add_or_update_application_tag(self, application_tag_news: dict):
        """Adds/updates a application_tag in the database"""

        tag = application_tag_news['_id']
        update_result = self.db.application_tag.update_one({'_id' : tag}, 
                            {'$set': application_tag_news}, upsert=True)

        if not update_result.raw_result['updatedExisting']:
            self.db.application_tag.update_one({'_id' : tag}, {'$set': {'added': dt.today()}})
            LOG.info("Added application_tag %s.", tag)
        elif update_result.modified_count:
            self.db.application_tag.update_one({'_id' : tag}, {'$set': {'updated': dt.today()}})
            LOG.info("Updated application_tag %s.", tag)
        else:
            LOG.info("No updates for application_tag %s.", tag)

    def sample(self, lims_id):
        return self.sample_collection.find_one({'_id':lims_id})

    def flowcell(self, run_id):
        return self.flowcell_collection.find_one({'_id':run_id})

    def app_tag(self, tag):
        return self.app_tag_collection.find_one({'_id':tag})

    def delete_sample(self):
        return None

    def add_or_update_analysis(self, analysis_result: dict):
        """Functionality to add or update analysis sample"""
        lims_id = analysis_result['_id']
        update_result = self.db.analysis.update_one({'_id' : lims_id}, {'$set': analysis_result}, upsert=True)

        if not update_result.raw_result['updatedExisting']:
            self.db.analysis.update_one({'_id' : lims_id}, 
                {'$set': {'added': dt.today()}})
            LOG.info("Added analysis sample %s.", lims_id)
        elif update_result.modified_count:
            self.db.analysis.update_one({'_id' : lims_id}, 
                {'$set': {'updated': dt.today()}})
            LOG.info("Updated analysis for sample %s.", lims_id)
        else:
            LOG.info("No analysis updates for sample %s.", lims_id)

    def analysis(self, analysis_id: str):
        """Functionality to get analyses results"""
        return self.analysis_collection.find_one({'_id':analysis_id})
        
    def find_samples(self, query:dict)-> list:
        """Function to find samples in samples collection based on query"""
        samples = self.sample_collection.find(query)
        return list(samples)

    def samples_aggregate(self, pipe : list):
        """Function to make a aggregation on the sample colleciton"""
        return self.sample_collection.aggregate(pipe)

    def flowcells_aggregate(self, pipe : list):
        """Function to make a aggregation on the flowcell colleciton"""
        return self.flowcell_collection.aggregate(pipe)

    def get_category(self, app_tag):
        """Function get category based on application tag from the application tag collection"""
        tag = self.app_tag_collection.find_one({'_id' : app_tag} , { "category": 1 })
        return tag.get('category') if tag else None
