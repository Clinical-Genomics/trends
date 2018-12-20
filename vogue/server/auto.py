# encoding: utf-8
from flask_debugtoolbar import DebugToolbarExtension

from .app import create_app

app = create_app()

from . import views

def main():
    app.debug = True
    #toolbar = DebugToolbarExtension(app)
    app.run(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    main()
