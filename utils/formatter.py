import json
import os

def save_as_json(data, filename, output_dir):
    output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
