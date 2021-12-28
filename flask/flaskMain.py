###################### Imports ######################

from flask import Flask, render_template,request,redirect,url_for,session,flash
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from utils import * #imports celery
import emailReport
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed
from flask_sqlalchemy import SQLAlchemy

# from celery import Celery


import os
import sys

# is there a way to do just import?
sys.path.insert(0, "../emailValidity") # to import emailValidity.py
import emailValidity

UPLOAD_FOLDER = '../flask/uploadFolder'
ALLOWED_EXTENSIONS = {'.csv','.xlsx'}

###################### Flask ######################

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__,template_folder='HTML')

app.secret_key = "super secret key"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost:5672/' #'amqp://guest:guest@http://127.0.0.1:5000/' #rabbit mq.
#app.config['CELERY_BACKEND'] = #db
celery = make_celery(app)

bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


###################### Functions ######################
@app.route('/', methods=['GET','POST'])
def index():
    email = None
    file = None
    form = NameForm()
    if form.validate_on_submit():
        email = form.email.data
        file = form.file.data
    form.email.data = ''


    if file:
        print(email)
        #save the file
        filename = secure_filename(file.filename)
        #determine the extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        #find extension
        extension = os.path.splitext(filename)[1]
        extension = "csv" if extension == ".csv" else "xlsx"

        """Celery"""
        #parse
        go.delay(os.path.join(app.config['UPLOAD_FOLDER'], filename), email, extension)
        """
        emailVerify.(os.path.join(app.config['UPLOAD_FOLDER'], filename), email, extension)

        #remove the file
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File {0} uploaded and parsed!\nInitial length: {1}. Final length: {2}'.format(filename,
                                                                                            session["initial"],
                                                                                           session["final"]))
        """
        return redirect("/")

    return render_template('upload.html', form=form, email=email, file=file)

#
@celery.task(name='flaskMain.go')
def go(path, recipients=None, extension="csv"):
    emailVerify(path, recipients, extension)

    # remove the file
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    flash('File {0} uploaded and parsed!\nInitial length: {1}. Final length: {2}'.format(filename,
                                                                                         session["initial"],
                                                                                         session["final"]))

# processSheet
"""
@celery.task(name='flaskMain.processSheet')
def processSheet(file, email):
    print(email)
    # save the file
    filename = secure_filename(file.filename)
    # determine the extension
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # find extension
    extension = os.path.splitext(filename)[1]
    extension = "csv" if extension == ".csv" else "xlsx"
    # parse
    emailVerify(os.path.join(app.config['UPLOAD_FOLDER'], filename), email, extension)
    # remove the file
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    flash('File {0} uploaded and parsed!\nInitial length: {1}. Final length: {2}'.format(filename,
                                                                                         session["initial"],
                                                                                         session["final"]))
    #return 'done' #redirect("/")
"""

#class for the form
class NameForm(FlaskForm):
    email = StringField('What is your email?', validators=[DataRequired(), Email()])
    file = FileField('Select your file', validators=[DataRequired(),
                                                     FileAllowed(["csv", "xlsx"],
                                                                 "Only CSV or XLSX files are allowed")])
    submit = SubmitField('Submit')

#@celery.task(name='flaskMain.emailVerify')
def emailVerify(path, recipients=None, extension="csv"):
    valid = emailValidity.emailValidation(filename=path,type=extension, debug=True, multi=True)
    valid.check(save=True, inplace=True)
    session["initial"]=valid.getInitialLength()
    session["final"]=valid.getFinalLength()
    subjectLine = os.path.basename(path)

    report = emailReport.report("aleksei@lightyearstrategies.com", recipients,
                                "Checked '%s' file" % subjectLine, "We parsed your file!", path,
                                "me")
    report.sendMessage()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)