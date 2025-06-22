from airflow.decorators import task

@task
def appending_the_datas(
    extracted_data_path="Data_kind_stack/extracted_data/extract_data.csv",
    main_csv_path="Data_kind_stack/main_data/raw_data.csv"
):
    import pandas as pd
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    try:
        if not os.path.exists(extracted_data_path):
            print("Extracted data file does not exist.")
            return

        new_extract = pd.read_csv(extracted_data_path)
        if new_extract.empty:
            print("Extracted data is empty.")
            return

        os.makedirs(os.path.dirname(main_csv_path), exist_ok=True)

        if not os.path.exists(main_csv_path):
            print("Main CSV does not exist. Creating a new one.")
            new_extract.to_csv(main_csv_path, index=False)
            return

        main_csv = pd.read_csv(main_csv_path)

        if main_csv.empty:
            print("Main CSV is empty. Overwriting with new data.")
            new_extract.to_csv(main_csv_path, index=False)
            return

        if list(main_csv.columns) != list(new_extract.columns):
            print("Schema mismatch between main and new extract.")
            return

        updated_csv = pd.concat([main_csv, new_extract], ignore_index=True)
        updated_csv.to_csv(main_csv_path, index=False)
        print(f"Appended data: {new_extract.shape[0]} new rows added. Total rows now: {updated_csv.shape[0]}")

        new_extract.iloc[0:0].to_csv(extracted_data_path, index=False)
        print("Extracted file cleared after appending.")

    except Exception as e:
        print(f"Error in appending data: {e}")
