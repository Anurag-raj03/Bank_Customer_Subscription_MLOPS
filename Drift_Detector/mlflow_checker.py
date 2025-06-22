import mlflow
import pandas as pd

mlflow.set_tracking_uri("http://mlflow:5000")
experiment_name="Bank Marketing"
min_thres_acc=0.80

def check_model_accuracy_drop():
    experiment=mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        raise Exception(f"No experiment found: {experiment_name}")
    
    runs=mlflow.search_runs(experiment_ids=[experiment.experiment_id],order_by=["start_time ASC"])
    
    if len(runs)<2:
        raise Exception("Not enough runs to compare perfomance")
    
    base_accuracy = runs.iloc[0]["metrics.Accuracy Score"]
    latest_accuracy = runs.iloc[-1]["metrics.Accuracy Score"]

    print(f"Base Accuracy: {base_accuracy} | Latest Accuracy: {latest_accuracy}")

    if latest_accuracy < base_accuracy or latest_accuracy < min_thres_acc:
        return True, latest_accuracy

    return False, latest_accuracy