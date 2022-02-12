import os

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

#AWS_ACCESS_KEY_ID = None
#with open('aws_access.txt',"r") as aws_a_k:
#    AWS_ACCESS_KEY_ID = aws_a_k.read()

#AWS_SECRET_ACCESS_KEY = None
#with open('aws_secret.txt',"r") as aws_secret:
#    AWS_SECRET_ACCESS_KEY = aws_secret.read()

FLASK_SECRET_KEY = None
with open('flask_secret.txt',"r") as flask_secret:
    FLASK_SECRET_KEY = flask_secret.read()

FLASK_DIR = os.path.abspath(os.path.dirname(__file__))
LIGHTYEAR_DIR = os.path.dirname(FLASK_DIR)
UPLOAD_DIR = FLASK_DIR + '/uploadFolder'
EMAIL_VALIDITY_DIR = LIGHTYEAR_DIR + '/ev_20'
