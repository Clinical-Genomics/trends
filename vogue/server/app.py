# encoding: utf-8
import coloredlogs
from flask import Flask
from . import extentions

def create_app():
    """Generate a flask application."""
    app = Flask(__name__, template_folder='templates')

    # load config
    app.config.from_object(__name__.replace('app', 'config'))

    configure_extensions(app)

    return app


def configure_extensions(app: Flask):
    """Configure extensions and logging"""
    coloredlogs.install(level='DEBUG' if app.debug else 'INFO')

    extentions.adapter.init_app(app)
