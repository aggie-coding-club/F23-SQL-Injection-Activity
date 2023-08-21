from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return "Starting point"


@app.route("/test")
def test():
    return render_template("index.html", title="tester", username="hungrymonkey")
