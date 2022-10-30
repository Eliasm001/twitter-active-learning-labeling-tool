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
    def __init__(self, dataset):
         self.dataset = dataset
         # dataset that got chosen
         self.df_climate = pd.read_csv(f'data/{dataset}')
         # create column for our own labels --> only if it does not already exist
         if 'my_label' not in self.df_climate:
             self.df_climate['my_label'] = np.nan
         # preprocess the hashtags if not done before
         self.df_climate['hashtag'] = self.df_climate['message'].apply(lambda x: re.findall(r"#(\w+)", x))
     

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
        self.df_climate.to_csv(f'data/{self.dataset}', index=False)

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
        print(hashtags)
        # flatten the list
        flat_list = [item for sublist in hashtags for item in sublist]    
        # create a wordcloud to be shown on the analysis page
        #Frequency of words
        fdist = FreqDist(flat_list)
        # WordCloud save as a file
        wc = WordCloud(width=800, height=400, max_words=50).generate_from_frequencies(fdist)
        # plot it
        #WordCloud
        wc = WordCloud(width=800, height=400, max_words=50).generate_from_frequencies(fdist)
        # save the wordcloud 
        image = wc.to_image()
        image.save('./static/plots/wordcloud.png')   
       
        
        

