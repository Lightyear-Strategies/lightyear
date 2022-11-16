import os
from flask import render_template, request, send_file
from flask_login import login_required
from werkzeug.utils import secure_filename
from flask_app.scripts.EmailValidator import ev_API
from flask_app.scripts.config import Config
from flask_app.scripts.create_flask_app import app


@login_required
def email_validator():

    """
    Gets information from the form, extracts files.
    Sends files to Celery via SQS broken for background email verification.
    Redirects to authentication if bot is not logged in
    @param:    None
    @return:   Email Verification Page
    """
    if request.method == 'POST':
        filenames = []

        files = request.files

        if files:
            filename = secure_filename(files.get('file').filename)
            orig_path = os.path.join(Config.UPLOAD_DIR, filename)
            files.get('file').save(orig_path)
            filenames.append(filename)

            final_path, mimetype, attachment_filename, as_attachment = parseSendEmail(orig_path, filename)
            # remove the file after sending it
            @app.after_request
            def delete(response):
                file_remover(final_path.split(".")[0]+"_final.csv")
                return response

            # print('Sending File')
            # print(final_path.split(".")[0]+"_final.csv")
            return send_file(final_path.split(".")[0]+"_final.csv",
                             mimetype=mimetype,
                             attachment_filename=attachment_filename,
                             as_attachment=as_attachment)

        else:
            print('No files')

    return render_template('emailValidator.html')



def emailVerify(path):
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

    return path, 'text/csv', subject_line, True # path, mimetype, attachment_filename, as_attachment)



def parseSendEmail(path):
    print('parseSendEmail')

    with app.app_context():
        return emailVerify(path)


def file_remover(path):
    #print('file_remover')
    if os.path.exists(path):
        os.remove(path)
        print("The file has been deleted successfully")
    else:
        print("The file does not exist!")