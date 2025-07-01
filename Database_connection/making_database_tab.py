import time
from db_init import create_database, create_table

db_name = "banking_costumer_data"
table1 = "temp_table_new_costumer"
table2 = "banking_new_data_history"
table3 = "new_data_preprocess_table"


MAX_RETRIES = 10
for attempt in range(MAX_RETRIES):
    try:
        print(f"[Try {attempt+1}] Attempting DB setup...")
        create_database(db_name)
        create_table(db_name, table1)
        create_table(db_name, table2)

        print("Database and tables created successfully.")
        
        break
    except Exception as e:
        print(f"Error during DB setup: {e}")
        if attempt < MAX_RETRIES - 1:
            time.sleep(5)
        else:
            print("Exceeded max retries. Failing...")
