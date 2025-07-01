from airflow.decorators import task
from airflow.utils.log.logging_mixin import LoggingMixin

@task
def retrain_task(
    main_csv_path="Data_kind_stack/main_data/raw_data.csv",
    new_preprocessed_file="Data_kind_stack/main_preproccesd/after_preprocess.csv"
):
    log = LoggingMixin().log
    import os
    import sys
    import joblib
    import pandas as pd
    import mlflow
    import mlflow.sklearn
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
    from mlflow.models.signature import infer_signature

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from src.Data_ingest.data_validations import data_val
    from src.Preprocessing.labeling import label_encod
    from src.Preprocessing.smote_balancing import smote_split
    from src.Preprocessing.scaling import scale

    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("Bank Marketing")

    label_artifact = os.path.join("artifacts", "label_encoders.jbl")
    scaling_artifact = os.path.join("artifacts", "scalers.jbl")
    example_input_path = os.path.join("Data_kind_stack", "exmpl_input", "Example_input.csv")

    try:
        main_csv_path = os.path.abspath(main_csv_path)
        new_preprocessed_file = os.path.abspath(new_preprocessed_file)

        log.info("Step 1: Validating and reading input data.")
        df = data_val(main_csv_path)

        log.info("Step 2: Encoding categorical features.")
        df = label_encod(df)

        log.info("Step 3: Scaling using PowerTransformer.")
        df = scale(df)

        log.info("Step 4: Saving preprocessed data.")
        df.to_csv(new_preprocessed_file, index=False)

        log.info("Step 5: Reloading preprocessed CSV.")
        df = data_val(new_preprocessed_file)

        log.info("Step 6: Splitting and balancing with SMOTE.")
        x_train, x_test, y_train, y_test = smote_split(df, target_column='y', test_size=0.2)

        log.info("Step 7: Training RandomForest and logging to MLflow.")
        with mlflow.start_run():
            model = RandomForestClassifier()
            model.fit(x_train, y_train)
            y_pred = model.predict(x_test)
            joblib.dump(model, "artifacts/Random_ForestModel.jbl")

            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            re = recall_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)

            if os.path.exists(label_artifact):
                mlflow.log_artifact(label_artifact)
            if os.path.exists(scaling_artifact):
                mlflow.log_artifact(scaling_artifact)

            mlflow.log_metric("Accuracy Score", acc)
            mlflow.log_metric("F1_Score", f1)
            mlflow.log_metric("Recall Score", re)
            mlflow.log_metric("Precision Score", prec)
            mlflow.log_param("test_size", 0.2)
            mlflow.log_param("DataFrame shape", str(df.shape))
            mlflow.log_param("SMOTE_applied", True)

            example_input_df = pd.read_csv(example_input_path)
            if 'Unnamed: 0' in example_input_df.columns:
                example_input_df = example_input_df.drop(columns=['Unnamed: 0'])
            example_output = model.predict(example_input_df)
            
            signature = infer_signature(example_input_df, example_output)

            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="RandomForest",
                signature=signature,
                registered_model_name="BankMarketingRandomForestModel"
            )

        log.info("Retraining and logging complete.")

    except Exception as e:
        log.error(f"An error occurred during retraining: {e}")
