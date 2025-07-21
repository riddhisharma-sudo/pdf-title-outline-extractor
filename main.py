import os
import json
import re
import pdfplumber
from pathlib import Path
from collections import defaultdict

from utils.extractor import extract_text_blocks, extract_title
from utils.extract_headings import extract_headings_from_words
from utils.text_utils import normalize_spacing  # Not used directly, but useful if needed

INPUT_DIR = "input"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_words_with_metadata(pdf_path):
    all_words = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            words = page.extract_words(extra_attrs=["fontname", "size", "x0", "x1", "top"])
            for w in words:
                all_words.append({
                    "text": w["text"].strip(),
                    "fontname": w.get("fontname"),
                    "size": w.get("size"),
                    "x0": w.get("x0"),
                    "x1": w.get("x1"),
                    "top": w.get("top"),
                    "page": page_num
                })
    return all_words

def process_file(pdf_path):
    print(f"\U0001F4C4 {pdf_path.name}")
    
    words = extract_words_with_metadata(pdf_path)
    
    with pdfplumber.open(pdf_path) as pdf:
        blocks = extract_text_blocks(pdf)
    title = extract_title(blocks)

    outline_data = extract_headings_from_words(words, detected_title=title)

    result = {
        "title": title,
        "outline": outline_data["outline"]
    }

    final_path = Path(OUTPUT_DIR) / f"{pdf_path.stem}.json"
    with open(final_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved: {final_path}")

def main():
    for pdf_file in Path(INPUT_DIR).glob("*.pdf"):
        process_file(pdf_file)

if __name__ == "__main__":
    main()

