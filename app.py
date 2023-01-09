# import the packages
from flask import Flask, render_template, request, flash, redirect
from src.data_management import ClimateChangeData
import os
from src.twitter_api import API
from src.active_learning import Active_Learner
import pandas as pd
from flask_socketio import SocketIO, emit

# initialize the flask framework
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
# we need that now for flask flash
app.secret_key = "super secret key"
# initialize the socket
socketio = SocketIO(app)

# which dataset did we choose? --> existing or fresh?
@app.route("/")
def hello_world():
    # list all of the existing datasets so that a user can choose which to label
    datasets = os.listdir('./data/')
    # print(datasets)
    return render_template("index.html", datasets=datasets)


"""
Handle the user input, which dataset he wants to choose
Ultimately, the chosen data frame will be the input argument for the methods
in functionality.py in order to decide which DataFrame to load
"""


@app.route('/choose_dataset', methods=['POST', 'GET'])
def choose_dataset():
   if request.method == 'POST':
       global dataset_name
       dataset_name = request.form['which_dataset']
       print(dataset_name)
       # create an instance of the ClimateChangeData Class to interact with its methods
       # make it global so that it can be accessed from outside of the function
       global Climate
       Climate = ClimateChangeData(dataset_name)
       # the already labeled tweets should go to the back of the df
       Climate.sort_dataframe()         
       print(dataset_name)
       # boolean whether we have already labeled this tweet
       labeled_pro = False       
       labeled_anti = False 
       labeled_neutral = False 
       labeled_news = False         
       tweet, sentiment, my_label, user_username, user_name, created_at, retweet_count, quote_count,\
       like_count, profile_urls = Climate.show_tweets()
       # counts to integers
       like_count = int(like_count)
       retweet_count = int(retweet_count)
       quote_count = int(quote_count) 
       # process the date when the tweet was created
       created_at = pd.to_datetime(created_at).strftime("%I:%M%p · %b %d, %Y ·")
       # if we have al label for this tweet, than we already color the symbol accordingly
       if my_label==1:
           labeled_pro = True
       elif my_label==-1:
           labeled_anti = True
       elif my_label==0:
           labeled_neutral = True
       elif my_label==2:
           labeled_news = True
       return render_template("labeling.html", tweet=tweet, sentiment=sentiment, my_label=my_label,\
         labeled_pro=labeled_pro, labeled_anti=labeled_anti, labeled_neutral=labeled_neutral, labeled_news=labeled_news,\
         user_username=user_username, user_name=user_name, created_at=created_at, retweet_count=retweet_count,\
         quote_count=quote_count,like_count=like_count,profile_urls=profile_urls)
       

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
    # retrieving data from the form
    search_term = request.form["search_term"]
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]
    language = request.form["language"]
    max_results = request.form["max_results"]
    # initialize API class
    # create a search instance and pass the search term
    global api
    api = API(search_term, language=language, start=start_time,
              end=end_time, max_results=max_results)
    # saves the dataset with the users specified parameters
    api.save_dataset()
    # Return DataFrame to the Labeling HTML
    # list all of the existing datasets including the freshly created dataset
    # so that a user can choose which to label
    datasets = os.listdir('./data/')
    # print(datasets)
    return render_template("index.html", datasets=datasets)


"""
User gets routed here when he clicks on labeling in the menu bar
This page gives the user a UI to label his datasets.
It works as follows: 
    -
    -
    -
"""


@app.route("/labeling")
def labeling():
    # the current tweet
    tweet, sentiment, my_label, user_username, user_name, created_at, retweet_count, quote_count,\
       like_count, profile_urls = Climate.show_tweets()
    # process the date when the tweet was created
    created_at = pd.to_datetime(created_at).strftime("%I:%M%p · %b %d, %Y ·")
    # counts to integers
    like_count = int(like_count)
    retweet_count = int(retweet_count)
    quote_count = int(quote_count)
    # boolean whether we have already labeled this tweet
    labeled_pro = False       
    labeled_anti = False 
    labeled_neutral = False 
    labeled_news = False         
    # if we have al label for this tweet, than we already color the symbol accordingly
    if my_label == 1:
        labeled_pro = True
    elif my_label == -1:
        labeled_anti = True
    elif my_label == 0:
        labeled_neutral = True
    elif my_label == 2:
        labeled_news = True
    return render_template("labeling.html", tweet=tweet, sentiment=sentiment, my_label=my_label,\
         labeled_pro=labeled_pro, labeled_anti=labeled_anti, labeled_neutral=labeled_neutral, labeled_news=labeled_news,\
         user_username=user_username, user_name=user_name, created_at=created_at, retweet_count=retweet_count,\
         quote_count=quote_count,like_count=like_count,profile_urls=profile_urls)
"""
This function gets triggered by the java script function called next_tweet
"""


