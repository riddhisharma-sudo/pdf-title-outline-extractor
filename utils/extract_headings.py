import re
from typing import List, Dict
from collections import Counter
from .group_lines import group_words_by_line

def is_probable_form_document(lines: List[Dict]) -> bool:
    short_lines = [line for line in lines if len(line["text"]) < 40]
    return len(short_lines) / len(lines) > 0.7

def is_junk(text: str) -> bool:
    text = text.strip().lower()
    return (
        not text or
        len(text) <= 2 or
        re.fullmatch(r"[\divxlc]+\.*\)?", text)
    )

def normalize_text(text: str) -> str:
    return re.sub(r'(.)\1{2,}', r'\1', text)

def merge_multiline_headings(blocks: List[Dict]) -> List[Dict]:
    if not blocks:
        return []

    merged = []
    buffer = [blocks[0]]

    for curr in blocks[1:]:
        prev = buffer[-1]
        if (
            curr["page"] == prev["page"] and
            abs(curr["top"] - prev["top"]) < 2.5 and
            round(curr["font_size"], 1) == round(prev["font_size"], 1)
        ):
            buffer.append(curr)
        else:
            merged.append({
                "text": " ".join(b["text"].strip() for b in buffer),
                "font_size": buffer[0]["font_size"],
                "page": buffer[0]["page"],
                "top": buffer[0]["top"]
            })
            buffer = [curr]

    if buffer:
        merged.append({
            "text": " ".join(b["text"].strip() for b in buffer),
            "font_size": buffer[0]["font_size"],
            "page": buffer[0]["page"],
            "top": buffer[0]["top"]
        })

    return merged

def extract_headings_from_words(words: List[Dict], detected_title=None, exclude_texts=None) -> Dict:
    exclude_texts = set(exclude_texts or [])
    lines = group_words_by_line(words)
    lines = merge_multiline_headings(lines)

    if is_probable_form_document(lines):
        return {"outline": []}

    size_counter = Counter(round(line["font_size"], 1) for line in lines)
    sorted_sizes = sorted(size_counter.items(), key=lambda x: -x[0])
    heading_levels = {size: f"H{idx + 1}" for idx, (size, _) in enumerate(sorted_sizes[:4])}

    known_h1_labels = {"revision history", "table of contents", "acknowledgements"}
    seen = set()
    outline = []

    for line in lines:
        size = round(line["font_size"], 1)
        raw_text = line["text"].strip()
        text = normalize_text(raw_text)
        lowered = text.lower()

        if detected_title and lowered in detected_title.lower():
            continue
        if text in exclude_texts:
            continue
        if is_junk(text):
            continue
        if len(text.split()) > 20:
            continue
        if text.lower() in seen:
            continue
        if re.match(r"^\d+\.\d+", text) and text[4:].strip() and text[4:].strip()[0].islower():
            continue

        text = re.sub(r"\.{3,}\s*\d{1,3}$", "", text).strip()

        if lowered in known_h1_labels:
            level = "H1"
        elif re.match(r"^\d+\.\d+\.\d+", text):
            level = "H4"
        elif re.match(r"^\d+\.\d+", text):
            level = "H3"
        elif re.match(r"^\d+\.", text):
            level = "H2"
        elif size in heading_levels:
            level = heading_levels[size]
        else:
            continue

        outline.append({
            "level": level,
            "text": text,
            "page": line["page"]
        })
        seen.add(text.lower())

    return {"outline": outline}

