#### ———— After Restructuring ————
Possibly will need to redo shell scripts (Check)


__ To Run the Worker: __

celery -A flask_app.scripts.ev_flask_functions.celery worker -l INFO

__For Future:__

1. RabbitMQ can be run using Docker


#### ———— How to Start Celery in Flask ————

1. Install Celery
```
$ pip install celery
```

2. Create `celeryForProject.py` containing:

```
from celery import Celery

def init_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
```

3. Create `project.py` containing:

```
from celeryForProject import *

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost:5672/'
# app.config['CELERY_BACKEND'] = # for adding backend
celery = make_celery(app)


@app.route('/)
def addi(a,b):

    mult.delay(a,b)
    
    return f"This is Addition, and res is {a+b}"
    
@celery.task(name='project.mult')
def mult(a,b):
    return f"This is Multiplocation, and res is {a*b}"  
    
if __name__ == '__main__':
    app.run(debug=True)
    
```
- celery.task will return Multiplication string to terminal window with celery worker open
- Addition string will return to terminal window associated with Flask


4. Set Up RabbitMQ (on MacOS)

[I used this source](https://docs.celeryproject.org/en/latest/getting-started/backends-and-brokers/rabbitmq.html#installing-rabbitmq-on-macos)

In short:
- Install Homebrew
`$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- Install RabbitMQ 
`$ brew install rabbitmq`
- Add the following to your path to be able to start and stop the broker: 
`$ PATH=$PATH:/usr/local/sbin`
  - In case of running with a start up file, add it to shell (e.g., .bash_profile or .profile).

5. Start/Stop RabbitMQ Server

* To start the server in Foreground: `$ sudo rabbitmq-server`

* To start the server in Background: `$ sudo rabbitmq-server -detached`

* Never use **kill** *(kill(1))* to stop the RabbitMQ server, but rather use the rabbitmqctl command:
`$ sudo rabbitmqctl stop`

To Access RabbitMQ go to: http://localhost:15672/
To Check whether worker is connected: http://localhost:15672/#/connections

6. Start RabbitMQ Worker

To run worker in Foreground:
`$ celery -A flask_app.scripts.EmailVerification.ev_flask_functions.celery worker -l INFO`

To run Worker in Background (Have not went over it):
https://docs.celeryproject.org/en/latest/getting-started/next-steps.html#in-the-background

To turn off worker: `ctrl-C`

But [this guide](https://docs.celeryproject.org/en/latest/userguide/workers.html#stopping-the-worker) suggests (*but Idk how to use these*) 
- Shutdown should be accomplished using the TERM signal.
- Also as processes can’t override the KILL signal, the worker will not be able to reap its children; make sure to do so
manually. This command usually does the trick: 
`$ pkill -9 -f 'celery worker'`

7. Start Flask

`python3 project.py`


---- Guides that were used: ----

Instructions from: https://www.youtube.com/watch?v=iwxzilyxTbQ

Code from: https://flask.palletsprojects.com/en/2.0.x/patterns/celery/

Overview: https://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html

Downloading RabbitMQ for MacOS: https://docs.celeryproject.org/en/latest/getting-started/backends-and-brokers/rabbitmq.html#broker-rabbitmq

About workers: https://docs.celeryproject.org/en/latest/userguide/workers.html#stopping-the-worker

Celery Best Practices: https://betterprogramming.pub/python-celery-best-practices-ae182730bb81

Found about Celery from: https://stackoverflow.com/questions/45363505/python-flask-returning-a-html-page-while-simultaneously-performing-a-function/45383965


Handy stackoverflow posts:

1. https://stackoverflow.com/questions/18133249/django-celery-cannot-connect-to-amqp-guest127-0-0-80005672
2. https://stackoverflow.com/questions/49373825/kombu-exceptions-encodeerror-user-is-not-json-serializable
3. https://stackoverflow.com/questions/25884951/attributeerror-flask-object-has-no-attribute-user-options
