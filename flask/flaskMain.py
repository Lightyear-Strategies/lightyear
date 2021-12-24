from flask import Flask, render_template
from utils import *

import sys
sys.path.insert(0, "../emailValidity") # to import emailValidity.py
import emailValidity

app = Flask(__name__,template_folder='HTML')

@app.route("/")
def welcome():
    return render_template('welcome.html')


@app.route("/everify")
@timethis
def emailVerify():

    file = "../flask/static/ChoiceNYjournalists.csv" #"../emailValidity/test.csv"
    saveLocation = None #"../flask/results/"

    valid = emailValidity.emailValidation(filename=file,type="csv", debug=True, multi=True)
    valid.check(save=True,saveLocation=saveLocation)
    return render_template('repeat.html')


if __name__ == '__main__':
    app.run(debug=True)