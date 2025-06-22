import pandas as pd

def load_input_raw_data(data: dict):
    try:
        df = pd.DataFrame([data])
        return df
    except Exception as e:
        raise RuntimeError(f"Error loading raw input: {e}")

def preprocess_input(data_dict: dict, label_encoder, scaler):
    try:
        df = pd.DataFrame([data_dict])
        return _transform(df, label_encoder, scaler)
    except Exception as e:
        raise RuntimeError(f"Preprocessing (dict) error: {e}")
    
def preprocess_input_df(df: pd.DataFrame, label_encoder: dict, scaler: dict) -> pd.DataFrame:
    try:

        for col, encoder in label_encoder.items():
            if col in df.columns:
                df[col] = encoder.transform(df[col].astype(str))  
            else:
                print(f"Warning: Column '{col}' not found for label encoding.")


        for col, scaler_obj in scaler.items():
            if col in df.columns:
                df[col] = scaler_obj.transform(df[[col]]).flatten()  
            else:
                print(f"Warning: Column '{col}' not found for scaling.")

        return df

    except Exception as e:
        print(f"Error in preprocess_input_df: {e}")
        raise e
    except Exception as e:
        raise RuntimeError(f"Preprocessing (DataFrame) error: {e}")

def _transform(df: pd.DataFrame, label_encoder, scaler):
    for col, encoder in label_encoder.items():
        if col in df.columns:
            df[col] = encoder.transform(df[col])

    for col, scaler_obj in scaler.items():
        if col in df.columns:
            df[col] = scaler_obj.transform(df[[col]])

    return df

def predicts(df, model):
    try:
        prediction = model.predict(df)[0]
        return prediction
    except Exception as e:
        raise RuntimeError(f"Prediction error: {e}")
