import os
import pandas as pd

def load_context_data(file_path="src/Data/Banking_Call_Data.xlsx", sheet_name=0):
    return pd.read_excel(file_path, sheet_name=sheet_name)

def format_customer_input(data: dict) -> str:
    return "\n".join([f"{key.capitalize()}: {value}" for key, value in data.items()])
