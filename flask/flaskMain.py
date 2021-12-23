from flask import Flask, render_template
import sys

sys.path.insert(0, "../emailValidity")
import emailValidity

app = Flask(__name__,template_folder='HTML')

@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/everify")
def everify():
    file = "../flask/static/ChoiceNYjournalists.csv"  # did not make the proper name
    valid = emailValidity.emailValidation(filename=file,
                                          type="csv", debug=True, multi=True)
    valid.check(save=True)
    return "Done"


if __name__ == '__main__':
    app.run(debug=True)