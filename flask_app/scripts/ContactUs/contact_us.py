from flask import render_template, request, redirect
from flask_app.scripts.EmailValidator import  emailReport
from flask_app.scripts.googleAuth import authCheck, localServiceBuilder
from flask_app.scripts.forms import ContactUs
from flask_app.scripts.config import Config
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
            name = form.name.data
            email = form.email.data
            subject = 'Contact Us: ' + form.subject.data
            recipients = Config.CONTACT_US_RECIPIENTS
            #print(request.form.get('send_copy'))
            copy = True if request.form.get('send_copy') else False

            if copy:
                recipients.append(email)

            message = f'''\nFrom: {name} — {email}
            \n{form.message.data}
            '''

            if Config.ENVIRONMENT == 'server':
                print('in server config environment')
                if not authCheck():
                    print('trying to get authcheck')
                    return redirect('/authorizeCheck')
            elif Config.ENVIRONMENT == 'local':
                localServiceBuilder()

            report = emailReport.report("george@lightyearstrategies.com", recipients, subject, message)
            report.sendMessage()
            return render_template('OnSuccess/EmailSent.html')

        except Exception:
            traceback.print_exc()
            return render_template('ErrorPages/500.html')

    return render_template('contactUs.html', form=form, name=name, email=email,
                           message=message, subject=subject, copy=copy)