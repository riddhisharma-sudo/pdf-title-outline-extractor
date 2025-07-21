import json
from pathlib import Path

DEBUG_JSON = Path("output/sample_debug.json")  # replace with your actual file
OUTPUT_JSON = Path("output/sample_structured.json")

def load_debug_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def trim_for_prompt(data, max_words=2000):
    """Trim input data to avoid exceeding token limits."""
    trimmed = []
    total_words = 0
    for item in data:
        word_count = len(item["text"].split())
        if total_words + word_count > max_words:
            break
        trimmed.append(item)
        total_words += word_count
    return trimmed

def prepare_prompt(raw_data):
    text_lines = [f"{d['text']} [pg {d['page']}]" for d in raw_data]
    prompt = (
        "You are a PDF document analysis expert. "
        "Given the following extracted text blocks with page numbers, "
        "identify the **document title** and **generate a structured outline** of headings.\n\n"
        "Each heading should have:\n"
        "- level: H1 / H2 / H3 / H4 based on font size or semantic cues\n"
        "- text: clean heading text\n"
        "- page: page number\n\n"
        "Return your result in this JSON format:\n\n"
        "{\n"
        "  \"title\": \"...\",\n"
        "  \"outline\": [\n"
        "    {\"level\": \"H1\", \"text\": \"...\", \"page\": 1},\n"
        "    {\"level\": \"H2\", \"text\": \"...\", \"page\": 2},\n"
        "    ...\n"
        "  ]\n"
        "}\n\n"
        "Here is the input text:\n\n"
        + "\n".join(text_lines)
    )
    return prompt

def save_output(output_data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    raw = load_debug_json(DEBUG_JSON)
    trimmed = trim_for_prompt(raw)
    prompt = prepare_prompt(trimmed)

    # 👇 You now manually copy this `prompt` and paste it into ChatGPT
    print("\n=== COPY BELOW PROMPT INTO CHATGPT ===\n")
    print(prompt)
    print("\n=== END PROMPT ===\n")

    print("⚠️ After you get response, paste the JSON below and I’ll save it for you.")
