set -e
set -o pipefail

echo "[🔁 DVC] Setting up DVC..."

if [ ! -d ".dvc" ]; then
    echo "Initializing DVC without SCM..."
    dvc init --no-scm
fi

if [ ! -f "Data_kind_stack.dvc" ]; then
    echo " Adding Data_kind_stack to DVC..."
    dvc add Data_kind_stack
    dvc commit -m "Added Data_kind_stack"
else
    echo "Data_kind_stack already tracked by DVC"
fi

echo "Initializing Database & Tables..."
python Database_connection/making_database_tab.py

echo "Inserting Dummy Data..."
python Database_connection/testing_dummy_data.py

echo "Launching the app..."
uvicorn main:app --host 0.0.0.0 --port 8000
