from flask import render_template, request, session
from flask_app.scripts.EmailValidator import  emailReport
from flask_app.scripts.forms import ContactUs
from flask_app.scripts.config import Config
from flask_app.scripts.create_flask_app import mp
import traceback


def contact_us():

    """
    Gets information from the form, extracts files.
    Sends files to Celery via SQS broken for background email verification.
    Redirects to authentication if bot is not logged in
    @param:    None
    @return:   config page
    """
    name = None
    email = None
    subject = None
    message = None
    copy = None
    form = ContactUs()
    if form.validate_on_submit():
        try:
            name = session['name'].capitalize() #form.name.data
            email = session['email'] #form.email.data
            subject = 'Contact Us: ' + form.subject.data
            recipients = Config.CONTACT_US_RECIPIENTS
            #print(request.form.get('send_copy'))
            copy = True if request.form.get('send_copy') else False

            mp.track(session['email'], 'Used Contact Us', {'subject': subject, 'message': form.message.data, 'session_id': request.cookies.get('session')})

            # print(email)

            if copy:
                recipients.append(email)

            message = f'''\nFrom: {name} — {email}
            \n{form.message.data}
            '''

            report = emailReport.report(Config.SENDER_EMAIL_NAME, recipients, subject, message)
            report.sendMessage()
            return render_template('OnSuccess/EmailSent.html')

        except Exception:
            traceback.print_exc()
            return render_template('ErrorPages/500.html')
    mp.track(session['email'], 'Viewed Contact Us', {'session_id': request.cookies.get('session')})

    return render_template('contactUs.html', form=form, message=message, subject=subject, copy=copy)