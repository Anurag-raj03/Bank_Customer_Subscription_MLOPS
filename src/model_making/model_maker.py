import mlflow
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging
import mlflow.sklearn
import joblib
from sklearn.ensemble import RandomForestClassifier
from Data_ingest.data_validations import data_val
from Preprocessing.labeling import label_encod
from Preprocessing.smote_balancing import smote_split  
from Preprocessing.scaling import scale
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("Bank Marketing")

path = os.path.join("Data", "Banking_Call_Data.xlsx")
preprocessed_path = "Data_kind_stack/main_preproccesd/main_preprocessed.csv"
label_artifact = os.path.join("artifacts", "label_encoders.jbl")
scaling_artifact = os.path.join("artifacts", "scalers.jbl")
example_input_path = os.path.join("Data_kind_stack", "exmpl_input", "Example_input.csv")

def model_makings(path: str):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        logging.info("Step 1: Reading and validating input data.")
        df = data_val(path)

        logging.info("Step 2: Encoding categorical features.")
        df = label_encod(df)

        logging.info("Step 3: Scaling features using PowerTransformer.")
        df = scale(df)
        print(df.columns)
        logging.info("Step 4: Saving preprocessed data.")
        df.to_csv(preprocessed_path, index=False)

        logging.info("Step 5: Reloading saved preprocessed CSV.")
        df = data_val(preprocessed_path)
        t=df.columns
        if 'Unnamed: 0' in t:
           df.drop('Unnamed: 0',axis=1,inplace=True)
        logging.info(df.columns)

        logging.info("Step 6: Splitting data and applying SMOTE to training set.")
        x_train, x_test, y_train, y_test = smote_split(df, target_column='y', test_size=0.2)
        print(x_train)
        print(y_train)
        print(x_test)
        print(y_test)

        logging.info("Step 7: Training and logging the model to MLflow.")
        with mlflow.start_run():
            model = RandomForestClassifier()
            model.fit(x_train, y_train)
            y_pred = model.predict(x_test)
            



            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            re = recall_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)

            mlflow.log_artifact(label_artifact)
            mlflow.log_artifact(scaling_artifact)

            mlflow.log_metric("Accuracy Score", acc)
            mlflow.log_metric("F1_Score", f1)
            mlflow.log_metric("Recall Score", re)
            mlflow.log_metric("Precision Score", prec)

            mlflow.log_param("test_size", 0.2)
            mlflow.log_param("DataFrame shape", str(df.shape))
            mlflow.log_param("SMOTE_applied", True)

            from mlflow.models.signature import infer_signature
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
            joblib.dump(model, "artifacts/Random_ForestModel.jbl")

    except Exception as e:
        logging.error(f"An error occurred during training: {e}")
