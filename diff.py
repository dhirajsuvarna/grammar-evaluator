from difflib import SequenceMatcher
from pprint import pprint


def find_diff(a, b):
    # Split the sentences into words
    words_a = a.split()
    words_b = b.split()

    # Initialize the SequenceMatcher with the word lists
    s = SequenceMatcher(None, words_a, words_b)

    differences = []
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == "replace":
            start_a = len(" ".join(words_a[:i1])) + (i1 > 0)
            end_a = len(" ".join(words_a[:i2]))
            start_b = len(" ".join(words_b[:j1])) + (j1 > 0)
            end_b = len(" ".join(words_b[:j2]))
            differences.append(
                {
                    "type": "replace",
                    "original_text": " ".join(words_a[i1:i2]),
                    "suggestion": " ".join(words_b[j1:j2]),
                    "startIndex": start_a,
                    "endIndex": end_a,
                }
            )
        elif tag == "delete":
            start_a = len(" ".join(words_a[:i1])) + (i1 > 0)
            end_a = len(" ".join(words_a[:i2])) + (i2 > 0)
            differences.append(
                {
                    "type": "delete",
                    "original_text": " ".join(words_a[i1:i2]),
                    "suggestion": "",
                    "startIndex": start_a,
                    "endIndex": end_a,
                }
            )
            # differences.append(
            #     (f"Delete '{' '.join(words_a[i1:i2])}'", start_a, end_a, None, None)
            # )
        elif tag == "insert":
            start_a = len(" ".join(words_a[:i1])) + (i1 > 0)
            end_a = len(" ".join(words_a[:j2]))
            differences.append(
                {
                    "type": "insert",
                    "original_text": "",
                    "suggestion": " ".join(words_b[j1:j2]),
                    "startIndex": start_a,
                    "endIndex": end_a,
                }
            )
            # differences.append(
            #     (f"Insert '{' '.join(words_b[j1:j2])}'", None, None, start_b, end_b)
            # )

    return differences


if __name__ == "__main__":
    # Use the function with the example sentences
    input_text = "It is is more fun to talk with someone who doesnt use long, difikolt words but rather short, easy words like, What about lunch"
    # correct_text = "It is more fun to talk with someone who doesn't use long, difficult words but rather short, easy words like, 'What about lunch?'"
    correct_text = "It's more fun to talk with someone who doesn't use long, difficult words but rather short, easy words like, 'What about lunch?'"
    word_differences_with_positions = find_diff(input_text, correct_text)
    pprint(word_differences_with_positions)
