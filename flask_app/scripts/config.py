import os

SCRIPTS_DIR = os.path.abspath(os.path.dirname(__file__))
FLASK_DIR = os.path.dirname(SCRIPTS_DIR)
LIGHTYEAR_DIR = os.path.dirname(FLASK_DIR)

CONFIG_DIR = os.path.join(FLASK_DIR,'configs')

UPLOAD_DIR = os.path.join(FLASK_DIR,'uploadFolder')

os.makedirs(UPLOAD_DIR, exist_ok=True)


AWS_ACCESS_KEY_ID = None
with open(os.path.join(CONFIG_DIR, 'aws_access.txt'), "r") as aws_a_k:
    AWS_ACCESS_KEY_ID = aws_a_k.read()

AWS_SECRET_ACCESS_KEY = None
with open(os.path.join(CONFIG_DIR, 'aws_secret.txt'), "r") as aws_secret:
    AWS_SECRET_ACCESS_KEY = aws_secret.read()

FLASK_SECRET_KEY = None
with open(os.path.join(CONFIG_DIR, 'flask_secret.txt'), "r") as flask_secret:
    FLASK_SECRET_KEY = flask_secret.read()

