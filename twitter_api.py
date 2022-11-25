import pandas as pd
import numpy as np
import twitter_config
import tweepy as tweepy
from twitter_config import *
 
"""
    API hat gerade nur einen Suchterm, man kann hier aber beliebig andere Sachen einstellen,
    für den Anfang aber erst einmal nur das hier
""" 
class API:
    def __init__(self, search_term):
        self.search_term = search_term
        #Create a client and a search request for the API
        self.client = tweepy.Client(bearer_token = twitter_config.Bearer_Token)
        self.response = self.client.search_recent_tweets(self.search_term)
        #Create a dataframe of the Response with column of interest 'text' 
        self.df_api = pd.DataFrame(self.response.data)
        #tweet = df_api['text'].iloc[self.tweet_counter_api]
        # sollte auch so funktionieren, da in data_management definiert
        # self.df_api["my_label"] = np.nan
        # self.df_api["sentiment"] = np.nan
 
    tweet_counter_api = 0
    
    # shows the tweets inside of pandas df
    def save_dataset(self, name):
        self.df_api.to_csv(f'data/{name}.csv')
