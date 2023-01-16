# import all packages
import pandas as pd
import numpy as np
import re
from wordcloud import WordCloud
from nltk import FreqDist
import matplotlib.pyplot as plt

# all functions and variables specific to the climate change dataset


class ClimateChangeData():

    # Constructor
    def __init__(self, dataset_name):
         self.dataset_name = dataset_name
         # dataset that got chosen
         self.df_climate = pd.read_csv(f'data/{dataset_name}')
         # preprocessing steps for the dataset
         self.df_climate = self.preprocessing(self.df_climate)
         # tweet counter variable
         self.tweet_counter_climate = 0
     

    def preprocessing(self, dataset):
        self.dataset = dataset
        # create column for our own labels --> only if it does not already exist
        if 'my_label' not in self.dataset:
            self.dataset['my_label'] = np.nan
        # rename the column text to message coming from the twitter api
        if 'text' in self.dataset:
            self.dataset = self.dataset.rename({'text': 'message'}, axis=1)
        if 'id' in self.dataset:
            self.dataset = self.dataset.rename({'id': 'tweetid'}, axis=1)
        # when the dataset comes from the api, then we dont have the sentiment attribute
        if 'sentiment' not in self.dataset:
            self.dataset['sentiment'] = np.nan
        # new column so that the active learning model methods work properly
        if 'trained_on' not in self.dataset:
            self.dataset['trained_on'] = np.zeros(len(self.dataset))
        # create an index column
        if 'df_index' not in self.dataset:
            self.dataset['df_index'] = self.dataset.index
        # if we get an empty text then we delete the row
        self.dataset = self.dataset.dropna(subset='message')
        # preprocess the hashtags if not done before
        self.dataset['hashtag'] = self.dataset['message'].apply(lambda x: re.findall(r"#(\w+)", x)).astype('str')
        return self.dataset

    # shows the tweets inside of pandas df
    def show_tweets(self):
        tweet = self.df_climate['message'].iloc[self.tweet_counter_climate]
        sentiment = self.df_climate['sentiment'].iloc[self.tweet_counter_climate]
        my_label = self.df_climate['my_label'].iloc[self.tweet_counter_climate]
        user_username = self.df_climate['user_username'].iloc[self.tweet_counter_climate]
        user_name = self.df_climate['user_name'].iloc[self.tweet_counter_climate]
        created_at = self.df_climate['created_at'].iloc[self.tweet_counter_climate] 
        retweet_count = self.df_climate['retweet_count'].iloc[self.tweet_counter_climate] 
        quote_count = self.df_climate['quote_count'].iloc[self.tweet_counter_climate] 
        like_count = self.df_climate['like_count'].iloc[self.tweet_counter_climate] 
        profile_urls = self.df_climate['profile_urls'].iloc[self.tweet_counter_climate] 
        return tweet, sentiment, my_label, user_username, user_name, created_at, retweet_count, quote_count,\
               like_count, profile_urls

    # shows the tweets inside of pandas df
    def show_most_liked_tweets(self):
        df_most_liked = self.df_climate.iloc[[np.argmax(self.df_climate['like_count'])]].head(1)
        tweet = df_most_liked['message'].iloc[0]
        sentiment = df_most_liked['sentiment'].iloc[0]
        my_label = df_most_liked['my_label'].iloc[0]
        user_username = df_most_liked['user_username'].iloc[0]
        user_name = df_most_liked['user_name'].iloc[0]
        created_at = df_most_liked['created_at'].iloc[0]
        retweet_count = df_most_liked['retweet_count'].iloc[0]
        quote_count = df_most_liked['quote_count'].iloc[0]
        like_count = df_most_liked['like_count'].iloc[0]
        profile_urls = df_most_liked['profile_urls'].iloc[0]
        return tweet, sentiment, my_label, user_username, user_name, created_at, retweet_count, quote_count,\
               like_count, profile_urls
    
    # shows the full dataset inside of pandas df
    def show_full_dataset(self):
        rows = self.df_climate.iloc[0:]
        rows = list(rows.itertuples(index=False))
        return rows

    # puts the users label into the my_label column
    def label(self, label):
        self.df_climate.loc[self.tweet_counter_climate, 'my_label'] = label

    # overwrite the self.dataset with the newly ordered dataset after active learning
    def change_dataset(self, new_dataset):
        self.df_climate = new_dataset

    # overwrite the old dataset with the newly labeled data
    def save_results(self, dataset_name):
        self.df_climate.to_csv(f'data/{dataset_name}', index=False)

    # all labeled values will be put to the end of the dataframe
    def sort_dataframe(self):
        self.df_climate = self.df_climate.sort_values('my_label',na_position='first')

    """ 
    create a wordcloud based on the hashtags of the tweets
    the wordcloud is then saved into static/plots
    Challenge: Calculating the WordClouds takes too long
    Possible Solution for the Future: 
    Have a Calculate WordCloud Button at the Training Tab OR
    Do a Background Calculation for the WordCloud OR
    Calculate it once and then just load it from the plots folder
    """

    def create_wordcloud(self):
        # hashtags to list
        hashtags = self.df_climate['hashtag'].tolist()
        # clean up the hashtag list
        hashtags_clean = list()
        for hashtag in hashtags:
            hashtag = hashtag.replace('[','')
            hashtag = hashtag.replace(']','')
            hashtag = hashtag.replace("'",'')
            hashtag = hashtag.replace(" ",'')
            hashtag = hashtag.lower()
            hashtag = hashtag.split(',')
            hashtags_clean.append(hashtag)
        # flatten the list
        flat_list = [item for sublist in hashtags_clean for item in sublist if item]    
        # create a wordcloud to be shown on the analysis page
        # Frequency of words
        fdist = FreqDist(flat_list)
        # WordCloud save as a file
        # plot it
        # WordCloud
        wc = WordCloud(width=800, height=400,
                       max_words=50).generate_from_frequencies(fdist)
        # save the wordcloud
        image = wc.to_image()
        image.save('./static/plots/wordcloud.png')
