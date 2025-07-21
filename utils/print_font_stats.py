import pdfplumber
from collections import Counter
from pathlib import Path

INPUT_DIR = "input"

def scan_fonts(pdf_path):
    font_sizes = Counter()
    font_names = Counter()

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for word in page.extract_words(extra_attrs=["fontname", "size"]):
                font_sizes[word["size"]] += 1
                font_names[word["fontname"]] += 1

    return font_sizes, font_names

def main():
    for file in Path(INPUT_DIR).glob("*.pdf"):
        print(f"\n📄 {file.name}")
        font_sizes, font_names = scan_fonts(str(file))

        print("  🔠 Font Sizes:")
        for size, count in sorted(font_sizes.items(), key=lambda x: -x[1]):
            print(f"    {size:.2f}: {count} times")

        print("  🅱 Font Names (may help detect bold):")
        for name, count in sorted(font_names.items(), key=lambda x: -x[1])[:5]:
            print(f"    {name}: {count} times")

if __name__ == "__main__":
    main()
