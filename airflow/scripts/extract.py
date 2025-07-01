from airflow.decorators import task

@task
def extraction_data(
    db_name: str,
    table_name: str,
    extracted_data_path="Data_kind_stack/extracted_data/extract_data.csv",
    reference_drift_data="Data_kind_stack/extracted_data/reference_drift_data.csv"
    
):
    import pandas as pd
    from sqlalchemy import create_engine
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from Database_connection.db_init import clear_table

    try:
        DATABASE_URL = f"postgresql://postgres:admin@postgres:5432/{db_name}"
        engine = create_engine(DATABASE_URL)
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql(query, con=engine)

        if df.empty:
            print(f"Extraction Task: Table `{table_name}` in `{db_name}` has no data.")
            return None

        os.makedirs(os.path.dirname(extracted_data_path), exist_ok=True)

        df.to_csv(extracted_data_path, index=False)

        if os.path.exists(reference_drift_data) and os.path.getsize(reference_drift_data) > 0:
            df.to_csv(reference_drift_data, mode='a', index=False, header=False)
        else:
            df.to_csv(reference_drift_data, mode='w', index=False, header=True)

        print(f"Extraction completed from `{table_name}`, saved to: {extracted_data_path}")

        clear_table(db_name, table_name)

        return extracted_data_path

    except Exception as e:
        print(f"Error during extraction from `{table_name}`: {e}")
        raise e
