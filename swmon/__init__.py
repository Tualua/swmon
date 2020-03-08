import os
from flask import Flask


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    # Load the default configuration
    app.config.from_object('config.default')

    # Load the configuration from the instance folder
    app.config.from_pyfile('config.py')

    # Load the file specified by the APP_CONFIG_FILE environment variable
    # Variables defined here will override those in the default configuration
    app.config.from_envvar('APP_CONFIG_FILE')
    app.config.from_mapping(SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'swmon.db'))

    from .models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from . import views
    views.init_app(app)

    return app
