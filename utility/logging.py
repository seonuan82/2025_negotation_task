import os
import json
from datetime import datetime

def log(text, user_id=""):
    with open(f"log/negotiation_log_{user_id}.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")

def log_json(data, user_id):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = f"logs/{user_id}/{timestamp}.json"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
