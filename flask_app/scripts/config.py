import os
from kombu.utils.url import quote    # To work with AWS SQS
from dotenv import load_dotenv

load_dotenv()

class Config:
    SCRIPTS_DIR = os.path.abspath(os.path.dirname(__file__))
    FLASK_DIR = os.path.dirname(SCRIPTS_DIR)
    LIGHTYEAR_DIR = os.path.dirname(FLASK_DIR)
    CONFIG_DIR = os.path.join(FLASK_DIR,'configs')
    HTML_DIR = os.path.join(FLASK_DIR, 'HTML')
    UPLOAD_DIR = os.path.join(FLASK_DIR,'uploadFolder')
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    EV_API_KEY = os.getenv('EV_API_KEY')
    DATABASE_URI = 'sqlite:///' + os.path.join(FLASK_DIR, 'Database.sqlite3')

    WEB_CLIENT_SECRETS_FILE = os.path.join(CONFIG_DIR,'web_google_client.json')
    LOCAL_CLIENT_SECRETS_FILE = os.path.join(CONFIG_DIR,'local_google_client.json')
    PICKLE_FILE = os.path.join(CONFIG_DIR,'token.pickle')

    BROKER_TRANSPORT_OPTIONS = {"region":os.getenv('AWS_REGION')}
    CELERY_LOCAL_BROKER_URL = 'amqp://guest:guest@localhost:5672/'


    CELERY_WEB_BROKER_URL = 'sqs://{AWS_ACCESS_KEY_ID}:{AWS_SECRET_ACCESS_KEY}'\
                            '@sqs.{REGION}.amazonaws.com/{ACCOUNT}/{SERVICE_NAME}'\
        .format(
            AWS_ACCESS_KEY_ID=quote(os.getenv('AWS_ACCESS_KEY_ID'), safe=''),
            AWS_SECRET_ACCESS_KEY=quote(os.getenv('AWS_SECRET_ACCESS_KEY'), safe=''),
            REGION=os.getenv('AWS_REGION'),
            ACCOUNT=os.getenv('AWS_ACCOUNT'),
            SERVICE_NAME=os.getenv('AWS_ACCOUNT')
        )


