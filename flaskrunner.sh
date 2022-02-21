#!/bin/bash

echo "sourcing venv"
source venv/bin/activate
echo "sourced venv"

if pgrep -f 'celery worker' 2>/dev/null; then
  echo "terminating celery worker "
  pkill -9 -f 'celery worker'
  echo "terminated celery worker"
fi

echo "starting celery"
celery -A flaskMain.celery worker -l INFO --detach
echo "started celery"

echo "starting gunicorn"
sudo gunicorn --bind 0.0.0.0:80 -w 2 wsgi:app
echo "started gunicorn"

echo "deactivating venv"
deactivate
echo "deactivated venv"
