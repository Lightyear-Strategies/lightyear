#!/bin/bash

pkill -9 -f 'celery worker'
cd /home/ubuntu
source lysenv1/bin/activate
cd lightyear/flask
celery -A flaskMain.celery worker -l INFO --detach
sudo gunicorn --bind 0.0.0.0:80 -w 2 wsgi:app
