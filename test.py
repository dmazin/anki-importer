import unittest
from main import process_input_line, process_question_and_answer, convert_text_to_anki


class TestAnkiConversion(unittest.TestCase):
    def test_process_input_line(self):
        self.assertEqual(process_input_line("* test line"), "* test line<br>")
        self.assertEqual(process_input_line("normal line"), "normal line")

    def test_process_question_and_answer(self):
        self.assertEqual(process_question_and_answer("What is Python?", "A programming language?"),
                         "What is Python?;A programming language?;Reverse")
        self.assertEqual(process_question_and_answer("{{c1::Python}} is a programming language."),
                         "{{c1::Python}} is a programming language.;;Cloze")
        self.assertEqual(process_question_and_answer("What is Python?", "A programming language."),
                         "What is Python?;A programming language.;Basic")

    def test_convert_text_to_anki(self):
        input_text = "What is Python?\nA programming language?\n\n{{c1::Python}} is a programming language."
        deck_name = "Test Deck"
        expected_output = "#notetype column:3\n#deck:Test Deck\nWhat is Python?;A programming language?;Reverse\n" \
                          "{{c1::Python}} is a programming language.;;Cloze"
        self.assertEqual(convert_text_to_anki(input_text, deck_name), expected_output)

if __name__ == '__main__':
    unittest.main()
