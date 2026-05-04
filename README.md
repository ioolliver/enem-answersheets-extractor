# ENEM Answersheet Extractor

Extract answers from an ENEM PDF into JSON.

The output format is:

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

Answers are encoded as `A=0`, `B=1`, `C=2`, `D=3`, `E=4`.

## Usage

```bash
python3 extract_answers.py pdfs/2024_dia_1.pdf --pretty
```

To extract every PDF in the `pdfs/` folder into one JSON array:

```bash
python3 extract_answers.py pdfs --pretty
```

That folder output format is:

```json
[
  {
    "year": 2024,
    "day": 1,
    "application": "normal",
    "sheet": [
      {
        "index": 1,
        "hasTwoAnswers": true,
        "answer": {
          "english": 2,
          "spanish": 2
        }
      }
    ]
  }
]
```

Application is inferred from the filename suffix. Files named like `2024_dia_1_ppl.pdf`, `2024_dia_1_digital.pdf`, or `2024_dia_1_terceira.pdf` output `application` as `ppl`, `digital`, or `terceira`. Files without an application suffix output `normal`.

To extract only one application type from a folder:

```bash
python3 extract_answers.py pdfs --application-only ppl --pretty
```

When an ENEM row contains both English and Spanish alternatives, the output includes both in `answer.english` and `answer.spanish`. Rows with a single alternative use a numeric `answer` directly.

Canceled questions marked with text such as `Anulado` or `Anulada` are omitted from the output.

The script requires Poppler's `pdftotext` command to be installed.

## Tests

Run the test suite:

```bash
python3 -m unittest discover -s tests
```

The suite includes parser tests and a PDF compatibility matrix for selected known PDF fixtures.
