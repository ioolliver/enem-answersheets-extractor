import shutil
import unittest
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from enem_answersheet_extractor.cli import extract_text_from_pdf, parse_answers


ROOT = Path(__file__).resolve().parents[1]


COMPATIBILITY_CASES = {
    "2011_dia_1.pdf": {
        "count": 90,
        "range": (1, 90),
        "missing": [],
        "dual": [],
        "samples": {
            1: {"index": 1, "hasTwoAnswers": False, "answer": 4},
            46: {"index": 46, "hasTwoAnswers": False, "answer": 3},
            90: {"index": 90, "hasTwoAnswers": False, "answer": 0},
        },
    },
    "2012_dia_1.pdf": {
        "count": 90,
        "range": (1, 90),
        "missing": [],
        "dual": [],
        "samples": {
            1: {"index": 1, "hasTwoAnswers": False, "answer": 4},
            46: {"index": 46, "hasTwoAnswers": False, "answer": 1},
            90: {"index": 90, "hasTwoAnswers": False, "answer": 1},
        },
    },
    "2013_dia_1.pdf": {
        "count": 90,
        "range": (1, 90),
        "missing": [],
        "dual": [],
        "samples": {
            1: {"index": 1, "hasTwoAnswers": False, "answer": 4},
            46: {"index": 46, "hasTwoAnswers": False, "answer": 1},
            90: {"index": 90, "hasTwoAnswers": False, "answer": 0},
        },
    },
    "2014_dia_1.pdf": {
        "count": 90,
        "range": (1, 90),
        "missing": [],
        "dual": [],
        "samples": {
            1: {"index": 1, "hasTwoAnswers": False, "answer": 4},
            46: {"index": 46, "hasTwoAnswers": False, "answer": 0},
            90: {"index": 90, "hasTwoAnswers": False, "answer": 2},
        },
    },
    "2015_dia_1.pdf": {
        "count": 90,
        "range": (1, 90),
        "missing": [],
        "dual": [],
        "samples": {
            1: {"index": 1, "hasTwoAnswers": False, "answer": 0},
            46: {"index": 46, "hasTwoAnswers": False, "answer": 3},
            90: {"index": 90, "hasTwoAnswers": False, "answer": 0},
        },
    },
    "2016_dia_1.pdf": {
        "count": 90,
        "range": (1, 90),
        "missing": [],
        "dual": [],
        "samples": {
            1: {"index": 1, "hasTwoAnswers": False, "answer": 1},
            46: {"index": 46, "hasTwoAnswers": False, "answer": 1},
            90: {"index": 90, "hasTwoAnswers": False, "answer": 4},
        },
    },
    "2017_dia_1.pdf": {
        "count": 90,
        "range": (1, 90),
        "missing": [],
        "dual": [1, 2, 3, 4, 5],
        "samples": {
            1: {
                "index": 1,
                "hasTwoAnswers": True,
                "answer": {"english": 3, "spanish": 4},
            },
            46: {"index": 46, "hasTwoAnswers": False, "answer": 2},
            90: {"index": 90, "hasTwoAnswers": False, "answer": 4},
        },
    },
    "2018_dia_1.pdf": {
        "count": 90,
        "range": (1, 90),
        "missing": [],
        "dual": [1, 2, 3, 4, 5],
        "samples": {
            1: {
                "index": 1,
                "hasTwoAnswers": True,
                "answer": {"english": 1, "spanish": 1},
            },
            46: {"index": 46, "hasTwoAnswers": False, "answer": 2},
            90: {"index": 90, "hasTwoAnswers": False, "answer": 4},
        },
    },
    "2019_dia_1.pdf": {
        "count": 90,
        "range": (1, 90),
        "missing": [],
        "dual": [1, 2, 3, 4, 5],
        "samples": {
            1: {
                "index": 1,
                "hasTwoAnswers": True,
                "answer": {"english": 1, "spanish": 0},
            },
            46: {"index": 46, "hasTwoAnswers": False, "answer": 1},
            90: {"index": 90, "hasTwoAnswers": False, "answer": 1},
        },
    },
    "2020_dia_1.pdf": {
        "count": 90,
        "range": (1, 90),
        "missing": [],
        "dual": [1, 2, 3, 4, 5],
        "samples": {
            1: {
                "index": 1,
                "hasTwoAnswers": True,
                "answer": {"english": 0, "spanish": 0},
            },
            46: {"index": 46, "hasTwoAnswers": False, "answer": 3},
            90: {"index": 90, "hasTwoAnswers": False, "answer": 3},
        },
    },
    "2021_dia_1.pdf": {
        "count": 90,
        "range": (1, 90),
        "missing": [],
        "dual": [1, 2, 3, 4, 5],
        "samples": {
            1: {
                "index": 1,
                "hasTwoAnswers": True,
                "answer": {"english": 2, "spanish": 2},
            },
            46: {"index": 46, "hasTwoAnswers": False, "answer": 1},
            90: {"index": 90, "hasTwoAnswers": False, "answer": 1},
        },
    },
    "2022_dia_1.pdf": {
        "count": 90,
        "range": (1, 90),
        "missing": [],
        "dual": [1, 2, 3, 4, 5],
        "samples": {
            1: {
                "index": 1,
                "hasTwoAnswers": True,
                "answer": {"english": 3, "spanish": 4},
            },
            46: {"index": 46, "hasTwoAnswers": False, "answer": 3},
            90: {"index": 90, "hasTwoAnswers": False, "answer": 0},
        },
    },
    "2023_dia_1.pdf": {
        "count": 90,
        "range": (1, 90),
        "missing": [],
        "dual": [1, 2, 3, 4, 5],
        "samples": {
            1: {
                "index": 1,
                "hasTwoAnswers": True,
                "answer": {"english": 1, "spanish": 0},
            },
            46: {"index": 46, "hasTwoAnswers": False, "answer": 2},
            90: {"index": 90, "hasTwoAnswers": False, "answer": 1},
        },
    },
    "2024_dia_1.pdf": {
        "count": 90,
        "range": (1, 90),
        "missing": [],
        "dual": [1, 2, 3, 4, 5],
        "samples": {
            1: {
                "index": 1,
                "hasTwoAnswers": True,
                "answer": {"english": 2, "spanish": 2},
            },
            46: {"index": 46, "hasTwoAnswers": False, "answer": 2},
            90: {"index": 90, "hasTwoAnswers": False, "answer": 2},
        },
    },
    "2024_dia_2.pdf": {
        "count": 89,
        "range": (91, 180),
        "missing": [129],
        "dual": [],
        "samples": {
            91: {"index": 91, "hasTwoAnswers": False, "answer": 1},
            136: {"index": 136, "hasTwoAnswers": False, "answer": 0},
            180: {"index": 180, "hasTwoAnswers": False, "answer": 4},
        },
    },
}


