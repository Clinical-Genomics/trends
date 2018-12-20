from mongo_adapter import get_client
from vogue.adapter.plugin import VougeAdapter

class ConfiguredVogueAdapter(VougeAdapter):

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        client = get_client(uri = app.config['MONGO_URI'])
        adapter = super().__init__(client, db_name = app.config['MONGO_DBNAME'])

adapter = ConfiguredVogueAdapter()
