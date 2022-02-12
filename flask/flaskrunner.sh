cd /home/ubuntu
source lysenv1/bin/activate
cd lightyear/flask
celery -A flaskMain.celery worker -l INFO
sudo gunicorn --bind 0.0.0.0:80 wsgi:app
