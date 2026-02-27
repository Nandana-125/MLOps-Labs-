from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
from data import load_data, split_data

def fit_model(X_train, y_train):
    """
    Train a Random Forest Classifier and save the model.
    Args:
        X_train (numpy.ndarray): Training features.
        y_train (numpy.ndarray): Training labels.
    Returns:
        model: Trained Random Forest Classifier.
    """
    rf_classifier = RandomForestClassifier(
        n_estimators=100, max_depth=5, random_state=42
    )
    rf_classifier.fit(X_train, y_train)
    joblib.dump(rf_classifier, "../model/diabetes_model.pkl")
    print("Model saved to ../model/diabetes_model.pkl")
    return rf_classifier

if __name__ == "__main__":
    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    model = fit_model(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")