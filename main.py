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
        return f"{question};{answer};Reverse;{tag}"
    elif is_cloze(question) or (answer and is_cloze(answer)):
        return f"{question}{('<br>'+answer) if answer else ''};;Cloze;{tag}"
    elif answer is not None:
        return f"{question};{answer};Basic;{tag}"

    raise ValueError("Invalid question and answer combination")


def is_cloze(line: str) -> bool:
    return bool(re.search(r"{{c\d::", line))


def bold_replace(s):
    return s.replace("**", "<b>", 1).replace("**", "</b>", 1)

def lt_gt_escape(s: str) -> str:
    # Replace '<' not preceded by '&lt;'
    s = re.sub(r'(?<!&lt;)<', '&lt;', s)

    # Replace '>' not preceded by '&gt;'
    s = re.sub(r'(?<!&gt;)>', '&gt;', s)
    
    return s

def convert_text_to_anki(input_text):
    """
    This will be a reverse note where the front is the first line, and the back
    is the second line.
    What is a synonym for positive predictive value?
    What is a synonym for precision?

    This will be a cloze note where all the lines will be the main field.
    What are the DNS records used to prevent email sender field spoofing?
    * {{c1::SPF}}
    * {{c2::DKIM}}
    * {{c3::DMARC}}

    This will be a basic note where the front is the first line, and the back is
    the second line.
    In terms of networking, what does ASN stand for?
    Autonomous system number.

    * Each note is separated by a whitespace or a line starting with '#'.
    * \n's are turned into <br>
    * words **surrounded** like so will get wrapped in <b> tags
    * it's possible for the front card to have multiple lines, but not the back
      card
    """
    lines = input_text.splitlines()
    output_lines = ["#notetype column:3", "#tags column:4"]

    question, answer = "", None
    tag = ""
    for line in lines:
        stripped_line = line.strip()

        # process tag
        if stripped_line.lower().startswith("#tag:"):
            split_tag = stripped_line.split(":")
            if len(split_tag) == 1:
                tag = ""
            else:
                tag = split_tag[1]

        # "close out" the note if we reach whitespace
        if not stripped_line or stripped_line.startswith("#"):
            # the reason for `is_cloze(question)` is because we can have
            # single-line cloze notes
            if question and (answer is not None or is_cloze(question)):
                output_lines.append(process_question_and_answer(question, answer, tag))
                question, answer = "", None
            continue

        if not question:
            question = stripped_line
        else:
            # It's possible for answers to span multiple lines
            answer = (answer + "\n" + line) if answer else line

    # handle the very last line (we need to do this because we "close out" a
    # note if we reach a whitespace line, which will not happen for the very end
    # of the file)
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
