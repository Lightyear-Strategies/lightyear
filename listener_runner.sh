#!/bin/bash

cd ~/lightyear

echo ""
echo "########################################"
d_t=`date +"%d-%m-%Y %R"`
echo "Today: ${d_t}"

echo "sourcing venv"
source venv/bin/activate
echo "sourced venv"

echo "starting listener"
# In order to resolve this error " Permission denied: '/home/ubuntu/lightyear/flask_app/configs/server_token.pickle' "
sudo python3 listenerMain.py
echo "started listener"

echo "deactivating venv"
deactivate
echo "deactivated venv"
