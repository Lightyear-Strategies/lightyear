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
celery -A flask_app.scripts.EmailVerification.ev_flask_functions.celery worker -l INFO --detach
echo "started celery"

echo "starting gunicorn"
sudo gunicorn -w 3 wsgi:app
echo "started gunicorn"

echo "deactivating venv"
deactivate
echo "deactivated venv"
