import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)

from src.preprocessing.preprocess import extract_features_dict

df = pd.read_csv("data/data.csv")

features = [
    "URLLength",
    "DomainLength",
    "IsDomainIP",
    "NoOfSubDomain",
    "HasObfuscation",
    "NoOfObfuscatedChar",
    "ObfuscationRatio",
    "NoOfLettersInURL",
    "LetterRatioInURL",
    "NoOfDegitsInURL",
    "DegitRatioInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL",
    "SpacialCharRatioInURL",
    "IsHTTPS"
]

print("Extracting features from raw URLs via preprocess.py ...")

feature_df = pd.DataFrame(df["URL"].apply(extract_features_dict).tolist())
feature_df["ClassLabel"] = df["label"]

X = feature_df.drop(
    "ClassLabel",
    axis=1
)

y = feature_df["ClassLabel"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

prediction = model.predict(X_test)

print("\nAccuracy:")

print(
    accuracy_score(
        y_test,
        prediction
    )
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        prediction
    )
)

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test, 
        prediction
    )
)

os.makedirs("models", exist_ok=True)

model_data = {
    "model": model,
    "features": X.columns.tolist()
}

joblib.dump(model_data, "models/model.pkl")

print("\nModel saved successfully:")
print("models/model.pkl")