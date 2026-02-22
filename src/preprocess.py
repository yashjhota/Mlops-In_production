import pandas as pd
import os

def preprocess(raw_path):
    df = pd.read_csv(raw_path)

    df = df.dropna()

    processed_path = raw_path.replace("raw", "processed")
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)

    df.to_csv(processed_path, index=False)

    print(f"Data processed at {processed_path}")
    return processed_path
