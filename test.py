import unittest
from main import (
    process_question_and_answer,
    convert_text_to_anki,
    is_cloze,
)


class TestAnkiConversion(unittest.TestCase):
    def test_process_question_and_answer_reverse(self):
        self.assertEqual(
            process_question_and_answer(
                "What is Python?",
                "What is the Ruby-like programming language starting with a p?",
            ),
            "What is Python?;What is the Ruby-like programming language starting with a p?;Reverse;",
        )

    def test_process_question_and_answer_cloze(self):
        self.assertEqual(
            process_question_and_answer("{{c1::Python}} is a programming language."),
            "{{c1::Python}} is a programming language.;;Cloze;",
        )

    def test_process_question_and_answer_basic(self):
        self.assertEqual(
            process_question_and_answer("What is Python?", "A programming language."),
            "What is Python?;A programming language.;Basic;",
        )

    def test_convert_text_to_anki(self):
        input_text = "# This is a comment\nWhat is Python?\nWhat is the Ruby-like programming language starting with a p?\n\n{{c1::Python}} is a programming language."
        expected_output = (
            "#notetype column:3\n#tags column:4\nWhat is Python?;What is the Ruby-like programming language starting with a p?;Reverse;\n"
            "{{c1::Python}} is a programming language.;;Cloze;"
        )
        self.assertEqual(convert_text_to_anki(input_text), expected_output)

    def test_convert_text_to_anki_empty_lines_and_comments(self):
        input_text = "# This is a comment\nWhat is Python?\nWhat is the Ruby-like programming language starting with a p?\n\n{{c1::Python}} is a programming language."
        expected_output = (
            "#notetype column:3\n#tags column:4\nWhat is Python?;What is the Ruby-like programming language starting with a p?;Reverse;\n"
            "{{c1::Python}} is a programming language.;;Cloze;"
        )
        self.assertEqual(convert_text_to_anki(input_text), expected_output)

    def test_multiline_basic(self):
        input_question = "Roughly into what two layers can we split up the block layer?\n* bio layer\n* request layer"
        expected_output = "#notetype column:3\n#tags column:4\nRoughly into what two layers can we split up the block layer?;* bio layer<br>* request layer;Basic;"
        self.assertEqual(convert_text_to_anki(input_question), expected_output)

    def test_multi_item_cloze(self):
        input_question = "Roughly into what two layers can we split up the block layer?\n* {{c1::bio layer}}\n* {{c2::request layer}}"
        expected_output = "#notetype column:3\n#tags column:4\nRoughly into what two layers can we split up the block layer?<br>* {{c1::bio layer}}<br>* {{c2::request layer}};;Cloze;"
        self.assertEqual(convert_text_to_anki(input_question), expected_output)

    def test_multiline_cloze(self):
        input_question = "echo 1 to 10 using a bash for loop\n{{c1::for i in $(seq 1 10)}}\n{{c2::do echo $i}}\n{{c3::done}}"
        expected_output = "#notetype column:3\n#tags column:4\necho 1 to 10 using a bash for loop<br>{{c1::for i in $(seq 1 10)}}<br>{{c2::do echo $i}}<br>{{c3::done}};;Cloze;"
        self.assertEqual(convert_text_to_anki(input_question), expected_output)

    def test_multiple_tags(self):
        input_text = "What is the meaning of life?\n42.\n\n#TAG:Linux\nWhat is Linux?\nAn OSS kernel.\n\n#TAG:Python\nWhat is Python?\nA programming language."
        expected_output = "#notetype column:3\n#tags column:4\nWhat is the meaning of life?;42.;Basic;\nWhat is Linux?;An OSS kernel.;Basic;Linux\nWhat is Python?;A programming language.;Basic;Python"
        self.assertEqual(convert_text_to_anki(input_text), expected_output)

    def test_text_is_bolded(self):
        # if an input word is **surrounded by double asterisks**, it should be bolded (<b>)
        input_text = "What is **Python**?\nA programming language."
        expected_output = "#notetype column:3\n#tags column:4\nWhat is <b>Python</b>?;A programming language.;Basic;"
        self.assertEqual(convert_text_to_anki(input_text), expected_output)

    def test_is_cloze(self):
        self.assertTrue(is_cloze("{{c1::bio layer}}"))
        self.assertFalse(is_cloze("bio layer"))


if __name__ == "__main__":
    unittest.main()
