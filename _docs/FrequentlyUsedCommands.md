source venv/bin/activate

deactivate

sudo gunicorn -w 3 wsgi:app

PATH=$PATH:/usr/local/sbin
sudo rabbitmq-server -detached
celery -A flask_app.scripts.EmailValidator.ev_flask_functions.celery worker -l INFO
sudo rabbitmqctl stop

pip3 freeze > requirements.txt


sudo lsof -i :<PortNumber>
kill -9 <PID>

