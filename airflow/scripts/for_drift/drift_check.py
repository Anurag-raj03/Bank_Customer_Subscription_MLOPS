from airflow.decorators import task


@task
def drift_check_task():
    import pandas as pd
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from Drift_Detector.evidently_runner import run_evidently_report

    CURRENT_PATH = "src/Data/Banking_Call_Data.xlsx"
    REFERENCE_PATH = "Data_kind_stack/extracted_data/reference_drift_data.csv"
    if not os.path.exists(CURRENT_PATH) or not os.path.exists(REFERENCE_PATH):
        raise FileNotFoundError("Missing current or reference file.")

    current_df = pd.read_excel(CURRENT_PATH)
    print(f"Checking drift on {len(current_df)} rows...")
    
    ref_df = pd.read_csv(REFERENCE_PATH)

    if ref_df.empty:
        return

    drift_detected = run_evidently_report(reference_path=REFERENCE_PATH, current_path=CURRENT_PATH)
    return drift_detected
