#!/bin/bash

ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9
cd /home/ubuntu
source lysenv1/bin/activate
cd lightyear/flask
celery -A flaskMain.celery worker -l INFO --detach
sudo gunicorn --bind 0.0.0.0:80 -w 2 wsgi:app
