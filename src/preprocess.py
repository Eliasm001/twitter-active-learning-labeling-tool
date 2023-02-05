import numpy as np
import pandas as pd
import nltk

nltk.download("omw-1.4")
nltk.download("wordnet")
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
import transformers


class Preprocessor:
    """
    Takes a DataFrame and preprocesses it
    """

    @staticmethod
    def preprocess_data(df, tokenizer):
        already_labeled = df[~df.my_label.isna()]
        X_labeled = tokenizer(
            list(already_labeled.message.values),
            padding="max_length",
            max_length=150,
            truncation=True,
            return_tensors="tf",
        )
        unused_data = df[df.trained_on == 0]
        training, predict = [
            x for _, x in unused_data.groupby(unused_data.my_label.isna())
        ]
        ids = [training.tweetid, predict.tweetid]
        X_train = tokenizer(
            list(training.message.values),
            padding="max_length",
            max_length=100,
            truncation=True,
            return_tensors="tf",
        )
        X_predict = tokenizer(
            list(predict.message.values),
            padding="max_length",
            # maximum char length / (reasonable characters per word to tweet sth. coherent)
            max_length=100,
            truncation=True,
            return_tensors="tf",
        )
        progress = already_labeled.shape[0] / (
            already_labeled.shape[0] + predict.shape[0]
        )
        return (
            X_train,
            training.my_label.values,
            X_predict,
            predict.sentiment.values,
            X_labeled,
            ids,
            progress,
        )

    @staticmethod
    def _preprocess_tweets(df, use_stemming=False):
        stop_words = set(stopwords.words("english"))
        stemmer = SnowballStemmer("english")
        lemmatizer = WordNetLemmatizer()

        df["message"] = df["message"].apply(lambda x: x.lower())

        # remove punctuation
        df["message"] = df["message"].str.replace("[^\w\s]", "", regex=True)

        # remove numbers
        df["message"] = df["message"].str.replace("\d", "", regex=True)

        # remove leading and trailing white space
        df["message"] = df["message"].apply(lambda x: x.strip())

        # remove hashtags
        # df["message"] = df["message"].str.replace(r"#\w+", "")
        df["message"] = df["message"].str.replace(r"#(\w+)", r"\1", regex=True)
        # remove mentions
        # df["message"] = df["message"].str.replace(r"@\w+", "")
        df["message"] = df["message"].str.replace(r"@(\w+)", r"\1", regex=True)

        # remove the retweet thing
        df["message"] = df["message"].str.replace(r"RT(\w+)", r"\1", regex=True)

        # remove stopwords
        df["message"] = df["message"].apply(
            lambda x: " ".join([word for word in x.split() if word not in stop_words])
        )

        # remove urls
        df["message"] = df["message"].str.replace(r"https?://\S+", "", regex=True)

        # stem or lemmatize words
        if use_stemming:
            df["message"] = df["message"].apply(
                lambda x: " ".join([stemmer.stem(word) for word in x.split()])
            )
        else:
            df["message"] = df["message"].apply(
                lambda x: " ".join([lemmatizer.lemmatize(word) for word in x.split()])
            )

        return df
