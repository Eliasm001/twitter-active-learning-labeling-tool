import numpy as np
import pandas as pd
import transformers
import tensorflow as tf
import tensorflow_hub as hub
import os
from sklearn.metrics import accuracy_score
from .preprocess import Preprocessor
from .model import Model
from sklearn.metrics.pairwise import cosine_similarity as sim


class Active_Learner:
    def __init__(self, dataset_name, modelName="prajjwal1/bert-tiny"):
        self.data = pd.read_csv(f"data/{dataset_name}")
        self.model = Model(dataset_name, modelName)

    def query(self):
        self.model.fit_nn()
        self.data.loc[self.data.tweetid.isin(self.model.train_ids), "trained_on"] = 1
        self.model.predict_sentiments()
        helper_df = pd.DataFrame.from_dict(
            {"tweetid": self.model.pred_ids, "score": self._compute_score()}
        )
        self.data = self.data.merge(helper_df, on="tweetid", how="left")
        self.data.score.fillna(0, inplace=True)
        self.data.sort_values(by=["score"], ascending=False, inplace=True)
        self.data.drop("score", axis=1, inplace=True)
        return self.data

    def get_accuracy(self):
        """
        computes accuracy of the fit (can only be used after query)
        """
        return accuracy_score(self.model.y_hat, self.model.y_predict)

    def save_modell(self):
        """
        saves the trained modell (model.model isnt a typo)
        """
        self.model.model.save_pretrained(f"models/{(self.model_name)}_{self.dataset_name}")

    def _compute_score(self):
        u = self.model.uncertainty
        s = np.max(
            sim(
                self.model.X_labeled["input_ids"].numpy(),
                self.model.X_predict["input_ids"].numpy(),
            ),
            axis=0,
        )
        alpha = 1 - self.model.progress
        return alpha * (1 - s) + (1 - alpha) * u
