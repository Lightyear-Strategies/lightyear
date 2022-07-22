import os
from flask import render_template, request, redirect
from flask_login import login_required
from werkzeug.utils import secure_filename
from flask_app.scripts.EmailValidator import ev_API, emailReport
from flask_app.scripts.googleAuth import authCheck, localServiceBuilder
from flask_app.scripts.config import Config
from flask_app.scripts.create_flask_app import init_celery, app


celery = init_celery(app)

@login_required
def email_validator():

    """
    Gets information from the form, extracts files.
    Sends files to Celery via SQS broken for background email verification.
    Redirects to authentication if bot is not logged in
    @param:    None
    @return:   Email Verification Page
    """
    if request.method == 'POST':  # form.validate_on_submit():
        filenames = []

        files = request.files
        email = request.form.get('email')
        print(email)

        if Config.ENVIRONMENT == 'server':
            if not authCheck():
                return redirect('/authorizeCheck')
        elif Config.ENVIRONMENT == 'local':
            localServiceBuilder()

        if files:
            for file in files:
                filename = secure_filename(files.get(file).filename) #.filename
                print(filename)
                #file.save(os.path.join(Config.UPLOAD_DIR, filename))
                files.get(file).save(os.path.join(Config.UPLOAD_DIR, filename))
                filenames.append(filename)

            for filename in filenames:
                # Celery
                # parse,remove file, send updated file
                # delay is from celery, test and see whether it would give an error
                pass

                ### Comment it out for now ###
                parseSendEmail.delay(os.path.join(Config.UPLOAD_DIR, filename), email, filename)
            #print('Here')

            return render_template('OnSuccess/EmailSent.html')

        else:
            print('No files')

    return render_template('emailValidator.html')



def emailVerify(path, recipients=None):
    print('emailVerify')
    """
    Uses functions from ev_API.py to verify emails.
    Creates email with processed file and sends it.
    @param:    path to file with emails
    @param:    recipients of processed file
    @return:   None
    """
    email = ev_API.emailValidation(filename=path)
    email.validation(save=True)
    subject_line = os.path.basename(path)
    report = emailReport.report("george@lightyearstrategies.com", recipients,
                                "Verified Emails in '%s' file" % subject_line, "Here is your file", path,"me")
    report.sendMessage()


@celery.task(name='ev_flask_functions.parseSendEmail')
def parseSendEmail(path, recipients=None, filename=None):
    print('parseSendEmail')
    """
    Celery handler
    @param:    path to file with emails
    @param:    recipients of processed file
    @param:    filename
    @return:   None
    """

    with app.app_context():
        emailVerify(path, recipients)

        # remove the file after sending it
        file_remover(os.path.join(Config.UPLOAD_DIR, filename))


def file_remover(path):
    print('file_remover')
    if os.path.exists(path):
        os.remove(path)
        print("The file has been deleted successfully")
    else:
        print("The file does not exist!")