source venv/bin/activate

deactivate

sudo gunicorn -w 3 wsgi:app

sudo systemctl start flaskrunner
sudo systemctl stop flaskrunner
sudo systemctl restart flaskrunner
sudo systemctl status flaskrunner




PATH=$PATH:/usr/local/sbin
sudo rabbitmq-server -detached
celery -A flask_app.scripts.EmailValidator.ev_flask_functions.celery worker -l INFO
sudo rabbitmqctl stop

pip3 freeze > requirements.txt


sudo lsof -i :<PortNumber>
sudo kill -9 <PID>

https://www.plesk.com/blog/various/find-files-in-linux-via-command-line/
sudo find / -name pg_config



