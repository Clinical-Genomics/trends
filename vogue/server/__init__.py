
import os
import logging
import ruamel.yaml

from flask import Flask
from pymongo import MongoClient

from vogue.adapter.plugin import VougeAdapter
from vogue.server.views import blueprint

from genologics.lims import Lims
from genologics.config import BASEURI,USERNAME,PASSWORD

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)




def create_app():
    return Flask(__name__)

def configure_app(app, config):
    try:
        app.lims = Lims(BASEURI,USERNAME,PASSWORD)
    except:
        app.lims = None
    configurations = ruamel.yaml.safe_load(config) if config else {}
    app.config = {**app.config, **configurations}
    client = MongoClient(app.config['DB_URI'])
    db_name = app.config['DB_NAME']
    app.client = client
    app.db = client[db_name]
    app.adapter = VougeAdapter(client, db_name = db_name)
    app.register_blueprint(blueprint)

    if app.config['DEBUG']==1:
        from flask_debugtoolbar import DebugToolbarExtension
        toolbar = DebugToolbarExtension(app)

    return app
