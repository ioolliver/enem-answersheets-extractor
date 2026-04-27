# ENEM Answersheet Extractor

## Project Goal

Create a script that reads an ENEM exam answer sheet PDF and extracts the answers as JSON.

Expected input:

- A PDF file containing ENEM answers.

Expected output:

```json
[
  {
    "index": 1,
    "hasTwoAnswers": true,
    "answer": {
      "english": 0,
      "spanish": 2
    }
  },
  {
    "index": 2,
    "hasTwoAnswers": false,
    "answer": 2
  }
]
```

Answer encoding:

- `A = 0`
- `B = 1`
- `C = 2`
- `D = 3`
- `E = 4`

## Current Implementation

The current implementation extracts answers from text-bearing ENEM PDFs using Poppler's `pdftotext`.

Main files:

- `extract_answers.py`: top-level CLI entry point.
- `src/enem_answersheet_extractor/cli.py`: PDF text extraction, parsing, and JSON output.
- `tests/test_parse_answers.py`: parser unit tests.
- `README.md`: user-facing usage notes.
- `pyproject.toml`: package metadata.

The provided sample file is:

- `pdfs/2025_dia_1.pdf`

Compatibility PDFs currently include day-1 answer keys from 2011 through 2024, plus `pdfs/2024_dia_2.pdf`, which has question 129 marked as `Anulado`.

This PDF is an ENEM answer key with embedded text, not a scanned filled answer sheet. The extractor currently targets this kind of PDF.

## Usage

Run the extractor:

```bash
python3 extract_answers.py pdfs/2025_dia_1.pdf --pretty
```

Write output to a file:

```bash
python3 extract_answers.py pdfs/2025_dia_1.pdf --output answers.json
```

When a question has both English and Spanish alternatives, both are included in the same JSON object under `answer.english` and `answer.spanish`. Questions with one alternative use a numeric `answer` directly.
Canceled questions marked with text such as `Anulado` or `Anulada` are omitted from the output.

## Dependencies

Runtime requirements:

- Python 3.10+
- Poppler command-line tools, specifically `pdftotext`

No Python third-party packages are currently required.

Tesseract OCR is not installed in the current environment, and OpenCV is not installed. The current extractor therefore does not perform OCR or bubble detection.

## Verification

Known passing commands:

```bash
python3 extract_answers.py pdfs/2025_dia_1.pdf --pretty
python3 -m unittest discover -s tests
```

The sample PDF extraction produced 90 answers.
The test suite includes a compatibility matrix for every PDF fixture currently in `pdfs/`. It also checks that every PDF fixture has an explicit compatibility case.

## Current Limitations

- The extractor works with PDFs that contain selectable/extractable text.
- It does not yet process scanned answer sheets or photos.
- It does not yet detect filled bubbles from raster images.
- It assumes ENEM answer letters are `A` through `E`.
- For questions 1-5, ENEM may include both English and Spanish answers; the extractor keeps both in the same output file.
- Canceled questions are ignored instead of being emitted with an answer value.

## Next Likely Step

If the project needs to support scanned or filled answer sheets, add an image-processing pipeline:

1. Render PDF pages to images with Poppler, for example `pdftoppm`.
2. Detect the answer grid and question rows.
3. Detect filled bubbles per row.
4. Map detected bubbles to `A-E`, then to `0-4`.
5. Add image fixtures and tests for scanned sheets.
