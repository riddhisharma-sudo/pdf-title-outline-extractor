import re
from collections import defaultdict
from utils.text_utils import normalize_spacing

def extract_title_from_words(words):
    page1_words = [w for w in words if w["page"] == 1]
    if not page1_words:
        return "Untitled"

    max_size = max(w["size"] for w in page1_words)
    title_words = [w for w in page1_words if w["size"] >= 0.9 * max_size]

    if not title_words:
        return "Untitled"

    # Group by line Y position
    lines_by_y = defaultdict(list)
    for w in title_words:
        y = round(w["top"], 1)
        lines_by_y[y].append(w)

    sorted_lines = sorted(lines_by_y.items(), key=lambda kv: kv[0])
    lines = []
    for _, line_words in sorted_lines:
        line_words = sorted(line_words, key=lambda w: w["x0"])
        line_text = " ".join(w["text"] for w in line_words)
        lines.append(line_text)

    raw_title = " ".join(lines)
    normalized = normalize_spacing(raw_title)

    print(f"[DEBUG] Final cleaned title: {normalized}")
    return normalized.strip()
