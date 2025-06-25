from airflow.decorators import task

@task
def trigger_retrain_task(drift_detected: bool, perf_result: dict):
    import requests
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    should_retrain = bool(drift_detected) or bool(perf_result["performance_drop"]) or bool(perf_result["below_threshold"])

    if should_retrain:
        airflow_url = "http://airflow:8080/api/v1/dags/drift_detection_pipeline_retarin/dagRuns"
        headers = {
            "Authorization": "Basic YWlyZmxvdzphaXJmbG93",  
            "Content-Type": "application/json"
        }

        payload = {
            "conf": {
                "accuracy": float(perf_result["accuracy"]),
                "drift_detected": bool(drift_detected),
                "below_threshold": bool(perf_result["below_threshold"])
            }
        }

        response = requests.post(airflow_url, json=payload, headers=headers)
        print(f"Triggered retrain DAG - status: {response.status_code}")
        return response.ok
    else:
        print("No need to retrain. Everything is good.")
        return False
