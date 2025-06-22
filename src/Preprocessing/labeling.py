import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder
import joblib
def label_encod(df:pd.DataFrame)->pd.DataFrame:
    encoders={}
    for i in ["job","marital","education","default","housing","loan","contact","month","poutcome","y"]:
        le=LabelEncoder()
        df[i]=le.fit_transform(df[i])
        encoders[i]=le 
    joblib.dump(encoders,os.path.join("artifacts","label_encoders.jbl"))    
    
    return df
    


    
