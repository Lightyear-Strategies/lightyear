import os

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

FLASK_SECRET_KEY = "super secret key"

FLASK_DIR = os.path.abspath(os.path.dirname(__file__))
LIGHTYEAR_DIR = os.path.dirname(FLASK_DIR)
UPLOAD_DIR = FLASK_DIR + '/uploadFolder'
EMAIL_VALIDITY_DIR = LIGHTYEAR_DIR +'/emailValidity'
EMAIL_VALIDITY_DIR2 = LIGHTYEAR_DIR + '/ev_20'
