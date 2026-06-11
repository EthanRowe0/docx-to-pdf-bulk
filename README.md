# docx-to-pdf-bulk

Batch-convert entire folders of `.doc` and `.docx` files to PDF with a single command.  
On Windows it drives **Microsoft Word** via COM automation, so output quality is identical to "Save As PDF" from within Word itself.

---

## Requirements

| Requirement | Notes |
|---|---|
| **Python 3.9+** | [python.org](https://www.python.org/downloads/) |
| **Microsoft Word** | Required on Windows for conversion |

> On macOS, `docx2pdf` uses Word for Mac if installed, or falls back to LibreOffice.  
> On Linux, [LibreOffice](https://www.libreoffice.org/) must be installed and on your `PATH`.

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/docx-to-pdf-bulk.git
cd docx-to-pdf-bulk

# 2. Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Basic — output goes to `<source>/pdf_output/`
```bash
python converter.py "C:\path\to\your\documents"
```

### Specify an output folder
```bash
python converter.py "C:\path\to\your\documents" --output "C:\path\to\pdfs"
```

### Re-convert files that already have a PDF
```bash
python converter.py ./docs --output ./pdfs --overwrite
```

### Verbose mode (prints each file as it converts)
```bash
python converter.py ./docs --verbose
```

### Windows — drag & drop
Drag any folder onto **`convert.bat`** and it will convert everything inside.

---

## All options

```
usage: converter.py [-h] [--output OUTPUT] [--overwrite] [--verbose] [--no-banner] source

positional arguments:
  source                Source folder containing DOC/DOCX files (searched recursively)

options:
  -h, --help            show this help message and exit
  --output, -o OUTPUT   Output folder for PDFs
  --overwrite           Re-convert even if a PDF already exists
  --verbose, -v         Print each file as it is processed
  --no-banner           Suppress the ASCII banner
```

---

## How it works

1. Recursively scans the source folder for `.doc` and `.docx` files.
2. Mirrors the folder structure in the output directory.
3. Skips files that already have a corresponding PDF (use `--overwrite` to force).
4. Prints a summary of converted / skipped / failed files when done.

---

## Example output

```
  Source : C:\Users\You\Documents\reports
  Output : C:\Users\You\Documents\reports\pdf_output

  Found 12 file(s) to process.

  Converting: 100%|████████████████████| 12/12 [00:18<00:00,  1.5s/file]

────────────────────────────────────────────────────────────
  RESULTS
────────────────────────────────────────────────────────────
  Total found   : 12
  Converted     : 11
  Skipped       : 0  (PDF already exists)
  Failed        : 1
  Time elapsed  : 18.3s
  Output folder : C:\Users\You\Documents\reports\pdf_output
────────────────────────────────────────────────────────────
```

---

## License

MIT
