import os
from kombu.utils.url import quote    # To work with AWS SQS
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Directories
    SCRIPTS_DIR = os.path.abspath(os.path.dirname(__file__))
    FLASK_DIR = os.path.dirname(SCRIPTS_DIR)
    LIGHTYEAR_DIR = os.path.dirname(FLASK_DIR)
    CONFIG_DIR = os.path.join(FLASK_DIR,'configs')
    UPLOAD_DIR = os.path.join(FLASK_DIR,'uploadFolder')
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    HTML_DIR = os.path.join(FLASK_DIR,'HTML')

    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    #'\xe9Y\xc6\xc0U\xab\xbf\xaed\xb6!:\x8fI\xbb?\xc1\t\xce\xf59N0\xf0\xd8\xf7\xbb\x13\\\xad\x08k'
    DATABASE_URI = 'sqlite:///' + os.path.join(FLASK_DIR, 'Database.sqlite3')

    EV_API_KEY = os.getenv('EV_API_KEY')
    #os.path.join(CONFIG_DIR,'ev_api_key.json')
    WEB_CLIENT_SECRETS_FILE = os.getenv('WEB_CLIENT_SECRETS_FILE')
    #os.path.join(CONFIG_DIR,'web_google_client.json')
    LOCAL_CLIENT_SECRETS_FILE = os.getenv('WEB_CLIENT_SECRETS_FILE')
    #os.path.join(CONFIG_DIR,'local_google_client.json')
    PICKLE_FILE = os.path.join(CONFIG_DIR,'token.pickle')

    # AWS
    CELERY_WEB_BROKER_URL = 'sqs://{AWS_ACCESS_KEY_ID}:{AWS_SECRET_ACCESS_KEY}'\
                            '@sqs.{REGION}.amazonaws.com/{ACCOUNT}/{SERVICE_NAME}'\
        .format(
            AWS_ACCESS_KEY_ID=quote(os.getenv('AWS_ACCESS_KEY_ID'), safe=''),
            AWS_SECRET_ACCESS_KEY=quote(os.getenv('AWS_SECRET_ACCESS_KEY'), safe=''),
            REGION=os.getenv('AWS_REGION'),
            ACCOUNT=os.getenv('AWS_ACCOUNT'),
            SERVICE_NAME=os.getenv('AWS_ACCOUNT')
        )

    BROKER_TRANSPORT_OPTIONS = {"region":os.getenv('AWS_REGION')}

    CELERY_LOCAL_BROKER_URL = 'amqp://guest:guest@localhost:5672/'

    # AWS_ACCESS_KEY_ID = None
    # with open(os.path.join(CONFIG_DIR, 'aws_access.txt'), "r") as aws_a_k:
    #     AWS_ACCESS_KEY_ID = aws_a_k.read()
    #
    # AWS_SECRET_ACCESS_KEY = None
    # with open(os.path.join(CONFIG_DIR, 'aws_secret.txt'), "r") as aws_secret:
    #     AWS_SECRET_ACCESS_KEY = aws_secret.read()

#print(Config.FLASK_SECRET_KEY)
#print(Config.AWS_ACCESS_KEY_ID)