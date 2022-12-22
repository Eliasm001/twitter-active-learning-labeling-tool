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
        self.response = self.client.search_recent_tweets(query, start_time=self.start, end_time=self.end,\
                            max_results=self.max_results, tweet_fields = ['created_at', 'public_metrics'],\
                            expansions = ['author_id'],user_fields = ['profile_image_url'])
        # get the user information
        self.users = self.response.includes['users'] #Ersetzen der 1 mit dem tweet counter 
        self.profile_urls = list()
        self.user_username = list()
        self.user_name = list()
        self.user_ids = list()
        for user in self.users:
            self.profile_urls.append(user.profile_image_url)
            self.user_username.append(user.username)
            self.user_name.append(user.name)
            self.user_ids.append(user.id)
        # df with the user data (only unique users)
        self.df_users = pd.DataFrame({'profile_urls':self.profile_urls, 'user_username':self.user_username,\
                                 'user_name':self.user_name, 'user_ids':self.user_ids})
        #Create a dataframe of the Response with column of interest 'text' 
        self.df_api = pd.DataFrame(self.response.data)
        # format the public information feature and add the new columns
        self.df_api_merged = self.df_api.merge(self.df_api['public_metrics'].apply(pd.Series),left_index=True, right_index=True)\
            .drop('public_metrics',axis=1)
        # combine the tweet df with the user df
        self.df_api_users_merge = self.df_api_merged.merge(self.df_users, left_on='author_id', right_on='user_ids')
        

 
    tweet_counter_api = 0
    
    # shows the tweets inside of pandas df
    def save_dataset(self):
        self.df_api_users_merge.to_csv(f'data/{self.search_term}_{self.language}_{self.max_results}_{self.creation}.csv')
