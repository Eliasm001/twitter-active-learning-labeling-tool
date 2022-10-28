# import the packages
from flask import Flask, render_template, request
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
    tweet, sentiment, my_label = Climate.show_tweets()
    return render_template("labeling.html", tweet = tweet, sentiment=sentiment, my_label=my_label)

"""
This function gets triggered by the java script function called next_tweet
"""
@app.route('/next_tweet')
def next_tweet():
    print('next_tweet')
    # point the indexer to the next tweet in the pandas df
    Climate.tweet_counter_climate += 1
    # show the next tweet
    tweet, sentiment, my_label = Climate.show_tweets()
    return render_template('labeling.html',tweet=tweet, sentiment=sentiment, my_label=my_label)

"""
This function gets triggered by the java script function called previous_tweet
"""
@app.route('/previous_tweet')
def previous_tweet():
    print('previous_tweet')
    # point the indexer to the next tweet in the pandas df
    Climate.tweet_counter_climate -= 1
    # show the next tweet
    tweet, sentiment, my_label = Climate.show_tweets()
    return render_template('labeling.html',tweet=tweet, sentiment=sentiment, my_label=my_label)

"""
After the user labeled a tweet, the label will be put into the my_label
column of the pandas DataFrame.
Then the next tweet will automatically be show (discuss whether this 
should be implemented or if the user should go to the next tweet by himself
or even to make it a setting that the user can take)
Currently we have four api calls for this --> make it less redundant by using best
practices in the future
"""

@app.route("/manual_label_pro")
def manual_label_pro():
    Climate.label(1)
    tweet, sentiment, my_label = Climate.show_tweets()
    return render_template('labeling.html',tweet=tweet, sentiment=sentiment, my_label=my_label)

@app.route("/manual_label_anti")
def manual_label_anti():
    Climate.label(-1)
    tweet, sentiment, my_label = Climate.show_tweets()
    return render_template('labeling.html',tweet=tweet, sentiment=sentiment, my_label=my_label)

@app.route("/manual_label_neutral")
def manual_label_neutral():
    Climate.label(0)
    tweet, sentiment, my_label = Climate.show_tweets()
    return render_template('labeling.html',tweet=tweet, sentiment=sentiment, my_label=my_label)

@app.route("/manual_label_news")
def manual_label_news():
    Climate.label(2)
    tweet, sentiment, my_label = Climate.show_tweets()
    return render_template('labeling.html',tweet=tweet, sentiment=sentiment, my_label=my_label)


"""
Handle the user input, which dataset he wants to choose
Ultimately, the chosen data frame will be the input argument for the methods
in functionality.py in order to decide which DataFrame to load
"""
@app.route('/choose_dataset',methods = ['POST', 'GET'])
def choose_dataset():
   if request.method == 'POST':
       try:
         dataset = request.form['choose_dataset']
         print(dataset)
         msg = "hinzugefügt."   
       except Exception as e: 
         msg = "nicht hinzugefügt. Überprüfen Sie Ihre Eingaben. " + str(e)
       finally: 
         tweet, sentiment, my_label = Climate.show_tweets() 
         return render_template("labeling.html", tweet=tweet, sentiment=sentiment, my_label=my_label)

"""
This page does ...
"""

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

"""
This page does ...
"""

@app.route("/training")
def training():
    return render_template("training.html")


if __name__ == '__main__':
    app.run(debug=True)