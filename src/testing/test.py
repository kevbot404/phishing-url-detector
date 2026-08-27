import argparse
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

from src.preprocessing.preprocess import extract_features_dict


MODEL_PATH = "models/model.pkl"
DATASET_PATH = "data/external_dataset.csv"


def load_model():
    model_data = joblib.load(MODEL_PATH)

    model = model_data["model"]
    features = model_data["features"]

    return model, features


def test_dataset():
    model, features = load_model()

    # only two columns with what we need:
    # URL and ClassLabel (1=legitimate, 0=phishing)
    df = pd.read_csv(DATASET_PATH)

    if "URL" not in df.columns or "ClassLabel" not in df.columns:
        raise ValueError(
            f"Expected 'URL' and 'ClassLabel' columns in {DATASET_PATH}, "
            f"found: {list(df.columns)}"
        )

    df = df.dropna(
        subset=["URL", "ClassLabel"]
    ).reset_index(drop=True)

    print(f"Loaded {len(df)} rows from {DATASET_PATH}")

    extracted = df["URL"].apply(
        extract_features_dict
    )

    X_test = pd.DataFrame(
        extracted.tolist(),
        columns=features
    )

    y_test = df["ClassLabel"].astype(int)

    y_pred = model.predict(X_test)

    y_prob = model.predict_proba(X_test)[:, 1]

    print("\n=== External Dataset Evaluation ===")

    print(
        "Accuracy :",
        accuracy_score(y_test, y_pred)
    )

    print(
        "Precision:",
        precision_score(y_test, y_pred)
    )

    print(
        "Recall   :",
        recall_score(y_test, y_pred)
    )

    print(
        "F1       :",
        f1_score(y_test, y_pred)
    )

    print(
        "ROC-AUC  :",
        roc_auc_score(y_test, y_prob)
    )

    print(
        "\nConfusion Matrix "
        "(rows=true, cols=pred) "
        "[0=phishing, 1=legitimate]:"
    )

    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            y_pred
        )
    )


def predict_url(url):
    model, features = load_model()

    feature_dict = extract_features_dict(url)

    input_data = pd.DataFrame(
        [feature_dict]
    )

    input_data = input_data[features]

    prediction = model.predict(
        input_data
    )[0]

    confidence = model.predict_proba(
        input_data
    )[0].max()

    return prediction, confidence


def cli():
    print("\n==============================")
    print(" URL PHISHING DETECTOR CLI ")
    print("==============================")

    print("Type 'exit' to stop\n")

    while True:
        user_url = input(
            "Enter URL: "
        ).strip()

        if user_url.lower() == "exit":
            print("Bye!")
            break

        if user_url == "":
            continue

        try:
            pred, conf = predict_url(
                user_url
            )

            label = (
                "PHISHING"
                if pred == 0
                else "LEGITIMATE"
            )

            print("\nResult")

            print("----------------------")

            print(
                "URL:",
                user_url
            )

            print(
                "Prediction:",
                label
            )

            print(
                "Confidence:",
                round(conf * 100, 2),
                "%"
            )

            print("----------------------\n")

        except Exception as e:
            print(
                "Error:",
                e
            )


def main():
    parser = argparse.ArgumentParser(
        description="URL phishing detector"
    )

    parser.add_argument(
        "--mode",
        choices=[
            "dataset",
            "cli"
        ],
        required=True,
        help="Run external dataset evaluation or interactive CLI"
    )

    args = parser.parse_args()

    if args.mode == "dataset":
        test_dataset()

    elif args.mode == "cli":
        cli()


if __name__ == "__main__":
    main()