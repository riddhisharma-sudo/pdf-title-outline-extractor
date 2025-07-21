import pdfplumber
import os
import json
import re
from collections import defaultdict

def normalize_spacing(text):
    text = text.strip()

    # Collapse spaced characters (e.g., "A p p l i c a t i o n" → "Application")
    if re.fullmatch(r"(?:[A-Za-z]\s+){2,}[A-Za-z]", text):
        return text.replace(" ", "")

    # Add space between lowercase-uppercase transitions: "OverviewFoundation" → "Overview Foundation"
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)

    # Collapse repeated letters (e.g., "RRRRRR" → "R")
    text = re.sub(r'(.)\1{2,}', r'\1', text)

    # Normalize whitespace
    return re.sub(r"\s+", " ", text).strip()

def is_junk_heading(text):
    return bool(re.fullmatch(r'\d+\.?', text.strip()))

def extract_text_blocks(pdf):
    blocks = []
    for page_num, page in enumerate(pdf.pages, 1):
        for obj in page.extract_words(
            use_text_flow=True,
            keep_blank_chars=False,
            extra_attrs=["size", "fontname", "top", "bottom"]
        ):
            text = obj["text"].strip()
            if not text:
                continue
            blocks.append({
                "text": text,
                "font_size": float(obj["size"]),
                "x0": obj["x0"],
                "x1": obj["x1"],
                "top": obj["top"],
                "bottom": obj["bottom"],
                "page": page_num
            })
    return blocks

def extract_title(blocks):
    if not blocks:
        return "Untitled"

    # Find largest font size blocks on the first page
    sorted_blocks = sorted(blocks, key=lambda b: (-b["font_size"], b["page"], b["top"]))
    top_font_size = sorted_blocks[0]["font_size"]
    top_blocks = [b for b in sorted_blocks if abs(b["font_size"] - top_font_size) < 0.5 and b["page"] == sorted_blocks[0]["page"]]

    lines_by_y = defaultdict(list)
    for b in top_blocks:
        lines_by_y[round(b["top"], 1)].append(b)

    title_lines = []
    for _, line_blocks in sorted(lines_by_y.items()):
        sorted_words = sorted(line_blocks, key=lambda w: w["x0"])
        line_text = " ".join(w["text"] for w in sorted_words)
        title_lines.append(line_text)

    raw_title = " ".join(title_lines).strip()
    return normalize_spacing(raw_title)

def merge_multiline_headings(blocks, min_font_size=10.0):
    merged, buffer = [], []
    prev_y = prev_font = prev_page = None

    for block in blocks:
        text = block["text"]
        font = block["font_size"]
        y = block["top"]
        page = block["page"]

        if buffer and font == prev_font and page == prev_page and abs(y - prev_y) < 12:
            buffer.append(block)
            prev_y = y
        else:
            if buffer:
                merged.append({
                    "text": " ".join([b["text"] for b in buffer]),
                    "font_size": buffer[0]["font_size"],
                    "page": buffer[0]["page"]
                })
            buffer = [block]
            prev_y, prev_font, prev_page = y, font, page

    if buffer:
        merged.append({
            "text": " ".join([b["text"] for b in buffer]),
            "font_size": buffer[0]["font_size"],
            "page": buffer[0]["page"]
        })
    return merged

def build_outline(blocks, title_text):
    headings = []
    merged = merge_multiline_headings(blocks)

    font_sizes = sorted(set(b["font_size"] for b in merged), reverse=True)
    h1_font, h2_font, h3_font = (font_sizes + [0.0, 0.0, 0.0])[:3]

    for b in merged:
        text = b["text"].strip()
        if not text or text == title_text or is_junk_heading(text):
            continue
        if abs(b["font_size"] - h1_font) < 0.5:
            level = "H1"
        elif abs(b["font_size"] - h2_font) < 0.5:
            level = "H2"
        elif abs(b["font_size"] - h3_font) < 0.5:
            level = "H3"
        else:
            continue
        headings.append({
            "level": level,
            "text": text,
            "page": b["page"]
        })
    return headings

def process_pdf(path):
    with pdfplumber.open(path) as pdf:
        blocks = extract_text_blocks(pdf)
        title = extract_title(blocks)
        outline = build_outline(blocks, title)
        return {
            "title": title,
            "outline": outline
        }

def process_folder(folder_path):
    results = {}
    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, file)
            result = process_pdf(file_path)
            results[file] = result
    return results

if __name__ == "__main__":
    input_folder = "input"
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    results = process_folder(input_folder)
    for filename, data in results.items():
        name = os.path.splitext(filename)[0]
        out_path = os.path.join(output_folder, name + ".json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    print("✅ Extraction complete.")
print(normalize_spacing("OverviewFoundationLevelExtensions"))  # Expect: "Overview Foundation Level Extensions"
print(normalize_spacing("A p p l i c a t i o n"))               # Expect: "Application"
print(normalize_spacing("R R F F P P"))                         # Expect: "RFP"
