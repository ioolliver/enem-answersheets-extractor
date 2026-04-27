import unittest
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from enem_answersheet_extractor.cli import parse_answers


SAMPLE_TEXT = """
QUESTÃO
             INGLÊS       ESPANHOL
   1           D              B         46            E
   2           D              A         47            D
   3           D              D         48            E
   4           E              D         49            C
   5           A              C         50            A
  6                   E                 51            D
  45                  C                 90            A
"""


class ParseAnswersTest(unittest.TestCase):
    def test_parse_answers_includes_both_language_answers_when_present(self):
        answers = parse_answers(SAMPLE_TEXT)

        self.assertEqual(
            answers[:6],
            [
                {
                    "index": 1,
                    "hasTwoAnswers": True,
                    "answer": {"english": 3, "spanish": 1},
                },
                {
                    "index": 2,
                    "hasTwoAnswers": True,
                    "answer": {"english": 3, "spanish": 0},
                },
                {
                    "index": 3,
                    "hasTwoAnswers": True,
                    "answer": {"english": 3, "spanish": 3},
                },
                {
                    "index": 4,
                    "hasTwoAnswers": True,
                    "answer": {"english": 4, "spanish": 3},
                },
                {
                    "index": 5,
                    "hasTwoAnswers": True,
                    "answer": {"english": 0, "spanish": 2},
                },
                {"index": 6, "hasTwoAnswers": False, "answer": 4},
            ],
        )
        self.assertEqual(
            answers[-1],
            {"index": 90, "hasTwoAnswers": False, "answer": 0},
        )

    def test_two_answer_detection_is_independent_of_question_index(self):
        answers = parse_answers("91           A              C")

        self.assertEqual(
            answers,
            [
                {
                    "index": 91,
                    "hasTwoAnswers": True,
                    "answer": {"english": 0, "spanish": 2},
                }
            ],
        )

    def test_canceled_questions_are_ignored(self):
        answers = parse_answers("129      Anulado      174          C")

        self.assertEqual(
            answers,
            [{"index": 174, "hasTwoAnswers": False, "answer": 2}],
        )


if __name__ == "__main__":
    unittest.main()
