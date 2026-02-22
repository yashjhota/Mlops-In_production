from fastapi import FastAPI
import joblib
import os
import numpy as np
import json
from datetime import datetime
import time

app = FastAPI()

MODEL_PATH = "models/production_model.pkl"
LOG_FILE = "logs/predictions.jsonl"

def log_prediction(input_value, output_value):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "input": float(input_value),
        "prediction": int(output_value)
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


last_loaded_time = 0
model = None

def get_model():
    global last_loaded_time, model
    
    if not os.path.exists(MODEL_PATH):
        raise Exception("No production model available.")
    
    modified_time = os.path.getmtime(MODEL_PATH)

    if modified_time != last_loaded_time:
        model = joblib.load(MODEL_PATH)
        last_loaded_time = modified_time
        print("Model reloaded from disk.")
    
    return model

@app.get("/predict")
def predict(feature: float):
    model = get_model()
    prediction = model.predict(np.array([[feature]]))
    log_prediction(feature, prediction)
    return {"prediction": int(prediction[0])}