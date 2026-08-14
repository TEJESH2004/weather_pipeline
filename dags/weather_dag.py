from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# tell Airflow where your src folder is inside the container
sys.path.insert(0, '/opt/airflow/src')

from extractor   import extract_weather
from transformer import transform_weather
from loader      import load_weather

CITIES = [
    {"name": "Hyderabad", "lat": 17.38, "lon": 78.49},
    {"name": "Mumbai",    "lat": 19.07, "lon": 72.87},
    {"name": "Delhi",     "lat": 28.61, "lon": 77.20},
]

default_args = {
    "owner":            "tejesh",
    "retries":          2,
    "retry_delay":      timedelta(minutes=5),
    "email_on_failure": False,
}

def run_extract(**context):
    results = []
    for city in CITIES:
        raw = extract_weather(city)
        results.append(raw)
    return results

def run_transform(**context):
    results = context["ti"].xcom_pull(task_ids="extract_task")
    dfs = []
    for raw in results:
        df = transform_weather(raw)
        dfs.append(df.to_dict("records"))
    return dfs

def run_load(**context):
    import pandas as pd
    dfs = context["ti"].xcom_pull(task_ids="transform_task")
    for records in dfs:
        df = pd.DataFrame(records)
        load_weather(df)

with DAG(
    dag_id="weather_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule_interval="0 8 * * *",
    catchup=False,
    description="Daily weather ETL pipeline",
) as dag:

    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=run_extract,
    )

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=run_transform,
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=run_load,
    )

    extract_task >> transform_task >> load_task