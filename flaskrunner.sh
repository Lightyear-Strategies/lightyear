#!/bin/bash

echo "sourcing venv"
source venv/bin/activate
echo "sourced venv"

echo "starting gunicorn"
sudo gunicorn -w 3 wsgi:app
echo "started gunicorn"

echo "deactivating venv"
deactivate
echo "deactivated venv"
