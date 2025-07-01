from db_init import insert_subscriber

DB_NAME = "banking_costumer_data"
TABLE_NAME = "temp_table_new_costumer"

dummy_record = {
    'age': 32,
    'job': 'admin.',
    'marital': 'married',
    'education': 'primary',
    'default': 'no',
    'balance': 1200,
    'housing': 'yes',
    'loan': 'no',
    'contact': 'cellular',
    'day': 15,
    'month': 'may',
    'duration': 180,
    'campaign': 3,
    'pdays': -1,
    'previous': 0,
    'poutcome': 'other',
    'y': 'yes'
}

try:
  insert_subscriber(DB_NAME, TABLE_NAME, dummy_record)
  print("Dummy Data insertion completed")
except Exception as e:
  print(f"Failed to inser Data in {DB_NAME} {TABLE_NAME}")
  raise e    
