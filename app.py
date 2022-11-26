# import the packages
from flask import Flask, render_template, request
from data_management import ClimateChangeData
import os
from twitter_api import API

# initialize the flask framework
app = Flask(__name__)

# which dataset did we choose? --> existing or fresh?

@app.route("/")
def hello_world():
    # list all of the existing datasets so that a user can choose which to label
    datasets = os.listdir('./data/')
    #print(datasets)
    return render_template("index.html", datasets=datasets)

"""
Handle the user input, which dataset he wants to choose
Ultimately, the chosen data frame will be the input argument for the methods
in functionality.py in order to decide which DataFrame to load
"""
@app.route('/choose_dataset',methods = ['POST', 'GET'])
def choose_dataset():
   if request.method == 'POST':
       global dataset_name
       dataset_name = request.form['which_dataset']
       print(dataset_name)
       # create an instance of the ClimateChangeData Class to interact with its methods
       # make it global so that it can be accessed from outside of the function
       global Climate
       Climate = ClimateChangeData(dataset_name)         
       print(dataset_name)
       msg = "hinzugefügt."               
       tweet, sentiment, my_label = Climate.show_tweets() 
       return render_template("labeling.html", tweet=tweet, sentiment=sentiment, my_label=my_label)
       

"""
This lets the user interact with the twitter api
The user can create a new dataset, choosing from a set of config parameters when prompted:
- search term
- language?!
- recency
- number of tweets
...?
"""       

@app.route("/search", methods=["POST"])
def search():
    #retrieving data from the form
    search_term = request.form["search_term"]
    # initialize API class
    #create a search instance and pass the search term
    global api
    api = API(search_term)
    # saves the dataset with the users specified parameters
    api.save_dataset(name=search_term) 
    #Return DataFrame to the Labeling HTML
    # list all of the existing datasets including the freshly created dataset
    # so that a user can choose which to label
    datasets = os.listdir('./data/')
    #print(datasets)
    return render_template("index.html", datasets=datasets)


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
Overwrite the current climate change csv file with the user labeled data
JSON will request this function with an AJAX request
This function still needs to be modified in functionality.py in order to work properly
"""
@app.route("/save_results")
def save_results():
    Climate.save_results(dataset_name=dataset_name)
    print('Hello')
    return ""

"""
This page does ...
"""

@app.route("/analysis")
def analysis():
    # display the full dataset
    rows = Climate.show_full_dataset()
    # create the wordcloud plot --> in static/plots
    Climate.create_wordcloud()
    return render_template("analysis.html", rows=rows)

"""
This page does ...
"""

@app.route("/training")
def training():
    return render_template("training.html")


if __name__ == '__main__':
    app.run(debug=True)