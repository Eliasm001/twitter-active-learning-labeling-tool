# import the packages
from flask import Flask, render_template
from functionality import ClimateChangeData

# initialize the flask framework
app = Flask(__name__)

# create an instance of the ClimateChangeData Class to interact with its methods
Climate = ClimateChangeData()

@app.route("/")
def hello_world():
    return render_template("index.html")

"""
This page gives the user a UI to label his datasets.
It works as follows: 
    -
    -
    -
"""
@app.route("/labeling")
def labeling():
    # the current tweet
    tweet = Climate.show_tweets()
    return render_template("labeling.html", tweet = tweet)

"""
This function gets triggered by the java script function called next_tweet
"""
@app.route('/next_tweet')
def SomeFunction():
    print('next_tweet')
    Climate.tweet_counter_climate += 1
    next_tweet = Climate.show_tweets()
    return render_template('labeling.html',next_tweet=next_tweet)

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


@app.route("/training")
def training():
    return render_template("training.html")
