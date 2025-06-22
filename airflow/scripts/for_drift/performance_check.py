from airflow.decorators import task
@task
def performance_check_task():
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from Drift_Detector.mlflow_checker import check_model_accuracy_drop
    perf_drop, current_acc = check_model_accuracy_drop()
    below_threshold = current_acc < 0.70

    return {
        "accuracy": current_acc,
        "performance_drop": perf_drop,
        "below_threshold": below_threshold
    }
