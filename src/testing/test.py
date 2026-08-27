import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)

from src.preprocessing.preprocess import extract_features

MODEL_PATH = "models/model.pkl"
DATASET_PATH = "data/external_dataset.csv"

model_data = joblib.load(MODEL_PATH)
model = model_data["model"]
features = model_data["features"]

# only two columns with what we need: URL and ClassLabel (1=legitimate, 0=phishing).
df = pd.read_csv(DATASET_PATH)

if "URL" not in df.columns or "ClassLabel" not in df.columns:
    raise ValueError(
        f"Expected 'URL' and 'ClassLabel' columns in {DATASET_PATH}, "
        f"found: {list(df.columns)}"
    )

df = df.dropna(subset=["URL", "ClassLabel"]).reset_index(drop=True)

print(f"Loaded {len(df)} rows from {DATASET_PATH}")

extracted = df["URL"].apply(extract_features)
X_test = pd.DataFrame(extracted.tolist(), columns=features)

y_test = df["ClassLabel"].astype(int)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\n=== External Dataset Evaluation ===")
print("Accuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))
print("F1       :", f1_score(y_test, y_pred))
print("ROC-AUC  :", roc_auc_score(y_test, y_prob))

print("\nConfusion Matrix (rows=true, cols=pred) [0=phishing, 1=legitimate]:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))
