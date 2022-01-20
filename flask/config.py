import os

AWS_ACCESS_KEY_ID = 'AKIAWTJBD4D6MSEJXUF2'
AWS_SECRET_ACCESS_KEY = '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'

FLASK_SECURE_KEY = "super secret key"

FLASK_DIR = os.path.abspath(os.path.dirname(__file__))
LIGHTYEAR_DIR = os.path.dirname(FLASK_DIR)
UPLOAD_DIR = FLASK_DIR + '/uploadFolder'
EMAIL_VALIDITY_DIR = LIGHTYEAR_DIR +'/emailValidity'