@app.route('/next_tweet')
def next_tweet():  
    print('next_tweet')
    print(len(Climate.dataset))
    print(type(len(Climate.dataset)))
    print(Climate.tweet_counter_climate)
    print(type(Climate.tweet_counter_climate))
    # tweet counter may not be larger than the df length
    if Climate.tweet_counter_climate == len(Climate.dataset)-1:
        flash('Dies ist der letzte Tweet')
        return redirect('/labeling')
    else:
        # point the indexer to the next tweet in the pandas df
        Climate.tweet_counter_climate += 1
        # show the next tweet
        tweet, sentiment, my_label, user_username, user_name, created_at, retweet_count, quote_count,\
        like_count, profile_urls = Climate.show_tweets() 
        # process the date when the tweet was created
        created_at = pd.to_datetime(created_at).strftime("%I:%M%p · %b %d, %Y ·")
        # counts to integers
        like_count = int(like_count)
        retweet_count = int(retweet_count)
        quote_count = int(quote_count)
        # boolean whether we have already labeled this tweet
        labeled_pro = False       
        labeled_anti = False 
        labeled_neutral = False 
        labeled_news = False         
        # if we have al label for this tweet, than we already color the symbol accordingly
        if my_label == 1:
            labeled_pro = True
        elif my_label == -1:
            labeled_anti = True
        elif my_label == 0:
            labeled_neutral = True
        elif my_label == 2:
            labeled_news = True
        return render_template("labeling.html", tweet=tweet, sentiment=sentiment, my_label=my_label,\
            labeled_pro=labeled_pro, labeled_anti=labeled_anti, labeled_neutral=labeled_neutral, labeled_news=labeled_news,\
            user_username=user_username, user_name=user_name, created_at=created_at, retweet_count=retweet_count,\
            quote_count=quote_count,like_count=like_count,profile_urls=profile_urls) 

"""
This function gets triggered by the java script function called previous_tweet
"""


@app.route('/previous_tweet')
def previous_tweet():
    print('previous_tweet')
    # tweet counter may not be smaller than 0 otherwise we get a bug with .iloc[-1]
    if Climate.tweet_counter_climate == 0:
        flash('Dies ist bereits der erste Tweet')
        return redirect('/labeling')
    else:
        # point the indexer to the next tweet in the pandas df
        Climate.tweet_counter_climate -= 1
        # show the next tweet
        tweet, sentiment, my_label, user_username, user_name, created_at, retweet_count, quote_count,\
        like_count, profile_urls = Climate.show_tweets()
        # process the date when the tweet was created
        created_at = pd.to_datetime(created_at).strftime("%I:%M%p · %b %d, %Y ·")
        # counts to integers
        like_count = int(like_count)
        retweet_count = int(retweet_count)
        quote_count = int(quote_count)
        # boolean whether we have already labeled this tweet
        labeled_pro = False       
        labeled_anti = False 
        labeled_neutral = False 
        labeled_news = False         
        # if we have al label for this tweet, than we already color the symbol accordingly
        if my_label == 1:
            labeled_pro = True
        elif my_label == -1:
            labeled_anti = True
        elif my_label == 0:
            labeled_neutral = True
        elif my_label == 2:
            labeled_news = True
        return render_template("labeling.html", tweet=tweet, sentiment=sentiment, my_label=my_label,\
            labeled_pro=labeled_pro, labeled_anti=labeled_anti, labeled_neutral=labeled_neutral, labeled_news=labeled_news,\
            user_username=user_username, user_name=user_name, created_at=created_at, retweet_count=retweet_count,\
            quote_count=quote_count,like_count=like_count,profile_urls=profile_urls) 

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
    return ('', 204)


@app.route("/manual_label_anti")
def manual_label_anti():
    Climate.label(-1)
    return ('', 204)


@app.route("/manual_label_neutral")
def manual_label_neutral():
    Climate.label(0)
    return ('', 204)


@app.route("/manual_label_news")
def manual_label_news():
    Climate.label(2)
    return ('', 204)


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
    # tweet mit den meisten likes
    tweet, sentiment, my_label, user_username, user_name, created_at, retweet_count, quote_count,\
    like_count, profile_urls = Climate.show_most_liked_tweets()
    # process the date when the tweet was created
    created_at = pd.to_datetime(created_at).strftime("%I:%M%p · %b %d, %Y ·")
    # counts to integers
    like_count = int(like_count)
    retweet_count = int(retweet_count)
    quote_count = int(quote_count)
    return render_template("analysis.html", tweet=tweet, sentiment=sentiment, my_label=my_label,\
        user_username=user_username, user_name=user_name, created_at=created_at, retweet_count=retweet_count,\
        quote_count=quote_count,like_count=like_count,profile_urls=profile_urls, rows=rows) 


"""
Loading screen for the training process
"""
@app.route("/loading_screen")
def loading_screen():
	return render_template('loading.html')


"""
This page does ...
"""


@app.route("/training")
def training():
    # create instance of active learner class
    AL = Active_Learner(dataset_name=Climate.dataset_name)
    # invoke the model training
    df_active_learning = AL.query()
    print(df_active_learning)
    # update the dataset with the new order
    Climate.dataset = df_active_learning.reset_index().drop('index', axis=1)
    # also update the self.dataset variable
    Climate.change_dataset(Climate.dataset)
    print('Climate:')
    print(Climate.dataset)
    print(Climate.dataset_name)
    # save the dataset
    Climate.save_results(Climate.dataset_name)
    return render_template("training.html")


if __name__ == '__main__':
    app.run(debug=True, threaded=True)