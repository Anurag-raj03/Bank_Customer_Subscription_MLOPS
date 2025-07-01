from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import datetime,timedelta
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.retrain import retrain_task

default_args={
    'owner':'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 2,
    'retry_delay': timedelta(minutes=2)

}

with DAG (

    dag_id='drift_detection_pipeline_retarin',
    default_args=default_args,
    description="Bank Subscribe ETL Retrainig Pipeline for the BANK using AIRFLOW",
    schedule_interval=None,
    catchup=False,
    tags=["bank","etl_retarin"]
) as dag:



    retrain = retrain_task()

    retrain
