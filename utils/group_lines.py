from collections import defaultdict

from collections import defaultdict

def group_words_by_line(words, y_tolerance=2.0):
    """Group words into lines based on Y-coordinate proximity."""
    lines = defaultdict(list)
    for w in words:
        rounded_y = round(w["top"] / y_tolerance) * y_tolerance
        lines[(w["page"], rounded_y)].append(w)

    grouped_lines = []
    for (page, _), line_words in lines.items():
        line_words = sorted(line_words, key=lambda w: w["x0"])
        text = ""
        for i, w in enumerate(line_words):
            if i > 0 and (w["x0"] - line_words[i - 1]["x1"]) > 2.0:
                text += " "
            text += w["text"]

        if text.strip():
            grouped_lines.append({
                "text": text.strip(),
                "font_size": max(w["size"] for w in line_words),
                "top": min(w["top"] for w in line_words),
                "page": page,
                "words": line_words
            })

    return grouped_lines
