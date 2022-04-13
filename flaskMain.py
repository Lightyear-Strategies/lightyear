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
import traceback
from datetime import datetime, timedelta, date

from flask_app.config import *
from flask_app.utils import *  #imports Celery, timethis

from ev_20 import emailAPIvalid
from flask_app import emailRep
from flask_app.googleAuth import g_oauth, authCheck, localServiceBuilder

#from weeklyWriters.weekly import WeeklyReport

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

# To work with Celery in local environment using RabbitMQ, uncomment app.config below and comment our the two above
#app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost:5672/'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(FLASK_DIR, 'HarosDB.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

celery = make_celery(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
db.create_all()

###################### Classes ######################

class uploadEmailFilesForm(FlaskForm):
    """Constructor for the Email Verification Form"""

    email = StringField('What is your email?', validators=[DataRequired(), Email()])
    files = MultipleFileField('Select your files',
                              validators=[DataRequired(), FileAllowed(["csv", "xlsx"], "Only CSV or XLSX files are allowed")])
    submit = SubmitField('Submit')

class uploadJournalistCSV(FlaskForm):
    """Constructor for the Journalist Subscription Form"""

    personname = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your email?', validators=[DataRequired(), Email()])
    files = MultipleFileField('Select your files',
                              validators=[DataRequired(), FileAllowed(["csv", "xlsx"], "Only CSV or XLSX files are allowed")])
    submit = SubmitField('Submit')


###################### Functions ######################

#@param:    None
#@return:   Upload Journalists Page
@app.route('/journalists', methods=['GET','POST'])
def uploadJournalist():
    """
    Gets csv(s) with Journalists from the form, extracts data.
    """
    personname, email, files = None, None, None

    form = uploadJournalistCSV()
    if form.validate_on_submit():
        personname = form.personname.data
        personemail = form.email.data
        files = request.files.getlist(form.files.name)
        form.email.data = ''
        # filename

        journalists = []
        if files:
            for file in files:
                df = None
                try:
                    df = pd.read_csv(file)

                except Exception:
                    flash("Upload file in CSV Format")
                    print("Not CSV")
                    return redirect("/journalists")


                finally:
                    """For Future: should use re to check for 'ournalist' string """

                    pos_names = ["Journalists","Journalist","Journalist(s)","journalists", "journalist", "journalist(s)"]
                    i = 0
                    len_pos_names = len(pos_names)
                    while True:
                        if i == len_pos_names:
                            flash("You do not have neither \"Journalist(s)\" nor \"journalist(s)\"")
                            return redirect("/journalists")
                        if pos_names[i] in df.columns:
                            journalists.extend(df[pos_names[i]].tolist())
                            break
                        i+=1

            # only executed if there is no 'journalists' table
            if not db.inspect(db.engine.connect()).has_table('journalists'):
                data = [[personname,personemail,journalist, None] for journalist in journalists]
                df = pd.DataFrame(data, columns = ['ClientName', 'ClientEmail', 'Journalist','Muckrack'])
                df.to_sql(name='journalists', con=db.engine, index=False)

            else:

                try:
                    """For Future: No so efficient to drop all old entries and then append the new ones"""
                    journalists_df = pd.read_sql_table('journalists', db.engine)

                    # There are entries with current client, we remove the entries
                    if len(journalists_df[journalists_df['ClientName'] == personname]) > 0:
                        print("Deleting old entries")
                        journalists_df = journalists_df[journalists_df['ClientName'] != personname]

                    # Add new entries
                    print("Adding new rows")
                    data = [[personname, personemail, journalist, None] for journalist in journalists]
                    new_df = pd.DataFrame(data, columns=['ClientName', 'ClientEmail', 'Journalist','Muckrack'])
                    journalists_df = pd.concat([journalists_df,new_df], ignore_index=True)
                    journalists_df.to_sql(name='journalists', con=db.engine, index=False, if_exists='replace')

                    flash('Successfully Subscribed')
                except Exception:
                    traceback.print_exc()

                    # script to drop table, run with sudo privilage
                    #jour_table = db.Table('journalists', db.metadata, autoload=True, autoload_with=db.engine)
                    #print("Dropping the Journalists Table")
                    #jour_table.drop(db.engine)


            return redirect("/journalists")
        else:
            print('No files')

    return render_template('uploadJournalistCSV.html', form=form, email=email, files=files)

def journalistTableEntry(personname,personemail,list_journalists):
    row_dict = dict()
    row_dict["Name"] = personname
    row_dict["ClientEmail"] = personemail
    row_dict["Journalists"] = list_journalists

    return pd.DataFrame(data=row_dict)

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
def addDBData(df: pd.DataFrame): #(file):
    """
    Adds data to SQLite DB and checks for duplicates
    """
    # checking for duplicates
    whole_db = pd.read_sql_table('haros', db.engine, index_col='index')
    print(len(whole_db))
    print(whole_db.columns)
    res = pd.concat([whole_db, df])
    print(len(res))
    res.drop_duplicates(subset=['Summary'], inplace=True)
    print(len(res))
    res.reset_index(drop=True, inplace=True)

    # Load data to database
    print(res.columns)
    res.to_sql(name='haros', con=db.engine, index=True, if_exists='replace')



#@param:    None
#@return:   Haros table
@app.route('/haros')
def serveTable():
    """
    Brings to the table with Haros
    """
    return render_template('haroTableView.html', title='LyS Haros Database')

#@param:    option and id in the table
#@return:   string
@app.route('/api/used/<option>/<id>')
def used_unused(option : str = None, id : str = None):
    """
    Changes value in "Used" column of certain haro by using id
    Values can be "Used" or "None"
    """

    Haros = db.Table('haros', db.metadata, autoload=True, autoload_with=db.engine)
    query = db.session.query(Haros).filter(Haros.columns.index == int(id))
    #print(query.all())

    if option == "add":
        query.update({Haros.columns.Used : "Used" })
        db.session.commit()

    elif option == "remove":
        query.update({Haros.columns.Used: "None"})
        db.session.commit()

   # print(query.all())

    return "Ok"


#@param:    None/option
#@return:   table entries
@app.route('/api/serveHaros/<option>')
@app.route('/api/serveHaros')
def data(option=None):
    """
    Sorts the table, returns searched data
    """

    Haros = db.Table('haros', db.metadata, autoload=True, autoload_with=db.engine)
    #print(Haros.columns.DateReceived.all_())
    query = db.session.query(Haros) #.all()

    if option == "used":
        query = query.filter(Haros.columns.Used == "Used")

    # fresh queries
    if option == "fresh":
        freshmark = datetime.today().date() - timedelta(days=3)
        query = query.filter(Haros.columns.DateReceived >= freshmark)

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Haros.columns.Category.like(f'%{search}%'),
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


        # This part is only for web deployment
        if not authCheck():
            return redirect('/authorizeCheck')

        #localServiceBuilder() # Uncomment this, and comment the above lines to run locally

        if files:
            for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames.append(filename)

            for filename in filenames:
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
    """Celery handler"""
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
    #addDBData("/Users/rutkovskii/lightyear/haroListener/haro_csvs/ALL_OLD_HAROS.csv")
    #removeDBdups()

    #from werkzeug.middleware.profiler import ProfilerMiddleware
    #app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[5])
    app.run(host='0.0.0.0', port=80,debug=False,threaded=True)

