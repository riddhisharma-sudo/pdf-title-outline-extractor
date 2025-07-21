# 📄 PDF Document Structure Extractor – Adobe Hackathon Round 1A

This project is a CPU-only, offline tool designed for Adobe's Round 1A challenge: **"Understand Your Document"**.

It extracts the **document title** and a **structured outline (H1–H4)** from PDFs using layout-aware heuristics, text block parsing, and smart spacing normalization.

---

## 🚀 Features

- ✅ Accurate multiline **title** detection (handles stretched/merged letters)
- ✅ Heading hierarchy extraction: **H1, H2, H3, H4**
- ✅ Font-size + layout-based detection (no ML inference required)
- ✅ Output in clean structured **JSON** format
- ✅ Works offline in under 10s per 50-page document
- ✅ Fully Dockerized (≤200MB image, linux/amd64)

---

## 📂 Project Structure

adobe_r1a/
├── input/ # Input PDFs
├── output/ # Output JSONs
├── main.py # Main pipeline script
├── extractor.py # Optional block-based extractor
├── Dockerfile # Build for offline CPU-only Docker image
└── utils/
├── extract_headings.py # Heuristic heading detector
├── text_utils.py # Spacing normalizer
└── title_extractor.py # Multiline title logic

Heuristic Logic
Title is selected from the top of page 1 using:

Largest font size range

Line grouping by Y-position

Spacing normalization (e.g., A p p l i c a t i o n → Application)

Headings (H1–H4) are identified using:

Relative font sizes across pages

Numeric and semantic patterns (e.g., 1., 2.1, 3.1.1)

Known labels (e.g., "Table of Contents", "Acknowledgements")

