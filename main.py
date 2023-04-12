import argparse
import re


def process_input_line(line):
    return line + "<br>" if line.startswith("*") else line


def process_question_and_answer(question, answer=None):
    question = question.strip()

    if question.endswith("?") and (answer is not None) and answer.strip().endswith("?"):
        return f"{question};{answer.strip()};Reverse"
    elif re.search(r"{{c\d::", question) or (answer and re.search(r"{{c\d::", answer)):
        return f"{question};{answer if answer else ''};Cloze"
    elif answer is not None:
        return f"{question};{answer.strip()};Basic"

    raise ValueError("Invalid question and answer combination")


def convert_text_to_anki(input_text):
    lines = input_text.splitlines()
    output_lines = [f"#notetype column:3"]

    question, answer = "", None
    for line in lines:
        stripped_line = line.strip()

        if not stripped_line:
            if question and (answer is not None or re.search(r"{{c\d::", question)):
                output_lines.append(process_question_and_answer(question, answer))
                question, answer = "", None
            continue

        if not question:
            question = stripped_line
        elif not re.search(r"{{c\d::", question):
            answer = answer + process_input_line(line) if answer else process_input_line(line)

    if question and (answer is not None or re.search(r"{{c\d::", question)):
        output_lines.append(process_question_and_answer(question, answer))

    return "\n".join(output_lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input text file with questions and answers")
    args = parser.parse_args()

    with open(args.input_file, "r") as f_input:
        input_text = f_input.read()

    output_text = convert_text_to_anki(input_text)

    with open("anki.txt", "w") as f_output:
        f_output.write(output_text)


if __name__ == "__main__":
    main()
