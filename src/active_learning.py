import numpy as np
import pandas as pd
import transformers
import tensorflow as tf
import tensorflow_hub as hub
import os
from .preprocess import Preprocessor
from .model import Model
from sentence_transformers import SentenceTransformer, util
import torch
from sklearn.metrics.pairwise import cosine_similarity as sim
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
)


class Active_Learner:
    def __init__(
        self,
        dataset_name,
        modelName="prajjwal1/bert-tiny",
        numlab=3,
        sentence_model="sentence-transformers/all-MiniLM-L6-v2",
        uncertainty_metric="entropy",
        max_reordering=100,
        only_diff=False,
        only_unc=False,
    ):
        self.data = pd.read_csv(f"data/{dataset_name}")
        self.model = Model(
            dataset_name,
            modelName,
            numlab=numlab,
            uncertainty_metric=uncertainty_metric,
        )
        self.model_name = modelName
        self.dataset_name = dataset_name
        self.sentence_model = SentenceTransformer(sentence_model)
        self.max_reorder = max_reordering
        self.only_diff = only_diff
        self.only_unc = only_unc

    def query(self):
        self.model.fit_nn()
        self.data.loc[self.data.tweetid.isin(self.model.train_ids), "trained_on"] = 1
        self.model.predict_sentiments()
        self.untrained_data = self.data[self.data.trained_on == 0].copy()
        self.untrained_data["uncertainty"] = self.model.uncertainty
        self.untrained_tweets = Preprocessor._preprocess_tweets(
            self.untrained_data.copy()
        )["message"]
        self.untrained_data["embeddings"] = (
            self.sentence_model.encode(
                self.untrained_tweets.values, convert_to_tensor=True
            )
            .numpy()
            .tolist()
        )

        self.next_query = pd.DataFrame(columns=self.untrained_data.columns)
        self.reorder_counter = 0
        while (len(self.untrained_data) > 0) and (
            self.reorder_counter < self.max_reorder
        ):
            self.next_query, self.untrained_data = self._query_one(
                self.next_query, self.untrained_data
            )
            self.reorder_counter += 1
        if self.reorder_counter >= self.max_reorder:
            self.next_query = self.next_query.append(
                self.untrained_data, ignore_index=True
            )
        self.next_query.drop("embeddings", axis=1, inplace=True)
        self.next_query.drop("uncertainty", axis=1, inplace=True)
        self.data = self.next_query.append(
            self.data[self.data.trained_on == 1].copy(), ignore_index=True
        )

        return self.data

    def get_predictive_scores(self):
        """
        computes various scores of the prediction (can only be used after query and when true values are present)
        """
        acc = accuracy_score(self.model.y_hat, self.model.y_predict)

        # calculate the confusion matrix
        cm = confusion_matrix(self.model.y_hat, self.model.y_predict)

        return (acc, cm)

    def save_modell(self):
        """
        saves the trained modell (model.model isnt a typo)
        """
        self.model.model.save_pretrained(
            f"models/{(self.model_name)}_{self.dataset_name}"
        )

    def _query_one(self, next_query, untrained):
        """ """
        if len(next_query) > 0:
            u = untrained.uncertainty
            s = np.max(
                util.cos_sim(
                    torch.from_numpy(np.array(untrained.embeddings.tolist())),
                    torch.from_numpy(np.array(next_query.embeddings.tolist())),
                )
                .numpy()
                .tolist(),
                axis=1,
            )
            alpha = 1 - self.model.progress
            if self.only_diff == True:
                alpha = 1
            if self.only_unc == True:
                alpha = 0
            untrained["score"] = alpha * (1 - s) + (1 - alpha) * u
        else:
            untrained["score"] = untrained.uncertainty
        row = untrained.loc[untrained["score"].idxmax()].drop("score")
        next_query = next_query.append(row, ignore_index=True)
        untrained.drop(untrained["score"].idxmax(), inplace=True)
        untrained.drop("score", axis=1, inplace=True)
        return next_query, untrained
