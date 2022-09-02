import sys, os, logging
from flask import Flask


def create_app(config="DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object("datawarehouse.config." + config)

    with app.app_context():
        # declaring routes
        # from datawarehouse

        # register blueprints here
        # from datawarehouse.blueprints import ...

        return app
