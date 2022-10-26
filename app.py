from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/labeling")
def labeling():
    return render_template("labeling.html")


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


@app.route("/training")
def training():
    return render_template("training.html")