class PdfCompatibilityTest(unittest.TestCase):
    def test_every_pdf_fixture_has_a_compatibility_case(self):
        pdf_filenames = {path.name for path in (ROOT / "pdfs").glob("*.pdf")}

        self.assertEqual(pdf_filenames, set(COMPATIBILITY_CASES))

    @unittest.skipUnless(shutil.which("pdftotext"), "pdftotext is required")
    def test_known_pdfs_extract_expected_answer_sets(self):
        for filename, expected in COMPATIBILITY_CASES.items():
            with self.subTest(filename=filename):
                answers = parse_answers(extract_text_from_pdf(ROOT / "pdfs" / filename))
                by_index = {answer["index"]: answer for answer in answers}
                indexes = sorted(by_index)
                expected_range = expected["range"]
                missing = [
                    index
                    for index in range(expected_range[0], expected_range[1] + 1)
                    if index not in by_index
                ]
                dual = [
                    answer["index"]
                    for answer in answers
                    if answer["hasTwoAnswers"]
                ]

                self.assertEqual(len(answers), expected["count"])
                self.assertEqual((indexes[0], indexes[-1]), expected_range)
                self.assertEqual(missing, expected["missing"])
                self.assertEqual(dual, expected["dual"])

                for index, expected_answer in expected["samples"].items():
                    self.assertEqual(by_index[index], expected_answer)


if __name__ == "__main__":
    unittest.main()
