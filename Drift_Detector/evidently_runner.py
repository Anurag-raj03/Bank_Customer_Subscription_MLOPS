import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset, DataSummaryPreset, ClassificationPreset
from datetime import datetime
import os

def run_evidently_report(reference_path: str, current_path: str) -> bool:
    reference = pd.read_csv(reference_path)
    current = pd.read_excel(current_path)

    report = Report(metrics=[
        DataDriftPreset(),
        DataSummaryPreset(),
        ClassificationPreset()
    ])

    column_mapping = {
        "target": "y"
    }

    report.run(reference_data=reference, current_data=current, column_mapping=column_mapping)

    os.makedirs("drift_reports", exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"drift_reports/drift_report_{run_id}.html"
    report.save_html(output_path)
    print(f"Drift report saved to: {output_path}")

    drift_detected = report.as_dict()["metrics"][0]["result"].get("dataset_drift", False)
    return drift_detected
