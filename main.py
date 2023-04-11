import argparse
import re


def process_input_line(line):
    if line.startswith("*"):
        return line + "<br>"
    return line


def process_question_and_answer(question, answer):
    question = question.strip()
    answer = answer.strip()

    if question.endswith("?") and answer.endswith("?"):
        return f"{question};{answer};Reverse"
    elif re.search(r"{{c\d::", question):
        return f"{question};{answer};Cloze"
    else:
        return f"{question};{answer};Basic"


def convert_text_to_anki(input_text, deck_name):
    lines = input_text.splitlines()
    output_lines = [f"#notetype column:3", f"#deck:{deck_name}"]

    question = ""
    answer = ""
    for line in lines:
        stripped_line = line.strip()
        # If the line is empty, we're done with the current question and answer
        if not stripped_line:
            if question and answer:
                output_lines.append(process_question_and_answer(question, answer))
                question = ""
                answer = ""
            continue

        if not question:
            question = process_question(question, line)
        else:
            answer = process_answer(answer, line)

    # If we have a question and answer left over, add them to the output
    if question and answer:
        output_lines.append(process_question_and_answer(question, answer))

    return "\n".join(output_lines)


def process_question(question, line):
    if not question:
        return line.strip()
    return question


def process_answer(answer, line):
    return answer + process_input_line(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input text file with questions and answers")
    parser.add_argument("--deck", help="Name of the Anki deck", required=True)
    args = parser.parse_args()

    with open(args.input_file, "r") as f_input:
        input_text = f_input.read()

    output_text = convert_text_to_anki(input_text, args.deck)

    with open("anki.txt", "w") as f_output:
        f_output.write(output_text)


if __name__ == "__main__":
    main()
