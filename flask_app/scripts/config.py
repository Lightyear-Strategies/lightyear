import os
from kombu.utils.url import quote    # To work with AWS SQS

SCRIPTS_DIR = os.path.abspath(os.path.dirname(__file__))
FLASK_DIR = os.path.dirname(SCRIPTS_DIR)
LIGHTYEAR_DIR = os.path.dirname(FLASK_DIR)

CONFIG_DIR = os.path.join(FLASK_DIR,'configs')
UPLOAD_DIR = os.path.join(FLASK_DIR,'uploadFolder')
os.makedirs(UPLOAD_DIR, exist_ok=True)
HTML_DIR = os.path.join(FLASK_DIR,'HTML')


AWS_ACCESS_KEY_ID = None
with open(os.path.join(CONFIG_DIR, 'aws_access.txt'), "r") as aws_a_k:
    AWS_ACCESS_KEY_ID = aws_a_k.read()

AWS_SECRET_ACCESS_KEY = None
with open(os.path.join(CONFIG_DIR, 'aws_secret.txt'), "r") as aws_secret:
    AWS_SECRET_ACCESS_KEY = aws_secret.read()

FLASK_SECRET_KEY = '\xe9Y\xc6\xc0U\xab\xbf\xaed\xb6!:\x8fI\xbb?\xc1\t\xce\xf59N0\xf0\xd8\xf7\xbb\x13\\\xad\x08k'

AWS_REGION = 'ca-central-1',
AWS_ACCOUNT = '453725380860',
AWS_SERVICE_NAME = 'FlaskAppSQS-1'


DATABASE_URI = 'sqlite:///' + os.path.join(FLASK_DIR, 'Database.sqlite3')
CELERY_LOCAL_BROKER_URL = 'amqp://guest:guest@localhost:5672/'

CELERY_WEB_BROKER_URL = 'sqs://{AWS_ACCESS_KEY_ID}:{AWS_SECRET_ACCESS_KEY}' \
                        '@sqs.{REGION}.amazonaws.com/{ACCOUNT}/{SERVICE_NAME}'\
    .format(
        AWS_ACCESS_KEY_ID=quote(AWS_ACCESS_KEY_ID, safe=''),
        AWS_SECRET_ACCESS_KEY=quote(AWS_SECRET_ACCESS_KEY, safe=''),
        REGION=AWS_REGION,
        ACCOUNT=AWS_ACCOUNT,
        SERVICE_NAME=AWS_SERVICE_NAME
    )