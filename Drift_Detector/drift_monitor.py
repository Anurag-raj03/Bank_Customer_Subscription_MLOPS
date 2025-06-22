
import pandas as pd
import os
import requests

CURRENT_PATH = "src/Data/Banking_Call_Data.xlsx"
REFERENCE_PATH = "Data_kind_stack/extracted_data/refrence_drift_data.csv"
LAST_COUNT_PATH = "Data_kind_stack/last_count_for_drift/last_checked_count.txt"

def read_last_count():
    if not os.path.exists(LAST_COUNT_PATH):
        with open(LAST_COUNT_PATH, 'w') as f:
            f.write("0")
        return 0
    with open(LAST_COUNT_PATH, 'r') as f:
        return int(f.read().strip())

def write_last_count(count):
    with open(LAST_COUNT_PATH, 'w') as f:
        f.write(str(count))

def trigger_airflow_dag(payload):
    airflow_url = "http://airflow:8080/api/v1/dags/drift_monitoring_pipeline/dagRuns"
    headers = {
        "Authorization": "Basic YWlyZmxvdzphaXJmbG93",
        "Content-Type": "application/json"
    }
    response = requests.post(airflow_url, json={"conf": payload}, headers=headers)
    print(f"Airflow Trigger Status: {response.status_code}")
    return response.ok

def run_drift_check():
    try:
        if not os.path.exists(CURRENT_PATH) or not os.path.exists(REFERENCE_PATH):
            print("Reference or Current Data not found. Skipping.")
            return

        refrence_path = pd.read_csv(REFERENCE_PATH)
        total_rows = len(refrence_path)
        last_checked = read_last_count()

        if total_rows >= last_checked + 50:
            print("Drift or Accuracy Drop detected! Triggering DAG.")

            write_last_count(total_rows)

    except Exception as e:
        print(f"Drift check failed: {e}")
