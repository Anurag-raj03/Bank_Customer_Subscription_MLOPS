from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import timedelta
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.for_drift.drift_check import drift_check_task
from scripts.for_drift.performance_check import performance_check_task
from scripts.for_drift.trigger_retrain import trigger_retrain_task

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id="drift_monitoring_pipeline",
    default_args=default_args,
    description="Checks drift and accuracy drop to trigger retraining",
    schedule_interval="@hourly",
    catchup=False,
    tags=["drift", "monitoring", "retraining"]
) as dag:
    
    drift = drift_check_task()
    perf = performance_check_task()
    trigger = trigger_retrain_task(drift, perf)

    drift >> perf >> trigger
