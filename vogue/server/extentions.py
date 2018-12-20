from mongo_adapter import get_client
from vogue.adapter.plugin import VougeAdapter

class MongoAdapter:

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(app):
        client = get_client(uri = app.config['MONGO_URI'])
        adapter = VougeAdapter(client, db_name = app.config['MONGO_DB_NAME'])

adapter = MongoAdapter()
