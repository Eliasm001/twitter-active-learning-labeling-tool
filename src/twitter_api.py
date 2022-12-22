import pandas as pd
import numpy as np
from .twitter_config import *
import tweepy as tweepy
from datetime import datetime
import datetime
 
"""
    API hat gerade nur einen Suchterm, man kann hier aber beliebig andere Sachen einstellen,
    für den Anfang aber erst einmal nur das hier
""" 
class API:
    def __init__(self, search_term, language, start, end, max_results):
        # Suchbegriff für den Tweet
        self.language = str(language)           #Gerade en oder de
        self.start = datetime.datetime.strptime(start, '%Y-%m-%d')  #Format Muss passend sein zu dem was aus dem Frontend kommt
        self.end = datetime.datetime.strptime(end, '%Y-%m-%d')      #Format Muss passend sein zu dem was aus dem Frontend kommt
        self.max_results = int(max_results)     # Limit von 100 (kann auch umgangen werden, muss noch hinzugefügt werden)
        # Create a datetime instance
        datetimeInstance = datetime.datetime.today()       
        # Get only the date instance from datetime instance
        self.creation = datetimeInstance.date() # Könnte man zum file Name hinzufügen
        self.search_term = search_term
        #Create a query
        query = self.search_term +' lang:' + self.language
        #Create a client and a search request for the API
        self.client = tweepy.Client(bearer_token = Bearer_Token)
        self.response = self.client.search_recent_tweets(query, start_time=self.start, end_time=self.end, max_results=self.max_results)
        #Create a dataframe of the Response with column of interest 'text' 
        self.df_api = pd.DataFrame(self.response.data)
        #tweet = df_api['text'].iloc[self.tweet_counter_api]
        # sollte auch so funktionieren, da in data_management definiert
        # self.df_api["my_label"] = np.nan
        # self.df_api["sentiment"] = np.nan
 
    tweet_counter_api = 0
    
    # shows the tweets inside of pandas df
    def save_dataset(self):
        self.df_api.to_csv(f'data/{self.search_term}_{self.language}_{self.max_results}_{self.creation}.csv')
