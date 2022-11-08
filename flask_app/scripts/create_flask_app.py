from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

from flask_app.scripts.config import Config
from flask_app.scripts.googleAuth import g_oauth


##########################################
########### app created below ###########
##########################################

login_manager = LoginManager()
bootstrap = Bootstrap()
db = SQLAlchemy()


def init_celery(app):
    celery = Celery(
        app.import_name,
        backend=Config.DATABASE_URI, # app.config['CELERY_BACKEND'],
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

    app.secret_key = Config.FLASK_SECRET_KEY
    app.config['UPLOAD_FOLDER'] = Config.UPLOAD_DIR

    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app = set_broker(app, where)

    return app


def set_broker(app,where='server'):
    if where == 'server':
        app.config['CELERY_BROKER_URL'] = Config.CELERY_BROKER_URL
        app.config['BROKER_TRANSPORT_OPTIONS'] = Config.BROKER_TRANSPORT_OPTIONS

    if where == 'local':
        # To work with Celery in local environment using RabbitMQ
        app.config['CELERY_BROKER_URL'] = Config.CELERY_BROKER_URL

    return app


def create_app(where='server'):
    app = Flask(__name__, template_folder=Config.HTML_DIR, static_folder=Config.STATIC_DIR)
    app = add_configs(app,where)

    login_manager.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


# Always Created
# either use 'local' or 'server'
app = create_app(where=Config.ENVIRONMENT)