#!/bin/bash

cd /app

echo "Running DVC add..."
dvc add Data_kind_stack

echo "Adding to Git..."
git add Data_kind_stack.dvc .gitignore

echo "Committing changes..."
git commit -m "Update Data_kind_stack with new changes"

echo "Pushing to remote DVC storage..."
dvc push
