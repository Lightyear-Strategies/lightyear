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

from utils import * # imports Celery, timethis
import emailReport

sys.path.insert(0, "../emailValidity") # to import emailValidity.py
import emailValidity


###################### Flask ######################

app = Flask(__name__,template_folder='HTML')

app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = '../flask/uploadFolder'

# Celery
app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost:5672/'  # rabbitMQ
#app.config['CELERY_BACKEND'] = # for adding backend
celery = make_celery(app)

bootstrap = Bootstrap(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'HarosDB.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

###################### Globals ######################

ALLOWED_EXTENSIONS = {'.csv','.xlsx'}

###################### Classes ######################

#class for the email file upload form
class uploadEmailFilesForm(FlaskForm):
    email = StringField('What is your email?', validators=[DataRequired(), Email()])
    files = MultipleFileField('Select your files',
                              validators=[DataRequired(), FileAllowed(["csv", "xlsx"], "Only CSV or XLSX files are allowed")])
    submit = SubmitField('Submit')

###################### Functions ######################

def addDBData(file):
    # Read file into dataframe
    csv_data = pd.read_csv(file.name)

    # Removing white space in headers
    csv_data.columns = csv_data.columns.str.replace(' ', '')

    # Dropping the first column which is unnamed index
    csv_data.drop('Unnamed:0', axis=1, inplace=True)

    # Load data to database
    csv_data.to_sql(name='haros', con=db.engine, index=True, if_exists='append')

@app.route('/haros')
def serveTable():
    return render_template('haroTableView.html', title='LyS Haros Database')

#sorting table contents
@app.route('/api/serveHaros')
def data():
    Haros = db.Table('haros', db.metadata, autoload=True, autoload_with=db.engine)
    #print(Haros.columns)
    query = db.session.query(Haros) #.all()
    #print(query)

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Haros.columns.Category.like(f'%{search}%'),
            Haros.columns.Deadline.like(f'%{search}%'),
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
        if col_name not in ['Category','Deadline','MediaOutlet']:
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

@app.route('/', methods=['GET','POST'])
def validation():
    email = None
    files = None
    form = uploadEmailFilesForm()
    if form.validate_on_submit():
        filenames = []
        email = form.email.data
        files = request.files.getlist(form.files.name)
        form.email.data = ''

        if files:
            for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames.append(filename)
            #print('Saved')

            for filename in filenames:
                #print('in for loop')
                # determine extension
                extension = os.path.splitext(filename)[1]
                # find extension
                extension = "csv" if extension == ".csv" else "xlsx"

                # Celery
                # parse,remove file, send updated file
                parseSendEmail.delay(os.path.join(app.config['UPLOAD_FOLDER'], filename), email, extension, filename)

            return redirect("/")
        else:
            print('No files')

    return render_template('uploadEmailFiles.html', form=form, email=email, files=files)


@celery.task(name='flaskMain.parseSendEmail')
def parseSendEmail(path, recipients=None, extension="csv", filename=None):
    with app.app_context():
        emailVerify(path, recipients, extension)

        # remove the file
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

def emailVerify(path, recipients=None, extension="csv"):
    valid = emailValidity.emailValidation(filename=path,type=extension, debug=True, multi=True)
    valid.check(save=True, inplace=True)
    subjectLine = os.path.basename(path)

    report = emailReport.report("aleksei@lightyearstrategies.com", recipients,
                                "Verified Emails in '%s' file" % subjectLine, "Here is your file", path,"me")

    report.sendMessage()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    #file1 = open('HARO_test.csv')
    #addDBData(file1)
    app.run(debug=True)
    
