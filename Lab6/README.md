# Lab 6: ML Metadata — Student Performance Dataset

## Overview
This lab demonstrates how to use **ML Metadata (MLMD)** concepts to track artifacts, executions, and lineage in an ML pipeline. It is based on the [MLMD Lab from the MLOps course](https://github.com/raminmohammadi/MLOps/tree/main/Labs/MLMD_Labs) with the following modifications:

- **Dataset**: Student Performance in Exams (Kaggle) instead of Chicago Taxi Trips
- **Schema Generation**: Pandas-based validation instead of TFDV
- **Metadata Store**: Custom SQLite-based implementation that mirrors the MLMD API, compatible with all Python versions and platforms (the original `ml-metadata` package has compatibility issues with Python 3.11+ and Apple Silicon)

## Dataset
The [Student Performance in Exams](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams) dataset contains 1000 student records with features:
- **Categorical**: gender, race/ethnicity, parental level of education, lunch type, test preparation course
- **Numerical**: math score, reading score, writing score

The data is split into train (70%), eval (15%), and serving (15%) sets.

## Project Structure
Lab6/
├── README.md
├── MLMD_Student_Performance.ipynb   # Main notebook
├── schema.pbtxt                      # Generated schema file
├── StudentsPerformance.csv           # Raw dataset
├── .gitignore
├── img/
│   └── mlmd_overview.png             # MLMD architecture diagram
└── data/
├── train/data.csv                # Training split (700 rows)
├── eval/data.csv                 # Evaluation split (150 rows)
└── serving/data.csv              # Serving split (150 rows)

## Steps to Re-run the Lab

### 1. Clone the repository
```bash
git clone https://github.com/Nandana-125/MLOps-Labs-.git
cd MLOps-Labs-/Lab6
```

### 2. Set up Python environment
```bash
python3 -m venv mlmd_env
source mlmd_env/bin/activate
pip install pandas jupyter
```

### 3. Launch the notebook
```bash
jupyter notebook MLMD_Student_Performance.ipynb
```

### 4. Run all cells
Execute each cell from top to bottom. The notebook will:
1. Load and preview the Student Performance dataset
2. Create an in-memory SQLite metadata store
3. Register artifact types (DataSet, Schema, Statistics)
4. Register an execution type (Data Validation)
5. Create input artifact (training dataset)
6. Create and track a Data Validation execution
7. Generate a schema from the dataset using pandas
8. Create output artifact (schema)
9. Record input/output events linking artifacts to executions
10. Set up an experiment context with attributions and associations
11. Query the metadata store to trace lineage from schema back to dataset

## Key Concepts Demonstrated
- **Artifact Types & Artifacts**: Registering and creating data objects (datasets, schemas)
- **Execution Types & Executions**: Tracking pipeline step runs with state management
- **Events**: Recording input/output relationships between artifacts and executions
- **Contexts**: Grouping related artifacts and executions under experiments
- **Lineage Tracking**: Querying the store to trace which dataset produced a given schema

## Requirements
- Python 3.8+
- pandas
- jupyter
- No additional ML-specific packages needed (uses built-in sqlite3)
