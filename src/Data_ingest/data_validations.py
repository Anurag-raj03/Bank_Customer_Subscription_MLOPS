def data_val(path:str):
    import pandas as pd
    if path:
        if path.split('.')[-1].lower()=='csv':
            df=pd.read_csv(path)
        elif path.split('.')[-1].lower()=='xlsx':
            df=pd.read_excel(path)
        elif path.split('.')[-1].lower()=='parquet':     
             df=pd.read_parquet(path)
        else:
            print(f"The format of the File is not valid --> {path.split('.')[-1]}")    
    return df          