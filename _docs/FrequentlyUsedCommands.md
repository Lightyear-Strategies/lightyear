source venv/bin/activate

deactivate

sudo gunicorn -w 3wsgi:app

celery -A flask_app.scripts.EmailVerification.ev_flask_functions.celery worker -l INFO

pip3 freeze > requirements.txt


sudo lsof -i :<PortNumber>
kill -9 <PID>

