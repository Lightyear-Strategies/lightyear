source venv/bin/activate

deactivate

sudo gunicorn --bind 0.0.0.0:80 wsgi:app

celery -A flask_app.scripts.EmailVerification.ev_flask_functions.celery worker -l INFO

pip3 freeze > all_requirements.txt

