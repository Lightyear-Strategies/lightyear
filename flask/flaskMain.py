from flask import Flask
import sys
sys.path.insert(0, "/Users/rutkovskii/lightyear/emailValidity")
import emailValidity

app = Flask(__name__)

#site_link = "http://localhost/5000/"

pages = "http://127.0.0.1:5000/hello \n http://127.0.0.1:5000/everify"
@app.route("/")
def welcome():
    return(pages)

@app.route("/hello")
def hello():
    return("hello")

@app.route("/everify2")
def everify2():
    emailValidity.checkAndSave("/Users/rutkovskii/lightyear/emailValidity/test.csv", debug=True, type="csv")
    return "Done"

@app.route("/everify")
def everify():
    csv = "/Users/rutkovskii/lightyear/flask/static/ChoiceNYjournalists.csv"
    save_path = "/Users/rutkovskii/lightyear/flask/results/"
    emailValidity.checkAndSave2(csv,save_path, debug=True, type="csv")
    return "Done"


if __name__ == '__main__':
    app.run(debug=True)