from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, MultipleFileField, RadioField
from wtforms.validators import DataRequired, Email, InputRequired
from flask_wtf.file import FileAllowed

###################### Forms ######################

class uploadEmailFilesForm(FlaskForm):
    """Constructor for the Email Verification Form"""

    email = StringField('What is your email?', validators=[DataRequired(), Email()])
    files = MultipleFileField('Select your files',
                              validators=[DataRequired(), FileAllowed(["csv", "xlsx"], "Only CSV or XLSX files are allowed")])
    submit = SubmitField('Submit')

class uploadJournalistCSV(FlaskForm):
    """Constructor for the Journalist Subscription Form"""

    personname = StringField('What is your full name?', validators=[DataRequired()])
    email = StringField('What is your email?', validators=[DataRequired(), Email()])
    frequency = RadioField(label='Receive updates every', validators=[InputRequired()], choices = [('_day', 'day'), ('_week', 'week'), ('_month', 'month')])
    files = MultipleFileField('Select your files',
                              validators=[DataRequired(), FileAllowed(["csv", "xlsx"], "Only CSV or XLSX files are allowed")])
    submit = SubmitField('Submit')
