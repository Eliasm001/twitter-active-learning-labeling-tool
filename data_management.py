# import all packages
import os
import pandas as pd
import numpy as np
import re
from wordcloud import WordCloud
from nltk import FreqDist
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_hub as hub
import transformers
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score as accuracy

# all functions and variables specific to the climate change dataset
class ClimateChangeData:

    # Constructor
    def __init__(self, dataset, model_name="prajjwal1/bert-tiny"):
        self.dataset = dataset
        self.model_name = model_name
        # dataset that got chosen
        self.df_climate = pd.read_csv(f"data/{dataset}")
        # create column for our own labels --> only if it does not already exist
        if "my_label" not in self.df_climate:
            self.df_climate["my_label"] = np.nan
        # create column to signal if it has already been used to train our model
        if "trained_on" not in self.df_climate:
            self.df_climate["trained_on"] = 0
        # preprocess the hashtags if not done before
        self.df_climate["hashtag"] = self.df_climate["message"].apply(
            lambda x: re.findall(r"#(\w+)", x)
        )
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
        # uses the corresponding finetuned model if available (else uses a new one from huggingfaces)
        if os.path.exists(f"models/{(model_name)}_{dataset}"):
            self.model = (
                transformers.TFAutoModelForSequenceClassification.from_pretrained(
                    f"models/{(model_name)}_{dataset}"
                )
            )
        else:
            # here we need to add a custom output layer for mutinomial classification
            self.model = (
                transformers.TFAutoModelForSequenceClassification.from_pretrained(
                    model_name, from_pt=True
                )
            )

    # tweet counter variable
    tweet_counter_climate = 0

    # shows the tweets inside of pandas df
    def show_tweets(self):
        tweet = self.df_climate["message"].iloc[self.tweet_counter_climate]
        sentiment = self.df_climate["sentiment"].iloc[self.tweet_counter_climate]
        my_label = self.df_climate["my_label"].iloc[self.tweet_counter_climate]
        return tweet, sentiment, my_label

    # puts the users label into the my_label column
    def label(self, label):
        self.df_climate.loc[self.tweet_counter_climate, "my_label"] = label

    # overwrite the old dataset with the newly labeled data and save the model
    def save_results(self):
        self.df_climate.to_csv(f"data/{self.dataset}", index=False)
        self.model.save_pretrained(f"models/{(self.model_name)}_{self.dataset}")

    """ 
    Preprocesses the Data, taking only data into account we havent used for training (as we dont need to train our model on 
    the same data multple times). 
    Returns the tuple: (X_train,y_train,X_predict,y_predict)
    """

    def preprocess_data(self):
        df = self.df_climate
        df.loc[df.sentiment == 0, "sentiment"] = 2
        # TO UPDATE When We have an appropriate output layer (this just removes the 2 values we cant handle yet)
        self.df_climate.loc[df.sentiment == 2, ["trained_on", "my_label"]] = [1, 2]
        # till we can use multinomial outputs
        df.loc[df.sentiment == -1, "sentiment"] = 0
        df = df[df.sentiment < 2]
        unused_data = df[df.trained_on == 0]
        training, predict = [
            x for _, x in unused_data.groupby(unused_data.my_label.isna())
        ]
        ids = [training.tweetid, predict.tweetid]
        X_train = self.tokenizer(
            list(training.message.values), padding=True, return_tensors="np"
        )
        X_predict = self.tokenizer(
            list(predict.message.values), padding=True, return_tensors="np"
        )
        return (
            X_train,
            training.sentiment.values,
            X_predict,
            predict.sentiment.values,
            ids,
        )

    """ 
    Fits the model and predicts the sentiments 
    Returns: Prediction - the corresponding logit values
    """

    def fit_and_predict(self):
        X_train, y_train, X_predict, y_predict, ids = self.preprocess_data()
        self.model.compile()
        self.model.fit(X_train.data, y_train)
        self.df_climate.loc[self.df_climate.tweetid.isin(ids[0]), "trained_on"] = 1
        y_pred = self.model.predict(X_predict.data)
        return (
            np.argmax(y_pred.logits, axis=1),
            y_pred.logits,
            ids[1],
            y_predict,
        )  # y still on 0-1 scale

    """
    I think we should extend the active learning stuff into another Module, but first I implemented some simple threshholding -> 
    rejecting predictions with an p = sigmoid(logit) < threshhold
    """

    def active_learning_iteration(self):
        threshhold = 0.7
        y_hat, logits, pred_id, y_true = self.fit_and_predict()
        y_hat = (y_hat - 0.5) * 2
        y_true = (y_true - 0.5) * 2
        p = np.max(tf.nn.sigmoid(logits), axis=1)
        # this takes 12 sec for the whole dataset (so in practice maybe 3-4 but I still think there should be a more elegant solution)
        for pred, id in list(zip(y_hat[p > threshhold], pred_id[p > threshhold])):
            self.df_climate.loc[self.df_climate.tweetid == id, "my_label"] = pred

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
        hashtags = self.df_climate["hashtag"].tolist()
        # flatten the list
        flat_list = [item for sublist in hashtags for item in sublist]
        # create a wordcloud to be shown on the analysis page
        # Frequency of words
        fdist = FreqDist(flat_list)
        # WordCloud save as a file
        wc = WordCloud(width=800, height=400, max_words=50).generate_from_frequencies(
            fdist
        )
        # plot it
        # WordCloud
        wc = WordCloud(width=800, height=400, max_words=50).generate_from_frequencies(
            fdist
        )
        # save the wordcloud
        image = wc.to_image()
        image.save("./static/plots/wordcloud.png")
