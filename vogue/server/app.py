# encoding: utf-8
import coloredlogs

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask

from vogue.server import extentions

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

def main():
    app.debug = True
    #toolbar = DebugToolbarExtension(app)
    app.run(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    main()

app = create_app()

from vogue.server import views
