import numpy as np
import pandas as pd
import transformers
import tensorflow as tf
import tensorflow_hub as hub
import os
from sklearn.metrics import accuracy_score
from .preprocess import Preprocessor


class Model:
    def __init__(self, dataset_name, modelName="prajjwal1/bert-tiny"):
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(modelName)
        self.df = pd.read_csv(f"data/{dataset_name}")
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
                    num_labels=4,
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
            ) = Preprocessor.preprocess_data(
                pd.read_csv(f"data/{dataset_name}"), self.tokenizer
            )
        except ValueError:
            raise ValueError("Please annotate new data before training the model")
        self.train_ids = self.ids[0]
        self.pred_ids = self.ids[1]
        if self.X_train == "please label new data before you train the model":
            print("please label new data before you train the model")

    def fit_nn(self):
        self.model.compile()
        train_transformed = self.y_train + 1
        self.model.fit(self.X_train.data, train_transformed)

    def predict_sentiments(self):
        prediction = self.model.predict(self.X_predict.data)
        self.y_hat = np.argmax(prediction.logits, axis=1) - 1
        self.uncertainty = 1 - np.max(tf.nn.sigmoid(prediction.logits), axis=1)
        return prediction

    def save_model(self):
        self.model.save_pretrained(f"models/{(self.model_name)}_{self.dataset_name}")
