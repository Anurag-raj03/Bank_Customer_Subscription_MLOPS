from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os
import sys
import joblib
import requests
import base64
import pandas as pd
from time import sleep

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prometheus_fastapi_instrumentator import Instrumentator
from BACKEND.prediciton_pipeline import load_input_raw_data, predicts, preprocess_input
from Database_connection.db_init import insert_subscriber, fetch_last_record
from Drift_Detector.drift_monitor import run_drift_check
from llm_explainer.explainer import generate_explanation

label_encoder = joblib.load("artifacts/label_encoders.jbl")
scaler = joblib.load("artifacts/scalers.jbl")
model = joblib.load("artifacts/Random_ForestModel.jbl")

app = FastAPI(title="Bank Marketing Prediction API")
Instrumentator().instrument(app).expose(app)

db_name = "banking_costumer_data"
table1 = "temp_table_new_costumer"
table2 = "banking_new_data_history"
raw_storage_path = "Data_kind_stack/user_raw_predictions.csv"
preprocessed_storage_path = "Data_kind_stack/user_preprocessed_predictions.csv"

class InputData(BaseModel):
    age: int
    job: str
    marital: str
    education: str
    default: str
    balance: int
    housing: str
    loan: str
    contact: str
    day: int
    month: str
    duration: int
    campaign: int
    pdays: int
    previous: int
    poutcome: str

def delayed_trigger_airflow(data):
    sleep(5)
    trigger_airflow_dag(data)

def delayed_drift_check():
    sleep(5)
    run_drift_check()

def delayed_drift_api():
    sleep(5)
    call_drift_api()

def trigger_airflow_dag(data: dict):
    try:
        airflow_trigger_url = "http://airflow:8080/api/v1/dags/bank_subscriber_etl_retrain_pipeline/dagRuns"
        headers = {
            "Authorization": "Basic " + base64.b64encode(b"airflow:airflow").decode("utf-8"),
            "Content-Type": "application/json"
        }
        payload = {"conf": data}
        print("[DEBUG] Triggering Airflow with:", payload)
        response = requests.post(airflow_trigger_url, headers=headers, json=payload)
        print("[Airflow] Trigger response:", response.status_code, response.text)
    except Exception as e:
        print("[Airflow Trigger Error]", e)

def call_drift_api():
    try:
        response = requests.get("http://drift-detector:3001/run-drift-check")
        print("[Drift API] Status Code:", response.status_code)
    except Exception as e:
        print("[Drift API Error]", e)

@app.post("/predict")
def make_prediction(data: InputData, background_tasks: BackgroundTasks):
    try:
        input_dict = data.dict()
        print("[Received Data]", input_dict)

        raw_df = load_input_raw_data(input_dict)
        preprocessed_df = preprocess_input(input_dict, label_encoder, scaler)

        prediction = predicts(preprocessed_df, model)
        raw_df["y"] = "yes" if prediction == 1 else "no"
        preprocessed_df["y"] = prediction
        input_dict["y"] = prediction

        os.makedirs(os.path.dirname(raw_storage_path), exist_ok=True)
        os.makedirs(os.path.dirname(preprocessed_storage_path), exist_ok=True)
        raw_df.to_csv(raw_storage_path, mode="a", index=False, header=not os.path.exists(raw_storage_path))
        preprocessed_df.to_csv(preprocessed_storage_path, mode="a", index=False, header=not os.path.exists(preprocessed_storage_path))

        try:
            last_row_df = pd.read_csv(raw_storage_path).tail(1)
            last_row_dict = last_row_df.to_dict(orient="records")[0]

            inserted1 = insert_subscriber(db_name, table1, last_row_dict)
            inserted2 = insert_subscriber(db_name, table2, last_row_dict)
            print("[DB Inserted]", inserted1, inserted2)

            last_record = fetch_last_record(db_name, table2)
        except Exception as e:
            print("[DB Insert Error]", e)
            inserted1 = inserted2 = False
            last_record = {}

        background_tasks.add_task(trigger_airflow_dag, last_row_dict)
        background_tasks.add_task(delayed_drift_check)
        background_tasks.add_task(delayed_drift_api)

        return {
            "prediction": "yes" if prediction == 1 else "no",
            "last_inserted_record": last_record,
            "db_insert_status": {"temp_table_new_costumer": inserted1, "banking_new_data_history": inserted2}
        }

    except Exception as e:
        print("[Prediction Error]", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/explain")
def explain_prediction(data: InputData):
    try:
        last_row_df = pd.read_csv(raw_storage_path).tail(1)
        last_row_dict = last_row_df.to_dict(orient="records")[0]
        preprocessed_df = preprocess_input(last_row_dict, label_encoder, scaler)
        prediction = predicts(preprocessed_df, model)
        explanation = generate_explanation(last_row_dict, prediction)
        return {
            "prediction": "yes" if prediction == 1 else "no",
            "explanation": explanation
        }

    except Exception as e:
        print("[Explanation Error]", e)
        raise HTTPException(status_code=500, detail=str(e))
