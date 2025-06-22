import mlflow
from mlflow.exceptions import MlflowException
from mlflow.tracking import MlflowClient

def register_model():
    mlflow.set_tracking_uri("http://mlflow:5000")
    experiment_name = "Bank Marketing"


    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = mlflow.create_experiment(experiment_name)
        print(f"New experiment '{experiment_name}' created with ID: {experiment_id}")
    else:
        experiment_id = experiment.experiment_id
        print(f"Existing experiment '{experiment_name}' found with ID: {experiment_id}")

    client = MlflowClient()
    runs = client.search_runs(experiment_ids=[experiment_id], order_by=["start_time DESC"], max_results=1)

    if not runs:
        print("No recent runs found in the experiment.")
        return

    latest_run = runs[0]
    run_id = latest_run.info.run_id
    print(f"🔍 Latest run ID: {run_id}")

    # Check for RandomForest model directory in artifacts
    artifacts = client.list_artifacts(run_id)
    artifact_paths = [artifact.path for artifact in artifacts]

    if "RandomForest" not in artifact_paths:
        print("No model directory named 'RandomForest' found in run artifacts.")
        return

    print("'RandomForest' model directory found. Proceeding to register...")

    model_uri = f"runs:/{run_id}/RandomForest"
    registered_model_name = "BankMarketingRandomForestModel"

    try:
        result = mlflow.register_model(model_uri=model_uri, name=registered_model_name)
        print(f"Model registered as '{registered_model_name}' (version: {result.version})")
    except MlflowException as e:
        print(f"Failed to register model: {e}")

if __name__ == "__main__":
    register_model()
