import os
from flask import Flask
from .extensions import db, migrate, celery


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    # Load the default configuration
    app.config.from_object('config.default')

    # Load the configuration from the instance folder
    app.config.from_pyfile('config.py')

    # Load the file specified by the APP_CONFIG_FILE environment variable
    # Variables defined here will override those in the default configuration
    # app.config.from_envvar('APP_CONFIG_FILE')
    app.config.from_mapping(SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'swmon.db'))

    db.init_app(app)
    migrate.init_app(app, db)
    init_celery(app)

    from . import views
    views.init_app(app)

    return app


def init_celery(app=None):
    app = app or create_app()
    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend = app.config["CELERY_RESULT_BACKEND"]
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
