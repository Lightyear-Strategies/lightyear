#!/bin/bash

cd ~/lightyear

echo "sourcing venv"
source venv/bin/activate
echo "sourced venv"

echo "starting listener"
python3 listenerMain.py 
echo "started listener"

echo "deactivating venv"
deactivate
echo "deactivated venv"
