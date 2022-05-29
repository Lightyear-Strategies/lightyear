source venv/bin/activate

deactivate

sudo gunicorn --bind 0.0.0.0:80 wsgi:app

celery -A flaskMain.celery worker -l INFO

pip3 freeze > all_requirements.txt

