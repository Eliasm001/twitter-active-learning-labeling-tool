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


        '''
        Receive the data from the Frontend and save into the search instance. 
        Then build a search query for the API
        '''
        self.language = str(language)
        self.start = datetime.datetime.strptime(start, '%Y-%m-%d')
        self.end = datetime.datetime.strptime(end, '%Y-%m-%d')   
        self.max_results = int(int(max_results)/10)
        self.max_results_original = max_results
        self.search_term = search_term
        #Create a query
        query = self.search_term +' lang:' + self.language + ' -is:retweet'



        '''
        Get the date, from when the API request was made
        '''
        # Create a datetime instance
        datetimeInstance = datetime.datetime.today()       
        # Get only the date instance from datetime instance
        self.creation = datetimeInstance.date() # Könnte man zum file Name hinzufügen
        #Create a client and a search request for the API

        '''
        Create an instance of a client to access the data through the Twitter API and get the data (Tweetfields) and the special fields (Userfields)
        '''
        client = tweepy.Client(bearer_token= Bearer_Token)

        data = list()
        includes = list()

        Paginator = tweepy.Paginator(client.search_recent_tweets,
                                    query=query, 
                                    start_time=self.start,
                                    end_time=self.end,
                                    max_results=10, 
                                    expansions='author_id',
                                    tweet_fields=['created_at', 'public_metrics'],
                                    user_fields=['username', 'profile_image_url'],
                                    limit = self.max_results
                                    )

        for response in Paginator:
            data.append(response.data)
            includes.append(response.includes)



    
        '''
        Extract the Twitter User data from the response of the client
        '''
        users = list()

        for i, page in enumerate(Paginator):
            users.append(includes[i]['users'])

        self.users = [item for sublist in users for item in sublist]


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




        '''
        Extract the Twitter User data from the response of the client
        '''
        self.data = [item for sublist in data for item in sublist]
        #Create a dataframe of the Response with column of interest 'text' 
        self.df_api = pd.DataFrame(self.data)
        # format the public information feature and add the new columns




        '''
        Merge The Response into a single DataFrame
        '''
        self.df_api_merged = self.df_api.merge(self.df_api['public_metrics'].apply(pd.Series),left_index=True, right_index=True)\
            .drop('public_metrics',axis=1)
        # combine the tweet df with the user df
        self.df_api_users_merge = self.df_api_merged.merge(self.df_users, left_on='author_id', right_on='user_ids')
        

 
    tweet_counter_api = 0
    
    # shows the tweets inside of pandas df
    def save_dataset(self):
        self.df_api_users_merge.to_csv(f'data/{self.search_term}_{self.language}_{self.max_results_original}_{self.creation}.csv')
