from flask import Flask
from flask_pymongo import PyMongo
from .config import Config
from .api import api
import logging

mongo = PyMongo()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Register namespaces before handling requests
    from .assets.routes import api as assets_api
    from .rules.routes import api as rules_api
    from .owners.routes import api as owners_api

    api.add_namespace(assets_api, path='/api/assets')
    api.add_namespace(rules_api, path='/api/rules')
    api.add_namespace(owners_api, path='/api/owners')

    api.init_app(app)

    return app
