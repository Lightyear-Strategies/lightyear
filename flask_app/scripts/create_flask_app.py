from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

import flask_app.scripts.config as config
from flask_app.scripts.googleAuth import g_oauth


##########################################
## app, bootstrap, db initialized below ##
##########################################


def init_app(where='server'):
    app = Flask(__name__, template_folder=config.HTML_DIR)
    app = add_configs(app,where)

    bootstrap = init_bootstrap(app)
    db = init_db(app)

    return app, bootstrap, db


def init_bootstrap(app):
    bootstrap = Bootstrap(app)
    return bootstrap


def init_db(app):
    db = SQLAlchemy(app)
    db.create_all()
    return db


def init_celery(app):
    celery = Celery(
        app.import_name,
        #backend=app.config['CELERY_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def add_configs(app,where):
    app.register_blueprint(g_oauth)

    app.secret_key = config.FLASK_SECRET_KEY
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_DIR

    app = set_broker(app, where)

    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app


def set_broker(app,where='server'):
    if where == 'server':
        app.config['CELERY_BROKER_URL'] = config.CELERY_WEB_BROKER_URL
        app.config['BROKER_TRANSPORT_OPTIONS'] = {"region": config.AWS_REGION}

    if where == 'local':
        # To work with Celery in local environment using RabbitMQ
        app.config['CELERY_BROKER_URL'] = config.CELERY_LOCAL_BROKER_URL

    return app


# Always Created
# either use 'local' or 'server'
app, bootstrap, db = init_app(where='server')