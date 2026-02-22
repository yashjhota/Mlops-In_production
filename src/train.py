import mlflow
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os
from sklearn.metrics import classification_report
import hashlib
import os

BEST_FILE = "models/best_score.txt"



def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()
    

def train(processed_path):
    df = pd.read_csv(processed_path)

    X = df[["feature"]]  # modify later
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=42)

    model = LogisticRegression(random_state=42)

    with mlflow.start_run():

        model.fit(X_train, y_train)

        acc = model.score(X_test, y_test)
        

        

        model_path = "models/model.pkl"
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, model_path)

        data_hash = file_hash(processed_path)

        if os.path.exists(BEST_FILE):
            with open(BEST_FILE, "r") as f:
                best_score = float(f.read())
        else:
            best_score = 0

        if acc > best_score:
            joblib.dump(model, "models/production_model.pkl")
            with open(BEST_FILE, "w") as f:
                f.write(str(acc))
        
        report = classification_report(y_test, model.predict(X_test), output_dict=True)
                
        
        mlflow.log_metric("accuracy", acc)
        mlflow.log_artifact(model_path)
        mlflow.log_param("data_hash", data_hash)
        mlflow.log_metric("precision", report["weighted avg"]["precision"])
        mlflow.log_metric("recall", report["weighted avg"]["recall"])
        mlflow.log_metric("f1_score", report["weighted avg"]["f1-score"])

    print("Training complete.")
    return model_path , acc

