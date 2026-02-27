import joblib

def predict_data(X):
    """
    Load the trained model and predict diabetes risk.
    Args:
        X (numpy.ndarray): Input features for prediction.
    Returns:
        y_pred (numpy.ndarray): Predicted labels (0 = low risk, 1 = high risk).
    """
    model = joblib.load("../model/diabetes_model.pkl")
    y_pred = model.predict(X)
    return y_pred