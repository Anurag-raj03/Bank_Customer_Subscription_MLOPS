import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset, ClassificationPreset
from evidently import ColumnMapping
from datetime import datetime
import os

def run_evidently_report(reference_path: str, current_path: str) -> bool:
    reference = pd.read_csv(reference_path)
    current = pd.read_excel(current_path)

    report = Report(metrics=[
        DataDriftPreset(),
        DataQualityPreset(),  
        ClassificationPreset()
    ])

    column_mapping = ColumnMapping(
        target='y',
        prediction='y',
        pos_label='yes'
    )

    report.run(reference_data=reference, current_data=current, column_mapping=column_mapping)

   
    os.makedirs("Drift_Detector/drift_reports", exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"Drift_Detector/drift_reports/drift_report_{run_id}.html"

    report.save_html(output_path)
    print(f"Drift report saved to: {output_path}")

    try:
        drift_detected = report.as_dict()["metrics"][0]["result"].get("dataset_drift", False)
    except Exception as e:
        print(f"Error checking drift: {e}")
        drift_detected = False

    return drift_detected
