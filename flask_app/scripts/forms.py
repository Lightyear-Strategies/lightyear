from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, MultipleFileField, RadioField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, InputRequired, EqualTo, ValidationError, Length, Regexp

from flask_app.scripts.LoginRegister.models import User


class uploadEmailFilesForm(FlaskForm):
    """Constructor for the Email Verification Form"""

    email = StringField('What is your email?', validators=[DataRequired(), Email()])
    files = MultipleFileField('Select your files',
                              validators=[DataRequired(), FileAllowed(["csv", "xlsx"], "Only CSV or XLSX files are allowed")])
    submit = SubmitField('Submit')

class uploadJournalistCSV(FlaskForm):
    """Constructor for the Journalist Subscription Form"""

    username = StringField('What is your full name?', validators=[DataRequired()])
    email = StringField('What is your email?', validators=[DataRequired(), Email()])
    frequency = RadioField(label='Receive updates every', validators=[InputRequired()],
                           choices=[('_day', 'day'), ('_week', 'week'), ('_month', 'month')])

    files = MultipleFileField('Select your files',
                              validators=[DataRequired(),
                                          FileAllowed(["csv", "xlsx"], "Only CSV or XLSX files are allowed")])
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators =[DataRequired(),
                                        Length(3, 30, message="Please provide a valid name"),
                                        Regexp(
                                            "^[A-Za-z][A-Za-z0-9_.]*$", 0,
                                            "Usernames must have only letters, numbers, dots or underscores",
                                        )
                                        ])
    email = StringField('Email', validators=[DataRequired(),Email(), Length(1, 64)])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(2, 72)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(2, 72),
                                                                EqualTo('password1',message="Passwords must match!")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username already in use.')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already in exists.')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email(),Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired(),Length(2, 72)])
    remember = BooleanField('Remember Me',validators= [DataRequired()]) # if remember then sessions?
    submit = SubmitField('Login')

    def validate_email(self, email):
        if not User.query.filter_by(email=email.data).first():
            raise ValidationError('This email is not registered.')


