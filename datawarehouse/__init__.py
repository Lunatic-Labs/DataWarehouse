import sys, os, logging
from flask import Flask

from datawarehouse.controller import register_blueprints

# This is a function that flask will run implicitly to start the application.
# This follows the application factory pattern, read more about it here:
# https://flask.palletsprojects.com/en/2.2.x/patterns/appfactories/
def create_app(config="DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object("datawarehouse.config.config." + config)

    with app.app_context():
        # declaring routes
        # from datawarehouse

        # register blueprints here
        # from datawarehouse.blueprints import ...
        register_blueprints(app)
        return app
