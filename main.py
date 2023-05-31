import argparse
import re


def process_question_and_answer(question, answer=None, tag=""):
    question = question.strip()

    question = bold_replace(question)
    if answer:
        answer = bold_replace(answer)

    if question.endswith("?") and (answer is not None) and answer.strip().endswith("?"):
        return f"{question};{answer.strip()};Reverse;{tag}"
    elif is_cloze(question) or (answer and is_cloze(answer)):
        return f"{question}{('<br>'+answer) if answer else ''};;Cloze;{tag}"
    elif answer is not None:
        return f"{question};{answer.strip()};Basic;{tag}"

    raise ValueError("Invalid question and answer combination")


def is_cloze(line: str) -> bool:
    return bool(re.search(r"{{c\d::", line))


def bold_replace(s):
    return s.replace("**", "<b>", 1).replace("**", "</b>", 1)


def convert_text_to_anki(input_text):
    lines = input_text.splitlines()
    output_lines = ["#notetype column:3", "#tags column:4"]

    question, answer = "", None
    tag = ""
    for line in lines:
        stripped_line = line.strip()

        if stripped_line.lower().startswith("#tag:"):
            split_tag = stripped_line.split(":")
            if len(split_tag) == 1:
                tag = ''
            else:
                tag = split_tag[1]

        if not stripped_line or stripped_line.startswith("#"):
            if question and (answer is not None or is_cloze(question)):
                output_lines.append(process_question_and_answer(question, answer, tag))
                question, answer = "", None
            continue

        if not question:
            question = stripped_line
        elif not is_cloze(question):
            answer = answer + f"<br>{line}" if answer else line

    if question and (answer is not None or is_cloze(question)):
        output_lines.append(process_question_and_answer(question, answer, tag))

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
