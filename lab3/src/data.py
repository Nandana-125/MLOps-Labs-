import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

def load_data():
    """
    Load the Diabetes dataset and return features and target.
    Features include age, sex, bmi, blood pressure, and 6 blood serum measurements.
    Target is a quantitative measure of disease progression one year after baseline.
    We convert it to binary: 1 if above median (high risk), 0 if below (low risk).
    """
    diabetes = load_diabetes()
    X = diabetes.data
    y = diabetes.target

    # Convert regression target to binary classification
    median_val = np.median(y)
    y_binary = (y > median_val).astype(int)

    return X, y_binary

def split_data(X, y):
    """
    Split the data into training and testing sets.
    Args:
        X (numpy.ndarray): Feature matrix.
        y (numpy.ndarray): Target labels.
    Returns:
        Tuple of (X_train, X_test, y_train, y_test)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test