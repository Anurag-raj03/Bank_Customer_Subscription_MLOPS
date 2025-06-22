echo "Intialization of the Database"
python Database_connection/making_database_tab.py
python Database_connection/testing_dummy_data.py
echo "Connection with the Database successfully Established"
echo "Starting the FastAPI application"
uvicorn main:app --host 0.0.0.0 --port 8000