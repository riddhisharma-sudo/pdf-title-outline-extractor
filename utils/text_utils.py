from typing import List, Dict

def reconstruct_text(words: List[Dict]) -> str:
    words_sorted = sorted(words, key=lambda w: w["x0"])
    text = ""
    for i, w in enumerate(words_sorted):
        if i > 0 and (w["x0"] - words_sorted[i - 1]["x1"]) > 3.0:
            text += " "
        text += w["text"]
    return text.strip()

import re

def normalize_spacing(text: str) -> str:
    # Fix spaced-out text like "A p p l i c a t i o n"
    if re.fullmatch(r"(?:[A-Za-z]\s+){2,}[A-Za-z]", text):
        return text.replace(" ", "")
    
    # Fix camelCase or PascalCase titles with no spaces
    spaced = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)
    
    # Collapse repeated characters (e.g., RRR -> R)
    spaced = re.sub(r'(.)\1{2,}', r'\1', spaced)

    # Final whitespace normalization
    return re.sub(r"\s+", " ", spaced.strip())
