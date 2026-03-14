from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.lab import load_data, data_preprocessing, build_save_model, load_model_elbow

# Define default arguments for the DAG
default_args = {
    'owner': 'Nandana',
    'start_date': datetime(2026, 1, 15),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

# Create DAG for Mall Customer Segmentation pipeline
with DAG(
    'Mall_Customer_Segmentation',
    default_args=default_args,
    description='KMeans clustering pipeline for Mall Customer Segmentation dataset',
    catchup=False,
) as dag:

    load_data_task = PythonOperator(
        task_id='load_data_task',
        python_callable=load_data,
    )

    data_preprocessing_task = PythonOperator(
        task_id='data_preprocessing_task',
        python_callable=data_preprocessing,
        op_args=[load_data_task.output],
    )

    build_save_model_task = PythonOperator(
        task_id='build_save_model_task',
        python_callable=build_save_model,
        op_args=[data_preprocessing_task.output, "model.sav"],
    )

    load_model_task = PythonOperator(
        task_id='load_model_task',
        python_callable=load_model_elbow,
        op_args=["model.sav", build_save_model_task.output],
    )

    load_data_task >> data_preprocessing_task >> build_save_model_task >> load_model_task

if __name__ == "__main__":
    dag.test()
