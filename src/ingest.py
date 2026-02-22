import os
import shutil
from datetime import datetime

def ingest():
    source_file = "external/new_data.csv"  # simulate new data location

    if not os.path.exists(source_file):
        print("No new data found.")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_file = f"data/raw/data_{timestamp}.csv"

    shutil.copy(source_file, dest_file)

    print(f"Data ingested at {dest_file}")
    return dest_file

