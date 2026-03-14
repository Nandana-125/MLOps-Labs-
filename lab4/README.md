# Lab 4: Airflow ML Pipeline — Mall Customer Segmentation

## Overview
This lab implements an Apache Airflow DAG pipeline that performs K-Means clustering on the **Mall Customer Segmentation** dataset. The pipeline loads data, preprocesses it, builds a clustering model, and determines the optimal number of clusters using the elbow method.

## Modifications from Original Lab
- **Different dataset**: Uses Mall Customer Segmentation data (Age, Annual Income, Spending Score) instead of the Credit Card dataset (Balance, Purchases, Credit Limit)
- **Different clustering features**: `Age`, `Annual Income (k$)`, `Spending Score (1-100)`
- **Reduced K range**: Iterates K from 1–19 (instead of 1–49) since the dataset has only 200 rows
- **Custom DAG name**: `Mall_Customer_Segmentation`
- **Custom Airflow credentials**: Personalized username/password

## Project Structure
```
lab4/
├── dags/
│   ├── airflow.py              # Airflow DAG definition
│   ├── data/
│   │   ├── file.csv            # Mall Customer dataset (200 rows)
│   │   └── test.csv            # Test samples for prediction
│   └── src/
│       ├── __init__.py
│       └── lab.py              # ML pipeline functions
├── docker-compose.yaml         # Airflow Docker setup
├── .env                        # Airflow UID config
├── logs/                       # Airflow logs (auto-generated)
├── plugins/                    # Airflow plugins directory
└── config/                     # Airflow config directory
```

## Dataset
**Mall Customer Segmentation Dataset** — 200 customers with the following features:
- `CustomerID`: Unique customer identifier
- `Gender`: Male/Female
- `Age`: Customer age
- `Annual Income (k$)`: Annual income in thousands of dollars
- `Spending Score (1-100)`: Score assigned by the mall based on spending behavior

Only `Age`, `Annual Income (k$)`, and `Spending Score (1-100)` are used for clustering.

## Pipeline Tasks (DAG)
1. **load_data_task** — Reads `file.csv` and serializes it for XCom transfer
2. **data_preprocessing_task** — Drops nulls, selects numeric features, applies MinMax scaling
3. **build_save_model_task** — Trains KMeans for K=1..19, saves model, returns SSE values
4. **load_model_task** — Loads saved model, finds optimal K via elbow method, predicts on test data

Task dependencies: `load_data → data_preprocessing → build_save_model → load_model_elbow`

## Prerequisites
- Docker Desktop (allocate at least 4GB memory, 8GB recommended)
- Git

## Steps to Run

### 1. Clone the repository
```bash
git clone https://github.com/Nandana-125/MLOps-Labs-.git
cd MLOps-Labs-/lab4
```

### 2. Set up environment
```bash
mkdir -p ./logs ./plugins ./config
echo "AIRFLOW_UID=$(id -u)" > .env
```

### 3. Initialize Airflow
```bash
docker compose up airflow-init
```
Wait until you see `exited with code 0`.

### 4. Start Airflow
```bash
docker compose up
```
Wait until you see health check logs from the webserver.

### 5. Access the UI
- Open http://localhost:8080
- Login with username: `nandana`, password: `nandana123`

### 6. Run the pipeline
- Find `Mall_Customer_Segmentation` in the DAGs list
- Toggle the switch to unpause
- Click the trigger (play) button to run

### 7. Stop Airflow
```bash
docker compose down
```

## Technologies
- Apache Airflow 2.10.5
- Python 3.12
- scikit-learn (KMeans clustering)
- pandas (data manipulation)
- kneed (elbow method)
- Docker & Docker Compose
