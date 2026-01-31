import json
from datetime import datetime

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib


def train_and_save():
    # 1) Load dataset (different from Iris)
    wine = load_wine()
    X, y = wine.data, wine.target

    # 2) Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3) Model pipeline (different from RandomForest)
    #    Scaling + Logistic Regression
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=2000, random_state=42))
        ]
    )

    # 4) Train
    model.fit(X_train, y_train)

    # 5) Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    report = classification_report(y_test, preds, output_dict=True)

    # 6) Save model
    joblib.dump(model, "wine_model.pkl")

    # 7) Save metrics (extra artifact so it’s clearly “your version”)
    metrics = {
        "dataset": "sklearn.load_wine",
        "model": "StandardScaler + LogisticRegression",
        "accuracy": acc,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "classification_report": report,
    }

    with open("metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print("Training complete ")
    print(f"Accuracy: {acc:.4f}")
    print("Saved: wine_model.pkl and metrics.json")


if __name__ == "__main__":
    train_and_save()

