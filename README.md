# **cis6930sp25 -- Project 2**

**Name:** Ruchita Potamsetti

---

## **Assignment Description**

This projects redacts senstive information from the provided pdfs. There are various ways this can be done using this script. Using --names we can provide specific names that we want to redact. Similarly using --entities will redact all the PERSON entities in the pdf. Using --coref will redact all the coreferences in the pdf. The text from the pdf is extracted and edited using Pymupdf and spacy is used for entity resolution.

---

## **Project Structure** 

```plaintext
cis6930sp25-project1/
├── COLLABORATORS.md              # A markdown file describing collaborations and inspirations taken from other websites.
├── Pipfile                       # Defines the dependencies and virtual environment for the project (used with pipenv).
├── README.md                     # Project description and instructions.
├── main.py                       # Main Python script that contains the core functionality of the project.
├── pyproject.toml                # Configuration file for the project, used by pipenv.
├── Project1_demo.gif             # Demo video
└── resources/                    # files to be redacted
    ├── test1.py     
    └── test2.py
└── output/                       # files after redaction
    ├── test1.py     
    └── test2.py
└── stats/                        # stats generated     
    └── stats1.py 
└── tests/                        # Directory containing all test files.
    ├── test_entity_detection.py  # Tests for verifying entity recognition logic and name matching.
    ├── test_redaction.py         # Tests for PDF text extraction and redaction functionality.
    └── test_stats_output.py      # Tests for validating stats file format and output completeness.
```

---

## **To Install**
This will create a virtual environment:
```sh
uv venv
```
To activate the virtual environment run:
Windows:
```sh
.venv\Scripts\activate
```
Mac:
```sh
source .venv/bin/activate
```
To install the necessary dependencies using `uv`, run:
```sh
uv pip install .
```
Install the model:
```sh
uv run -m spacy download en_core_web_sm
```
To deactivate the virtual environment run:
```sh
deactivate
```

---

## **To Run**
Execute the program using:
```sh
uv run python main.py --input "resources/*.pdf" --output myoutput/ --names "Bonilla" --names "Tulli Papyrus" --entities --coref
```

---

## **Example Output**
```sh
uv run python main.py --input "resources/test1.pdf" --output myoutput/ --names "Bonilla" --names "Tulli Papyrus"

test1.pdf       76x123  Tulli Papyrus   13      Name
test1.pdf       472x136 Tulli Papyrus   13      Name
test1.pdf       78x364  Bonilla 7       Name
test1.pdf       422x352 Bonilla 7       Name
test1.pdf       367x374 Bonilla 7       Name

```

---

## **To Test**
After installing, use the command below to execute the pytests:
```sh
uv run pytest
```

---

### **Demo**
![https://github.com/ruchipotamsetti/cis6930sp25-project2/blob/main/demo.gif]()

---



## **Features and Functions**

### **`main.py`**
- **`extract_pdf_text(file_path)`**  
  - Extracts text content from a PDF file page-by-page.
  - Parameters:
    - file_path (str): Path to input PDF file.
  - Returns: tuple (document object, list of page texts).

- **`get_named_entities(text, names, redact_all, coref)`**  
  - Identifies entities using spaCy's NLP pipeline with configurable options.
  - Parameters:
    - text (str): Text content to analyze.
    - names (list): Specific names to redact (case-sensitive).
    - redact_all (bool): Redact all PERSON entities when True.
    - coref (bool): Include coreference pronouns when True.
  - Returns: list of tuples (text, start, end, label) representing entities.

- **`redact_entities_in_pdf(doc, entities_by_page, pdf_filename, stats_file_handle)`**  
  - Applies redaction annotations to PDF document pages.
  - Parameters:
    - doc: PyMuPDF document object.
    - entities_by_page: List of entities per page.
    - pdf_filename: Original PDF filename for logging.
    - stats_file_handle: File handle for redaction statistics.

- **`redact_pdf(pdf_path, output_path, names, redact_all, stats_file_handle, coref)`**  
  - Main PDF processing workflow from input to redacted output.
  - Parameters:
    - pdf_path: Input PDF file path.
    - output_path: Directory for saving redacted PDFs.
    - names: List of specific names to redact.
    - redact_all: Boolean flag for comprehensive redaction.
    - stats_file_handle: Handle for statistics logging.
    - coref: Boolean flag for coreference resolution.

- **Command Line Arguments**  
  - `--input`: Specify file patterns for PDF inputs (supports glob)
  - `--output`: Define output directory for redacted PDFs
  - `--names`: List specific case-sensitive names to redact
  - `--entities`: Flag to redact all PERSON entities
  - `--coref`: Flag to redact coreference pronouns
  - `--stats`: Specify statistics file path (default: stderr)

**Key Features:**
- Page-level text extraction and processing
- Configurable entity recognition (specific names or all PERSON entities)
- Coreference resolution for pronouns (he/she/they etc.)
- Redaction statistics logging with location coordinates
- Batch processing of multiple PDF files using glob patterns
- Safe PDF handling with explicit file closures

**Dependencies:**
- spaCy (en_core_web_sm model) for NLP processing
- PyMuPDF (fitz) for PDF manipulation
- Standard libraries: os, sys, glob, argparse

---

## **Bugs and Assumptions**
1. **Text-Based PDFs**: Assumes PDFs contain selectable text layers (not scanned documents)
2. **SpaCy Accuracy**: Relies on spaCy's `en_core_web_sm` model for perfect PERSON entity detection
3. **Word Boundaries**: Assumes entity text matches PDF text exactly (no hyphenation/formatting variations)
4. **File Handling**: 
   - Overwrites existing files in output directory with same filenames
   - Requires write permissions for output directory and stats file path
   - Assumes UTF-8 encoding for all text operations

---
