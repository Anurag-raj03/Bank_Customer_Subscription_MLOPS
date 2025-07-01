from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import datetime,timedelta
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.extract import extraction_data
from scripts.transform import transforming_data
from scripts.load import appending_the_datas
from scripts.retrain import retrain_task

default_args={
    'owner':'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 2,
    'retry_delay': timedelta(minutes=2)

}

with DAG (

    dag_id='bank_subscriber_etl_retrain_pipeline',
    default_args=default_args,
    description="Bank Subscribe ETL Retrainig Pipeline for the BANK using AIRFLOW",
    schedule_interval=None,
    catchup=False,
    tags=["bank","etl_retarin"]
) as dag:

    extract = extraction_data.override(task_id="extract_from_db")(
    db_name="banking_costumer_data",
    table_name="temp_table_new_costumer"
)

    transform = transforming_data()

    load = appending_the_datas()

    retrain = retrain_task()

    extract >> transform >> load >> retrain
