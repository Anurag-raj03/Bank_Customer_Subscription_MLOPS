from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib 
import os

def scale(df: pd.DataFrame) -> pd.DataFrame:
    scalers = {}
    for col in ["age", "balance", "duration"]:
        scaler = StandardScaler()
        df[col] = scaler.fit_transform(df[[col]]).ravel()
        scalers[col] = scaler
    joblib.dump(scalers, os.path.join("artifacts", "scalers.jbl"))    
    return df
