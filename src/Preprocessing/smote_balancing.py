

import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

def apply_smote(X, y, random_state=42):
    print("Applying SMOTE to balance the classes...")
    smote = SMOTE(random_state=random_state)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    print(f"Done. New class distribution:\n{y_resampled.value_counts()}")
    return X_resampled, y_resampled

def smote_split(df, target_column='y', test_size=0.2, random_state=42):
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    X = df.drop(columns=[target_column])
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    X_train_bal, y_train_bal = apply_smote(X_train, y_train, random_state=random_state)
    print("Columns in X_train_bal after SMOTE:", X_train_bal.columns.tolist())
    

    return X_train_bal, X_test, y_train_bal, y_test
