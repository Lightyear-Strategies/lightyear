###################### Imports ######################

from flask import Flask, render_template,request
from werkzeug.utils import secure_filename
from utils import *
import emailReport

import os
import sys

# is there a way to do just import?
sys.path.insert(0, "../emailValidity") # to import emailValidity.py
import emailValidity

UPLOAD_FOLDER = '../flask/uploadFolder'
ALLOWED_EXTENSIONS = {'.csv','.xlsx'}

###################### Flask ######################

app = Flask(__name__,template_folder='HTML')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


###################### Functions ######################

@app.route('/')
def upload_file():
    return render_template('upload.html')

#
# Implement:
# 1) check the extension of the file
# 2) remove the file right after it's sent
#
@app.route('/', methods=['POST'])
def upload_files():
    #ulpoad file and read it flask

    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        print(file_ext)
        if file_ext not in ALLOWED_EXTENSIONS:  # possibly check whether the file is actually csv??
            abort(400)                                  # https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
                                                # def validate_image(stream): ?

        path = os.path.join(UPLOAD_FOLDER, filename)
        uploaded_file.save(path)
    return emailVerify(path)
    #return redirect(url_for('index'))

#@timethis #wrapper
def emailVerify(path, recepients=None):

    valid = emailValidity.emailValidation(filename=path,type="csv", debug=True, multi=True)
    valid.check(save=True, inplace=True)

    report = emailReport.report("chris@lightyearstrategies.com", "chris@lightyearstrategies.com",
                       "this is the subject line", "This is the message body", path,
                       "me")
    report.sendMessage()

    return render_template('repeat.html') # send to email


if __name__ == '__main__':
    app.run(debug=True)