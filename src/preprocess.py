import numpy as np
import pandas as pd
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
            max_length=150,
            truncation=True,
            return_tensors="tf",
        )
        X_predict = tokenizer(
            list(predict.message.values),
            padding="max_length",
            max_length=150,
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
