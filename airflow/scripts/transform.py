from airflow.decorators import task

@task
def transforming_data(
    extracted_raw_path="Data_kind_stack/extracted_data/extract_data.csv",
    trans_database_path="Data_kind_stack/transform_data/transformed_database_data.csv"

):
    import pandas as pd
    import os
    import sys
    import joblib

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from BACKEND.prediciton_pipeline import preprocess_input_df  

    try:

        label_encoder = joblib.load("artifacts/label_encoders.jbl")
        scaler = joblib.load("artifacts/scalers.jbl")

        df_raw = pd.read_csv(extracted_raw_path)


        df_transformed = preprocess_input_df(df_raw, label_encoder, scaler)

        if df_transformed.empty:
            print("The transformed data is empty.")
            return trans_database_path

        os.makedirs(os.path.dirname(trans_database_path), exist_ok=True)
        df_transformed.to_csv(trans_database_path, index=False, mode='a', header=not os.path.exists(trans_database_path))
        
        print(f"Transformed data saved at: {trans_database_path}")
        return trans_database_path

    except Exception as e:
        print(f"Error in transforming the data: {e}")
        raise e
