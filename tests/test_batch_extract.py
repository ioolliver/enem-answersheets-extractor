import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from enem_answersheet_extractor.cli import extract_answer_sheets_from_folder, main


class BatchExtractTest(unittest.TestCase):
    def test_extract_answer_sheets_from_folder_adds_year_and_day_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdfs_dir = Path(tmp)
            (pdfs_dir / "2025_dia_2.pdf").touch()
            (pdfs_dir / "2024_dia_1.pdf").touch()

            text_by_filename = {
                "2024_dia_1.pdf": "1 A\n2 B",
                "2025_dia_2.pdf": "91 C\n92 D",
            }

            with patch(
                "enem_answersheet_extractor.cli.extract_text_from_pdf",
                side_effect=lambda path: text_by_filename[path.name],
            ):
                payload = extract_answer_sheets_from_folder(pdfs_dir)

        self.assertEqual(
            payload,
            [
                {
                    "year": 2024,
                    "day": 1,
                    "application": "normal",
                    "sheet": [
                        {"index": 1, "hasTwoAnswers": False, "answer": 0},
                        {"index": 2, "hasTwoAnswers": False, "answer": 1},
                    ],
                },
                {
                    "year": 2025,
                    "day": 2,
                    "application": "normal",
                    "sheet": [
                        {"index": 91, "hasTwoAnswers": False, "answer": 2},
                        {"index": 92, "hasTwoAnswers": False, "answer": 3},
                    ],
                },
            ],
        )

    def test_extract_answer_sheets_from_folder_adds_application_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdfs_dir = Path(tmp)
            (pdfs_dir / "2024_dia_1.pdf").touch()
            (pdfs_dir / "2024_dia_1_ppl.pdf").touch()
            (pdfs_dir / "2024_dia_1_digital.pdf").touch()
            (pdfs_dir / "2024_dia_1_terceira.pdf").touch()

            with patch(
                "enem_answersheet_extractor.cli.extract_text_from_pdf",
                return_value="1 A",
            ):
                payload = extract_answer_sheets_from_folder(pdfs_dir)

        self.assertEqual(
            [
                item["application"]
                for item in sorted(payload, key=lambda item: item["application"])
            ],
            ["digital", "normal", "ppl", "terceira"],
        )

    def test_main_outputs_folder_payload_as_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdfs_dir = Path(tmp)
            (pdfs_dir / "2024_dia_1.pdf").touch()

            stdout = io.StringIO()
            with (
                patch(
                    "enem_answersheet_extractor.cli.extract_text_from_pdf",
                    return_value="1 A",
                ),
                contextlib.redirect_stdout(stdout),
            ):
                exit_code = main([str(pdfs_dir)])

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            json.loads(stdout.getvalue()),
            [
                {
                    "year": 2024,
                    "day": 1,
                    "application": "normal",
                    "sheet": [{"index": 1, "hasTwoAnswers": False, "answer": 0}],
                }
            ],
        )

    def test_main_can_filter_folder_payload_by_application(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdfs_dir = Path(tmp)
            (pdfs_dir / "2024_dia_1.pdf").touch()
            (pdfs_dir / "2024_dia_1_ppl.pdf").touch()
            (pdfs_dir / "2024_dia_1_digital.pdf").touch()
            extracted_filenames = []

            def extract_text(pdf_path):
                extracted_filenames.append(pdf_path.name)
                return "1 A"

            stdout = io.StringIO()
            with (
                patch(
                    "enem_answersheet_extractor.cli.extract_text_from_pdf",
                    side_effect=extract_text,
                ),
                contextlib.redirect_stdout(stdout),
            ):
                exit_code = main([str(pdfs_dir), "--application-only", "ppl"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(extracted_filenames, ["2024_dia_1_ppl.pdf"])
        self.assertEqual(
            json.loads(stdout.getvalue()),
            [
                {
                    "year": 2024,
                    "day": 1,
                    "application": "ppl",
                    "sheet": [{"index": 1, "hasTwoAnswers": False, "answer": 0}],
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
