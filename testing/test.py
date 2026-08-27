import pandas as pd
import joblib

from preprocessing.preprocess import extract_features

MODEL_PATH = "model/model.pkl"
DATASET_PATH = "data/external_dataset.csv"

model = joblib.load(MODEL_PATH)

df = pd.read_csv(DATASET_PATH)

X = pd.DataFrame(
    df["URL"].apply(extract_features).tolist()
)

y = df["label"]

predictions = model.predict(X)
probabilities = model.predict_proba(X)[:, 1]