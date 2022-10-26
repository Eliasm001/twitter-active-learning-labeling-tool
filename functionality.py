# import all packages
import pandas as pd

# all functions and variables specific to the climate change dataset
class ClimateChangeData():

    # climate change daten
    df_climate = pd.read_csv('data/twitter_sentiment_data.csv')

    # tweet counter variable
    tweet_counter_climate = 0

    # shows the tweets inside of pandas df
    def show_tweets(self):
        tweet = self.df_climate['message'].iloc[self.tweet_counter_climate]
        return tweet