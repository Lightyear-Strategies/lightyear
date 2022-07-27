#!/bin/bash

# path="${PWD}/dailyCategoricalParser.py"
# echo $path

echo ""
echo "########################################"
cd ~/lightyear

#echo $PWD

d_t=`date +"%d-%m-%Y %R"`
echo "Today: ${d_t}"

echo "sourcing venv"
# if running locally, activating venv may cause a problem (if venv is already active)
source venv/bin/activate
echo "sourced venv"

if [ $# -eq 2 ];
then
  if [ "$1" == "parse" ];
  then
    echo "Categorical Parser"
    sudo python3 categoricalWritersRunner.py $1 $2

    echo "scp reports to the main server"
    scp -i /home/ubuntu/pems/MainServer.pem -r /home/ubuntu/lightyear/flask_app/scripts/PeriodicWriters/reports ubuntu@99.79.179.105:/home/ubuntu/lightyear/flask_app/scripts/PeriodicWriters

  elif [ "$1" == "send" ];
  then
    echo "Categorical Send $2"
    sudo python3 categoricalWritersRunner.py $1 $2

  else
    echo "Incorrect 1st argument"
  fi

else
  echo "You did not provide 2 arguments"
fi

echo "deactivating venv"
deactivate
echo "deactivated venv"
