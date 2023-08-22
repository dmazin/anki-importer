import argparse
import re


def process_question_and_answer(question, answer=None, tag=""):
    question = question.strip()
    question = lt_gt_escape(question)
    question = bold_replace(question)

    if answer:
        answer = bold_replace(answer)
        answer = lt_gt_escape(answer)
        answer = answer.strip().replace("\n", "<br>")

    if question.endswith("?") and (answer is not None) and answer.endswith("?"):
        return f'{quote_wrap(question)};{quote_wrap(answer)};{quote_wrap("Reverse")};{quote_wrap(tag)}'
    elif is_cloze(question) or (answer and is_cloze(answer)):
        return f'{quote_wrap(question + ("<br>" + answer if answer else ""))};;{quote_wrap("Cloze")};{quote_wrap(tag)}'
    elif answer is not None:
        return f'{quote_wrap(question)};{quote_wrap(answer)};{quote_wrap("Basic")};{quote_wrap(tag)}'

    raise ValueError("Invalid question and answer combination")


def is_cloze(line: str) -> bool:
    return bool(re.search(r"{{c\d::", line))


def bold_replace(s):
    return s.replace("**", "<b>", 1).replace("**", "</b>", 1)


def lt_gt_escape(s: str) -> str:
    s = re.sub(r'(?<!&lt;)<', '&lt;', s)
    s = re.sub(r'(?<!&gt;)>', '&gt;', s)
    return s


def quote_wrap(field):
    escaped_field = field.replace('"', '""')
    return f"\"{escaped_field}\""


def convert_text_to_anki(input_text):
    lines = input_text.splitlines()
    output_lines = ["#notetype column:3", "#tags column:4"]

    question, answer = "", None
    tag = ""
    for line in lines:
        stripped_line = line.strip()

        if stripped_line.lower().startswith("#tag:"):
            split_tag = stripped_line.split(":")
            tag = split_tag[1] if len(split_tag) > 1 else ""

        if not stripped_line or stripped_line.startswith("#"):
            if question and (answer is not None or is_cloze(question)):
                output_lines.append(process_question_and_answer(question, answer, tag))
                question, answer = "", None
            continue

        if not question:
            question = stripped_line
        else:
            answer = (answer + "\n" + line) if answer else line

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
