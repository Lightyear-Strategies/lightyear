from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, MultipleFileField, RadioField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, InputRequired, EqualTo, ValidationError, Length, Regexp

from flask_app.scripts.LoginSignUp.models import User


# class EmailValidator(FlaskForm):
#     """Constructor for the Email Verification Form"""
#
#     email = StringField('What is your email?', validators=[DataRequired(), Email()])
#     # files = MultipleFileField('Select your files',
#     #                           validators=[DataRequired(), FileAllowed(["csv", "xlsx"],
#     #                                                                   "Only CSV or XLSX files are allowed")])
#     submit = SubmitField('Submit')
#
#
# class PeriodicWriters(FlaskForm):
#     """Constructor for the Journalist Subscription Form"""
#
#     username = StringField('What is your full name?', validators=[DataRequired()])
#     email = StringField('What is your email?', validators=[DataRequired(), Email()])
#     frequency = RadioField('How frequently do you want to receive updates?',
#                             validators=[InputRequired()],
#                             choices=[('_day', 'daily'), ('_week', 'weekly')])
#
#     files = MultipleFileField('Select your files',
#                               validators=[DataRequired(),
#                                           FileAllowed(["csv", "xlsx"], "Only CSV or XLSX files are allowed")])
#     submit = SubmitField('Submit')


class SignUpForm(FlaskForm):
    """Constructor for the Register Page"""
    name = StringField('First Name',
                           validators =[DataRequired(),
                                        Length(1, 30, message="Please provide a valid name"),
                                        Regexp(
                                            "^[A-Za-z][A-Za-z0-9_.]*$", 0,
                                            "Names must have only letters, numbers, dots or underscores",
                                        )
                                        ])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(6, 72)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(6, 72),
                                                                EqualTo('password1',message="Passwords must match!")])
    submit = SubmitField('Register')

    # def validate_username(self, username):
    #     if User.query.filter_by(username=username.data.lower()).first():
    #         raise ValidationError('Username is already in use.')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data.lower().strip()).first():
            raise ValidationError('Email already exists.')


class LoginForm(FlaskForm):
    """Constructor for the Login Page"""
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired(),Length(2, 72)])
    remember_me = BooleanField('Remember Me')  # if remember then sessions?
    submit = SubmitField('Login')

    def validate_email(self, email):
        if "@" in email.data:
            print(len(email.data))
            print(len(email.data.lower().strip()))
            if not User.query.filter_by(email=email.data.lower().strip()).first():
                raise ValidationError('This email is not registered.')


    # def validate_username_email(self,username_email):
    #     if "@" in username_email.data:
    #         if not User.query.filter_by(email=username_email.data.lower()).first():
    #             raise ValidationError('This email is not registered.')
    #     else:
    #         if not User.query.filter_by(username=username_email.data.lower()).first():
    #             raise ValidationError('This username is not registered.')


class ContactUs(FlaskForm):
    """Constructor for the Contact Us Page"""
    # name = StringField('Full Name', validators=[DataRequired(), Length(1, 64)])
    # email = StringField('Email', validators=[DataRequired(),Email(), Length(1, 64)])
    subject = StringField('Subject of Inquiry', validators=[DataRequired(), Length(1, 64)])
    message = TextAreaField('Message')
    send_copy = BooleanField('Send me a copy of my message')
    submit = SubmitField('Send')


# class TopicTracker(FlaskForm):
#     """Constructor for the Categorical Writers  Subscription Form"""
#
#     username = StringField('What is your full name?', validators=[DataRequired()])
#     email = StringField('What is your email?', validators=[DataRequired(), Email()])
#     category = RadioField('Choose category of your interest:',
#                             validators=[InputRequired()],
#                             choices=[("AI","AI"), ("Crypto","Crypto"),("NFT","NFT"),
#                                      ("Economics","Economics"), ("Marketing","Marketing"), ("Philosophy","Philosophy")])
#
#     frequency = RadioField('How frequently do you want to receive updates?',
#                             validators=[InputRequired()],
#                             choices=[('_now','now'), ('_day', 'daily'), ('_week', 'weekly')])
#
#     submit = SubmitField('Submit')




