# encoding: utf-8
import os

# flask
TEMPLATES_AUTO_RELOAD = True

# server
CG_ENABLE_ADMIN = ('FLASK_DEBUG' in os.environ)

# mongo
MONGO_URI = os.environ['MONGO_URI']
MONGO_DB_NAME = os.environ['MONGO_DB_NAME']
