#!/bin/bash

# echo $PWD
# path="${PWD}/dailyCategoricalParser.py"
# echo $path

echo ""
echo "########################################"
cd ~/lightyear

d_t=`date +"%d-%m-%Y %R"`
echo "Today: ${d_t}"

echo "sourcing venv"
# if running locally, activating venv may cause a problem (if venv is already active)
source venv/bin/activate
echo "sourced venv"

if [ "$1" == "parse" ];
then
  echo "Categorical Parser"
  sudo python3 categoricalWritersRunner.py $1

elif [ "$1" == "send" ];
then
  echo "Categorical Send $2"
  sudo python3 categoricalWritersRunner.py $1 $2
fi

echo "deactivating venv"
deactivate
echo "deactivated venv"
