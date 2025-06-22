from fastapi import FastAPI
from drift_monitor import run_drift_check
from prometheus_client import start_http_server

app = FastAPI(title="Drift Detector API")


@app.get("/run-drift-check")
def trigger_drift_check():
    try:
        run_drift_check()
        return {"status": "Drift check executed successfully"}
    except Exception as e:
        return {"error": str(e)}
