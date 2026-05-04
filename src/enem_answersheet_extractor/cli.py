from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


LETTER_TO_INDEX = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
APPLICATIONS = ("normal", "ppl", "digital", "terceira")
PDF_FILENAME_RE = re.compile(
    r"^(?P<year>\d{4})_dia_(?P<day>\d+)(?:_(?P<application>ppl|digital|terceira))?\.pdf$",
    re.IGNORECASE,
)


def extract_text_from_pdf(pdf_path: Path) -> str:
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if shutil.which("pdftotext") is None:
        raise RuntimeError(
            "pdftotext was not found. Install Poppler tools and try again."
        )

    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def parse_answers(text: str) -> list[dict]:
    answers: dict[int, list[str]] = {}

    for line in text.splitlines():
        line_answers = _parse_answer_line(line)
        answers.update(line_answers)

    return [
        _format_answer(index, answers[index])
        for index in sorted(answers)
    ]


def extract_answer_sheets_from_folder(
    pdfs_dir: Path,
    application_only: str | None = None,
) -> list[dict]:
    if not pdfs_dir.exists():
        raise FileNotFoundError(f"Folder not found: {pdfs_dir}")

    if not pdfs_dir.is_dir():
        raise NotADirectoryError(f"Not a folder: {pdfs_dir}")

    payload = []
    for pdf_path in sorted(pdfs_dir.glob("*.pdf"), key=_pdf_sort_key):
        year, day, application = _parse_pdf_filename(pdf_path)
        if application_only is not None and application != application_only:
            continue

        payload.append(
            {
                "year": year,
                "day": day,
                "application": application,
                "sheet": parse_answers(extract_text_from_pdf(pdf_path)),
            }
        )

    return payload


def _parse_pdf_filename(pdf_path: Path) -> tuple[int, int, str]:
    match = PDF_FILENAME_RE.match(pdf_path.name)
    if match is None:
        raise ValueError(
            "PDF filename must follow YEAR_dia_DAY[_APPLICATION].pdf "
            f"where APPLICATION is ppl, digital, or terceira: {pdf_path.name}"
        )

    application = (match["application"] or "normal").lower()
    return int(match["year"]), int(match["day"]), application


def _pdf_sort_key(pdf_path: Path) -> tuple[int, int, str]:
    return _parse_pdf_filename(pdf_path)


def _parse_answer_line(line: str) -> dict[int, list[str]]:
    tokens = re.findall(r"\d+|[A-ZÀ-Ü]+", line.upper())
    parsed: dict[int, list[str]] = {}
    cursor = 0

    while cursor < len(tokens):
        if not tokens[cursor].isdigit():
            cursor += 1
            continue

        question = int(tokens[cursor])
        cursor += 1

        letters: list[str] = []
        while cursor < len(tokens) and not tokens[cursor].isdigit():
            if tokens[cursor] in LETTER_TO_INDEX:
                letters.append(tokens[cursor])
            cursor += 1

        if letters:
            parsed[question] = letters

    return parsed


def _format_answer(index: int, letters: list[str]) -> dict:
    if len(letters) >= 2:
        return {
            "index": index,
            "hasTwoAnswers": True,
            "answer": {
                "english": LETTER_TO_INDEX[letters[0]],
                "spanish": LETTER_TO_INDEX[letters[1]],
            },
        }

    return {
        "index": index,
        "hasTwoAnswers": False,
        "answer": LETTER_TO_INDEX[letters[0]],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract ENEM PDF answers into JSON."
    )
    parser.add_argument(
        "source",
        type=Path,
        help="Path to an ENEM PDF or a folder of YEAR_dia_DAY.pdf files.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write JSON to this file instead of stdout.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON with indentation.",
    )
    parser.add_argument(
        "--application-only",
        choices=APPLICATIONS,
        help="When source is a folder, extract only this application type.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.source.is_dir():
            payload_data = extract_answer_sheets_from_folder(
                args.source,
                application_only=args.application_only,
            )
        else:
            payload_data = parse_answers(extract_text_from_pdf(args.source))
    except Exception as error:
        parser.exit(1, f"error: {error}\n")

    payload = json.dumps(
        payload_data,
        ensure_ascii=False,
        indent=2 if args.pretty else None,
    )

    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
