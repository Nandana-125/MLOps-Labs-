import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator
import pickle
import os
import base64


def load_data():
    """
    Loads Mall Customer data from a CSV file, serializes it,
    and returns the base64-encoded serialized data.
    """
    print("Loading Mall Customer Segmentation data...")
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/file.csv"))
    serialized_data = pickle.dumps(df)
    return base64.b64encode(serialized_data).decode("ascii")


def data_preprocessing(data_b64: str):
    """
    Deserializes base64-encoded data, selects clustering features
    (Age, Annual Income, Spending Score), applies MinMax scaling,
    and returns base64-encoded preprocessed data.
    """
    data_bytes = base64.b64decode(data_b64)
    df = pickle.loads(data_bytes)

    # Drop missing values
    df = df.dropna()

    # Select numeric features for clustering (different from original lab)
    clustering_data = df[["Age", "Annual Income (k$)", "Spending Score (1-100)"]]

    # Apply MinMax scaling
    min_max_scaler = MinMaxScaler()
    clustering_data_minmax = min_max_scaler.fit_transform(clustering_data)

    clustering_serialized = pickle.dumps(clustering_data_minmax)
    return base64.b64encode(clustering_serialized).decode("ascii")


def build_save_model(data_b64: str, filename: str):
    """
    Builds KMeans models for k=1..19, records SSE (inertia),
    saves the last model, and returns the SSE list.
    """
    data_bytes = base64.b64decode(data_b64)
    df = pickle.loads(data_bytes)

    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "max_iter": 300,
        "random_state": 42,
    }

    sse = []
    for k in range(1, 20):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(df)
        sse.append(kmeans.inertia_)

    # Save the last fitted model
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    with open(output_path, "wb") as f:
        pickle.dump(kmeans, f)

    return sse


def load_model_elbow(filename: str, sse: list):
    """
    Loads the saved model and determines optimal k via elbow method.
    Predicts cluster for test.csv samples.
    """
    output_path = os.path.join(os.path.dirname(__file__), "../model", filename)
    loaded_model = pickle.load(open(output_path, "rb"))

    # Determine optimal clusters using elbow method
    kl = KneeLocator(range(1, 20), sse, curve="convex", direction="decreasing")
    print(f"Optimal number of clusters: {kl.elbow}")

    # Predict on test data
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/test.csv"))
    pred = loaded_model.predict(df)[0]

    try:
        return int(pred)
    except Exception:
        return pred.item() if hasattr(pred, "item") else pred
