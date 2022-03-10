###################### Imports ######################

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed
from flask_sqlalchemy import SQLAlchemy

import pandas as pd
import os
import sys
import time
from datetime import datetime, timedelta, date

from flask_app.config import *
from flask_app.utils import * # imports Celery, timethis

from  ev_20 import emailAPIvalid
from flask_app import emailRep
from flask_app.googleAuth import g_oauth, authCheck
from haroListener.haro_listener import HaroListener

###################### Flask ######################

app = Flask(__name__,template_folder=os.path.join(FLASK_DIR, 'HTML'))
app.register_blueprint(g_oauth)

app.secret_key = FLASK_SECRET_KEY #used in upload forms ?

os.makedirs(UPLOAD_DIR,exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

from kombu.utils.url import quote
app.config['CELERY_BROKER_URL'] = \
    'sqs://{AWS_ACCESS_KEY_ID}:{AWS_SECRET_ACCESS_KEY}@sqs.ca-central-1.amazonaws.com/453725380860/FlaskAppSQS-1'.format(
                                    AWS_ACCESS_KEY_ID=quote(AWS_ACCESS_KEY_ID, safe=''),
                                    AWS_SECRET_ACCESS_KEY=quote(AWS_SECRET_ACCESS_KEY, safe='')
                                    )
app.config['BROKER_TRANSPORT_OPTIONS'] = {"region": "ca-central-1"}

                                #'amqp://guest:guest@localhost:5672/'  # local rabbitMQ for Celery

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(FLASK_DIR, 'HarosDB.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

celery = make_celery(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
db.create_all()

###################### Classes ######################

class uploadEmailFilesForm(FlaskForm):
    """
    Constructor for the Email Verification Form
    """
    email = StringField('What is your email?', validators=[DataRequired(), Email()])
    files = MultipleFileField('Select your files',
                              validators=[DataRequired(), FileAllowed(["csv", "xlsx"], "Only CSV or XLSX files are allowed")])
    submit = SubmitField('Submit')

###################### Functions ######################

def removeDBdups():
    """
    removes duplicates from SQLite DB, does not need to be run often, as the addDBData function now checks for duplicates
    """
    whole_db = pd.read_sql_table('haros', db.engine)
    print(whole_db)
    whole_db.drop_duplicates(subset=['Summary'], inplace=True)
    print(whole_db)
    whole_db.to_sql('haros', con=db.engine, index=False, if_exists='replace')
    new_db = pd.read_sql_table('haros', db.engine)
    print(new_db)

# @param:    csv file with parsed haros
# @return:   None
def addDBData(df: pd.DataFrame):
    """
    Adds data to SQLite DB and checks for duplicateses
    """

    # checking for duplicates
    try:
        df.columns = df.columns.str.replace(' ', '')
        df.drop('Unnamed:0', axis=1, inplace=True)

    except Exception:
        print("no unnamed column")

    finally:
        print("in finally block")
        whole_db = pd.read_sql_table('haros', db.engine)
        print(len(whole_db))
        res = pd.concat([whole_db, df])
        print(len(res))
        res.drop_duplicates(subset=['Summary'], inplace=True)
        print(len(res))

        # Load data to database
        res.to_sql(name='haros', con=db.engine, index=False, if_exists='replace')


def listener_bg_process():
    """
    A function for celery to use to create a background process to listen for haro emails
    """
    listener = HaroListener('george@lightyearstrategies.com', False)
    listener.listen(addDBData)

#@param:    None
#@return:   Haros table
@app.route('/haros')
def serveTable():
    """
    Brings to the table with Haros
    """
    return render_template('haroTableView.html', title='LyS Haros Database')

#@param:    None
#@return:   table entries
@app.route('/api/serveHaros/<aim>', methods=['GET', 'POST'])
@app.route('/api/serveHaros', methods=['GET', 'POST'])
def data(aim=None):
    """
    Sorts the table, returns searched data
    """

    Haros = db.Table('haros', db.metadata, autoload=True, autoload_with=db.engine)
    #print(type(Haros.columns.DateReceived))
    #print(Haros.columns.DateReceived.all_())
    query = db.session.query(Haros) #.all()

    # fresh queries
    if aim == "fresh":
        freshmark = datetime.today().date() - timedelta(days=15)
        query = query.filter(Haros.columns.DateReceived >= freshmark)
    
    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Haros.columns.Category.like(f'%{search}%'),
            Haros.columns.Date.like(f'%{search}%'),
            Haros.columns.Deadline.like(f'%{search}%'), #Deadline --> Date
            Haros.columns.Summary.like(f'%{search}%'),
            Haros.columns.Email.like(f'%{search}%'),
            Haros.columns.MediaOutlet.like(f'%{search}%'),
            Haros.columns.Name.like(f'%{search}%'),
            Haros.columns.Requirements.like(f'%{search}%')
        ))

    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:

        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['Category','Date','MediaOutlet','Deadline']:
            col_name = 'Category'

        # gets descending sorting
        descending = request.args.get(f'order[{i}][dir]') == 'desc'

        desiredCol = getattr(Haros.columns,col_name)

        #decending
        if descending:
            desiredCol = desiredCol.desc()
        order.append(desiredCol)

        i += 1

    # ordering
    if order:
        query = query.order_by(*order)
        
    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response to be shown on HTML side
    return {
        'data': [dict(haro) for haro in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': query.count(),
        'draw': request.args.get('draw', type=int),
    }



#@param:    None
#@return:   Email Verification Page
@app.route('/', methods=['GET','POST'])
def validation():
    """
    Gets information from the form, extracts files.
    Sends files to Celery via SQS broken for background email verification.
    Redirects to authentication if bot is not logged in
    """
    email = None
    files = None
    form = uploadEmailFilesForm()
    if form.validate_on_submit():
        filenames = []
        email = form.email.data
        files = request.files.getlist(form.files.name)
        form.email.data = ''

        if not authCheck():
            return redirect('/authorizeCheck')

        if files:
            for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames.append(filename)

            for filename in filenames:
                # determine extension
                extension = os.path.splitext(filename)[1]
                # find extension
                extension = "csv" if extension == ".csv" else "xlsx"

                # Celery
                # parse,remove file, send updated file
                parseSendEmail.delay(os.path.join(app.config['UPLOAD_FOLDER'], filename), email, filename)

            return redirect("/")
        else:
            print('No files')

    return render_template('uploadEmailFiles.html', form=form, email=email, files=files)

#@param:    path to file with emails
#@param:    recipients of processed file
#@param:    filename
#@return:   None
@celery.task(name='flaskMain.parseSendEmail')
def parseSendEmail(path, recipients=None, filename=None):
    """
    Celery handler.
    """
    with app.app_context():
        emailVerify(path, recipients)

        # remove the file
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#@param:    path to file with emails
#@param:    recipients of processed file
#@return:   None
def emailVerify(path, recipients=None):
    """
    Uses functions from emailAPIvalid to verify emails.
    Creates email with processed file and sends it.
    """
    email = emailAPIvalid.emailValidation(filename=path)
    email.validation(save=True)

    subjectLine = os.path.basename(path)
    report = emailRep.report("george@lightyearstrategies.com", recipients,
                                "Verified Emails in '%s' file" % subjectLine, "Here is your file", path,"me")
    report.sendMessage()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    #addDBData("/Users/rutkovskii/lightyear/haroListener/haro_csvs/HAROS.csv")
    app.run(host='0.0.0.0', port=80,debug=True)

