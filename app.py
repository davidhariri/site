from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "This is running on my home's server"