# import all packages
import pandas as pd
import numpy as np

# all functions and variables specific to the climate change dataset
class ClimateChangeData():

    # Constructor
    def __init__(self, dataset):
         self.dataset = dataset
         # dataset that got chosen
         self.df_climate = pd.read_csv(f'data/{dataset}')
         # create column for our own labels --> only if it does not already exist
         if 'my_label' not in self.df_climate:
             self.df_climate['my_label'] = np.nan
     

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

    # overwrite the old dataset with the newly labeled data
    def save_results(self):
        self.df_climate.to_csv(f'data/{self.dataset}')