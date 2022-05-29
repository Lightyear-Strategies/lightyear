from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os

import flask_app.scripts.config as config
from flask_app.scripts.utils import make_celery
from flask_app.scripts.googleAuth import g_oauth

def create_app():
    app = Flask(__name__, template_folder=os.path.join(config.FLASK_DIR, '../HTML'))
    app.register_blueprint(g_oauth)

    app.secret_key = config.FLASK_SECRET_KEY #used in upload forms ?

    os.makedirs(config.UPLOAD_DIR, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_DIR

    from kombu.utils.url import quote
    app.config['CELERY_BROKER_URL'] = \
        'sqs://{AWS_ACCESS_KEY_ID}:{AWS_SECRET_ACCESS_KEY}@sqs.ca-central-1.amazonaws.com/453725380860/FlaskAppSQS-1'.format(
                                        AWS_ACCESS_KEY_ID=quote(config.AWS_ACCESS_KEY_ID, safe=''),
                                        AWS_SECRET_ACCESS_KEY=quote(config.AWS_SECRET_ACCESS_KEY, safe='')
                                       )
    app.config['BROKER_TRANSPORT_OPTIONS'] = {"region": "ca-central-1"}

    # To work with Celery in local environment using RabbitMQ, uncomment app.config below and comment our the two above
    #app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost:5672/'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(config.FLASK_DIR, '../HarosDB.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    celery = make_celery(app)
    bootstrap = Bootstrap(app)
    db = SQLAlchemy(app)
    db.create_all()

    return app, celery, bootstrap, db