import numpy as np
import pandas as pd
import transformers
import tensorflow as tf
import tensorflow_hub as hub
import os
from sklearn.metrics import accuracy_score
from .preprocess import Preprocessor
from sentence_transformers import SentenceTransformer, util


class Model:
    def __init__(
        self,
        dataset_name,
        modelName,
        uncertainty_metric,
        numlab=3,
    ):
        self.numlab = numlab
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(modelName)
        self.df = pd.read_csv(f"data/{dataset_name}")
        self.df = Preprocessor._preprocess_tweets(self.df)
        if os.path.exists(f"models/{(modelName)}_{dataset_name}"):
            self.model = (
                transformers.TFAutoModelForSequenceClassification.from_pretrained(
                    f"models/{(modelName)}_{dataset_name}"
                )
            )
        else:
            self.model = (
                transformers.TFAutoModelForSequenceClassification.from_pretrained(
                    modelName,
                    from_pt=True,
                    num_labels=numlab,
                )
            )
        try:
            (
                self.X_train,
                self.y_train,
                self.X_predict,
                self.y_predict,
                self.X_labeled,
                self.ids,
                self.progress,
            ) = Preprocessor.preprocess_data(self.df, self.tokenizer)
        except ValueError:
            raise ValueError("Please annotate new data before training the model")
        self.train_ids = self.ids[0]
        self.pred_ids = self.ids[1]
        self.uncertainty_metric = uncertainty_metric

    def fit_nn(self):
        self.model.compile(metrics=["accuracy"])
        if self.numlab == 3:
            train_transformed = self.y_train + 1
        else:
            train_transformed = self.y_train
        self.model.fit(self.X_train.data, train_transformed)

    def predict_sentiments(self):
        prediction = self.model.predict(self.X_predict.data)
        if self.numlab == 3:
            self.y_hat = np.argmax(prediction.logits, axis=1) - 1
        else:
            self.y_hat = np.argmax(prediction.logits, axis=1)
        # HIER Entropie benutzen
        if self.uncertainty_metric == "max_p":
            self.uncertainty = 1 - np.max(tf.nn.softmax(prediction.logits), axis=1)
        elif self.uncertainty_metric == "entropy":
            prob = tf.nn.softmax(prediction.logits)
            self.uncertainty = -np.sum(prob * np.log(prob), axis=-1)
            self.uncertainty = self.uncertainty / (np.log(self.numlab))
        return prediction

    def save_model(self):
        self.model.save_pretrained(f"models/{(self.model_name)}_{self.dataset_name}")
