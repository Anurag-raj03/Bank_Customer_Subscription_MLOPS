from airflow.decorators import task

@task
def appending_the_datas(
    extracted_data_path="Data_kind_stack/extracted_data/extract_data.csv",
    reference_drift_data="Data_kind_stack/extracted_data/reference_drift_data.csv",
    main_csv_path="Data_kind_stack/main_data/raw_data.csv"
):
    import pandas as pd
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    try:
        if not os.path.exists(reference_drift_data):
            print("Reference drift data file does not exist.")
            return

        ref_data = pd.read_csv(reference_drift_data)
        if ref_data.empty:
            print("Reference drift data is empty.")
            return

        last_row = ref_data.tail(1)

        os.makedirs(os.path.dirname(main_csv_path), exist_ok=True)

        if not os.path.exists(main_csv_path):
            last_row.to_csv(main_csv_path, index=False)
        else:
            main_csv = pd.read_csv(main_csv_path)
            if list(main_csv.columns) != list(last_row.columns):
                print("Schema mismatch.")
                return
            updated_csv = pd.concat([main_csv, last_row], ignore_index=True)
            updated_csv.to_csv(main_csv_path, index=False)
            print(f"Appended last row from reference data to main CSV. Total rows now: {updated_csv.shape[0]}")

        if os.path.exists(extracted_data_path):
            pd.DataFrame(columns=ref_data.columns).to_csv(extracted_data_path, index=False)
            print("Extracted data file cleared.")

    except Exception as e:
        print(f"Error in appending data: {e}")
