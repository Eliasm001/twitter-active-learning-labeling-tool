# import all packages
import pandas as pd
import numpy as np

# all functions and variables specific to the climate change dataset
class ClimateChangeData():

    # climate change daten
    df_climate = pd.read_csv('data/twitter_sentiment_data.csv')

    # create column for our own labels
    df_climate['my_label'] = np.nan

    # tweet counter variable
    tweet_counter_climate = 0

    # shows the tweets inside of pandas df
    def show_tweets(self):
        tweet = self.df_climate['message'].iloc[self.tweet_counter_climate]
        sentiment = self.df_climate['sentiment'].iloc[self.tweet_counter_climate]
        my_label = self.df_climate['my_label'].iloc[self.tweet_counter_climate]
        return tweet, sentiment, my_label

    # puts the users label into the my_label column
    def label(self, label):
        self.df_climate.loc[self.tweet_counter_climate,'my_label'] = label

    # def save_results(self):
    #     pd.to_csv('data/twitter_sentiment_data.csv')