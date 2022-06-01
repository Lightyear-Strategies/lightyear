

##########################################
## app, bootstrap, db initialized below ##
##########################################
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
import os

import flask_app.scripts.config as config
from flask_app.scripts.googleAuth import g_oauth


def init_app(where='server'):
    app = Flask(__name__, template_folder=os.path.join(config.FLASK_DIR, 'HTML'))
    print(os.path.join(config.FLASK_DIR, 'HTML'))
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

    app.secret_key = config.FLASK_SECRET_KEY  # used in upload forms ?

    app.config['UPLOAD_FOLDER'] = config.UPLOAD_DIR

    app = set_broker(app, where)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(config.FLASK_DIR, 'HarosDB.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app


def set_broker(app,where='server'):
    if where == 'server':
        # To work with AWS SQS
        from kombu.utils.url import quote

        app.config['CELERY_BROKER_URL'] = \
            'sqs://{AWS_ACCESS_KEY_ID}:{AWS_SECRET_ACCESS_KEY}@sqs.{region}.amazonaws.com/{account}/{service_name}'\
                .format(
                AWS_ACCESS_KEY_ID=quote(config.AWS_ACCESS_KEY_ID, safe=''),
                AWS_SECRET_ACCESS_KEY=quote(config.AWS_SECRET_ACCESS_KEY, safe=''),
                region='ca-central-1',
                account='453725380860',
                service_name='FlaskAppSQS-1'
            )
        app.config['BROKER_TRANSPORT_OPTIONS'] = {"region": "ca-central-1"}

    if where == 'local':
        # To work with Celery in local environment using RabbitMQ
        app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost:5672/'

    return app


# Always Created

app, bootstrap, db = init_app(where='server')