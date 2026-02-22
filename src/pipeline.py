from ingest import ingest
from preprocess import preprocess
from train import train
from evaluate import evaluate

def run_pipeline():
    raw_path = ingest()

    if not raw_path:
        return

    processed_path = preprocess(raw_path)

    model_path, acc = train(processed_path)

    evaluate(model_path, acc, threshold=0.8)

if __name__ == "__main__":
    run_pipeline()
