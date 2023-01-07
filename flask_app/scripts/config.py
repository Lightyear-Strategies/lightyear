import os
# from kombu.utils.url import quote    # To work with AWS SQS
from dotenv import load_dotenv

load_dotenv()


class Config:
    SCRIPTS_DIR = os.path.abspath(os.path.dirname(__file__))
    FLASK_DIR = os.path.dirname(SCRIPTS_DIR)
    LIGHTYEAR_DIR = os.path.dirname(FLASK_DIR)
    CONFIG_DIR = os.path.join(FLASK_DIR, 'configs')
    HTML_DIR = os.path.join(FLASK_DIR, 'HTML')
    STATIC_DIR = os.path.join(HTML_DIR, 'static')
    UPLOAD_DIR = os.path.join(FLASK_DIR, 'uploadFolder')
    REPORTS_DIR = os.path.join(FLASK_DIR, 'scripts/PeriodicWriters/reports/')
    EMAIL_ASSETS_DIR = os.path.join(SCRIPTS_DIR, 'EmailValidator/assets/')
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    EV_API_KEY = os.getenv('EV_API_KEY')
    MIXPANEL_TOKEN = os.getenv('MIXPANEL_TOKEN')

    DATABASE_URI = 'sqlite:///' + os.path.join(FLASK_DIR, 'Database.sqlite3')

    SERVER_NAME = os.getenv('SERVER_NAME')

    SENDER_EMAIL_NAME = '"George Lightyear" <george@lightyearstrategies.com>'

    with open(os.path.join(CONFIG_DIR, 'env.txt')) as e:
        ENVIRONMENT = e.read().strip()

    if ENVIRONMENT == 'server':
        CONTACT_US_RECIPIENTS = ['george@lightyearstrategies.com',
                                 'aleksei@lightyearstrategies.com',
                                 'nima@lightyearstrategies.com']

        CLIENT_SECRET_FILE = os.path.join(CONFIG_DIR, 'web_google_client.json')
        SERVICE_FILE = os.path.join(CONFIG_DIR, 'george.json')
        PICKLE_FILE = os.path.join(CONFIG_DIR, 'server_token.pickle')

        # BROKER_TRANSPORT_OPTIONS = {"region": os.getenv('AWS_REGION')}
        # CELERY_BROKER_URL = 'sqs://{AWS_ACCESS_KEY_ID}:{AWS_SECRET_ACCESS_KEY}' \
        #                         '@sqs.{REGION}.amazonaws.com/{ACCOUNT}/{SERVICE_NAME}' \
        #     .format(
        #     AWS_ACCESS_KEY_ID=quote(os.getenv('AWS_ACCESS_KEY_ID'), safe=''),
        #     AWS_SECRET_ACCESS_KEY=quote(os.getenv('AWS_SECRET_ACCESS_KEY'), safe=''),
        #     REGION=os.getenv('AWS_REGION'),
        #     ACCOUNT=os.getenv('AWS_ACCOUNT'),
        #     SERVICE_NAME=os.getenv('AWS_ACCOUNT')
        # )

    elif ENVIRONMENT == 'local':
        CLIENT_SECRET_FILE = os.path.join(CONFIG_DIR, 'local_google_client.json')
        SERVICE_FILE = os.path.join(CONFIG_DIR, 'george.json')
        PICKLE_FILE = os.path.join(CONFIG_DIR, 'local_token.pickle')
        # CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/'
        CONTACT_US_RECIPIENTS = ['george@lightyearstrategies.com',
                                 'aleksei@lightyearstrategies.com']

    else:
        raise Exception("No proper Enviroment is found")
