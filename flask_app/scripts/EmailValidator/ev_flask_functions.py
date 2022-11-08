import os
from flask import render_template, request, redirect, send_file, g
from flask_login import login_required
from werkzeug.utils import secure_filename
from flask_app.scripts.EmailValidator import ev_API, emailReport
from flask_app.scripts.googleAuth import authCheck, localServiceBuilder
from flask_app.scripts.config import Config
from flask_app.scripts.create_flask_app import app#, init_celery,


#celery = init_celery(app)

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
        #print(email)

        if Config.ENVIRONMENT == 'server':
           if not authCheck():
               return redirect('/authorizeCheck')
        elif Config.ENVIRONMENT == 'local':
           localServiceBuilder()

        if files:
            filename = secure_filename(files.get('file').filename) #.filename
            #file.save(os.path.join(Config.UPLOAD_DIR, filename))
            orig_path = os.path.join(Config.UPLOAD_DIR, filename)
            files.get('file').save(orig_path)
            filenames.append(filename)

            # Celery
            # parse,remove file, send updated file
            # delay is from celery, test and see whether it would give an error
            # parseSendEmail.delay(os.path.join(Config.UPLOAD_DIR, filename), email, filename)

            final_path, mimetype, attachment_filename, as_attachment = parseSendEmail(orig_path, email, filename)
            # remove the file after sending it
            @app.after_request
            def delete(response):
                file_remover(final_path)
                return response

            print('Sending File')
            print(final_path)
            return send_file(final_path,
                             mimetype=mimetype,
                             attachment_filename=attachment_filename,
                             as_attachment=as_attachment)

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

    return path,'text/csv', subject_line,True # path, mimetype, attachment_filename, as_attachment)

    # report = emailReport.report(Config.SENDER_EMAIL_NAME, recipients,
    #                             "Verified Emails in '%s' file" % subject_line, "Here is your file", path,"me")
    # report.sendMessage()


# @celery.task(name='ev_flask_functions.parseSendEmail')
def parseSendEmail(path, recipients=None, filename=None):
    print('parseSendEmail')
    # """
    # Celery handler
    # @param:    path to file with emails
    # @param:    recipients of processed file
    # @param:    filename
    # @return:   None
    # """

    with app.app_context():
        return emailVerify(path, recipients)


def file_remover(path):
    #print('file_remover')
    if os.path.exists(path):
        os.remove(path)
        print("The file has been deleted successfully")
    else:
        print("The file does not exist!")