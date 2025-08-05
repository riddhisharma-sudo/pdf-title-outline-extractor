

#  **PDF Document Structure Extractor – Adobe Hackathon Round 1A**

This tool is built for Adobe Hackathon **Round 1A: Understand Your Document**.
It extracts the **document title** and a **structured heading hierarchy (H1–H4)** from PDF files using **layout-aware heuristics**, **font-size analysis**, and **text normalization** — **completely offline** and optimized for CPU-only environments.

---

##  **Key Features**

* **Multiline Title Detection**
  Handles stretched or spaced-out letters (e.g., `A p p l i c a t i o n → Application`).

* **Heading Outline Extraction**
  Detects **H1, H2, H3, H4** based on font size and structural patterns.

* **No ML Model Required**
  Pure heuristic-based approach → lightweight and fast.

* **Performance**

  * CPU-only
  * Processes a **50-page PDF in under 10s**
  * Fully **offline**, no internet required

* **Output Format**
  Clean, structured **JSON** containing:

  * Title
  * Heading hierarchy with page numbers

* **Dockerized for Submission**
  Image size ≤ **200MB** (Linux/amd64)

---

##  **Project Structure**

```
adobe_r1a/
├── input/                  # Input PDFs
├── output/                 # Generated JSON outputs
├── main.py                 # Main pipeline script
├── extractor.py            # Optional: block-based extraction variant
├── Dockerfile              # Docker setup for CPU-only runtime
└── utils/
    ├── extract_headings.py # Heading detection heuristics
    ├── text_utils.py       # Text normalization helpers
    └── title_extractor.py  # Multiline title detection logic
```

---

##  **Heuristic Logic**

### **Title Detection**

* Extracted from **top of page 1** using:

  * Largest font size range
  * Line grouping by Y-position
  * Spacing normalization
    *(Example: `A p p l i c a t i o n` → `Application`)*

### **Heading Detection (H1–H4)**

* Uses:

  * **Relative font size hierarchy**
  * **Numeric patterns** (`1.`, `2.1`, `3.1.1`)
  * Known semantic labels (`Table of Contents`, `Acknowledgements`)

---

##  **Docker Setup**

### **Dockerfile**

```dockerfile
FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --prefer-binary --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Default command
CMD ["python", "main.py"]
```

---

##  **Run Instructions**

### **1. Install Dependencies (Local)**

```bash
pip install -r requirements.txt
```

### **2. Process PDFs**

```bash
python main.py
```

Outputs JSON files in the `output/` folder.

---

### **Run with Docker**

**Build Image:**

```bash
docker build -t pdf-structure-extractor .
```

**Run Container:**

```bash
docker run --rm -v $(pwd):/app pdf-structure-extractor
```

---

##  **Expected Output Example**

```json
{
  "title": "Understanding Digital Libraries",
  "outline": [
    {
      "level": "H1",
      "text": "Introduction",
      "page_number": 1
    },
    {
      "level": "H2",
      "text": "Background",
      "page_number": 2
    }
  ]
}
```

---

##  **Future Enhancements**

✔ Smarter detection for **rotated/scanned PDFs**
✔ Support for **multilingual documents**
✔ Visualization of extracted outline in **HTML**

---

**Author:** Riddhi Sharma
**Hackathon:** Adobe India – Understand Your Document (Round 1A)





