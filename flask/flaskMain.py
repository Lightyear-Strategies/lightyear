from flask import Flask

app = Flask(__name__)

site_link = "http://localhost/5000/"

@app.route("/hello")
def hello():
    print("hello")