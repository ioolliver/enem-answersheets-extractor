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

When an ENEM row contains both English and Spanish alternatives, the output includes both in `answer.english` and `answer.spanish`. Rows with a single alternative use a numeric `answer` directly.

Canceled questions marked with text such as `Anulado` or `Anulada` are omitted from the output.

The script requires Poppler's `pdftotext` command to be installed.

## Tests

Run the test suite:

```bash
python3 -m unittest discover -s tests
```

The suite includes parser tests and a PDF compatibility matrix for every PDF fixture currently in `pdfs/`: day-1 answer keys from 2011 through 2024, plus a 2024 day-2 PDF with a canceled question.
