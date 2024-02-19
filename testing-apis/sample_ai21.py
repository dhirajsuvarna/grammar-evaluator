response = {
    "corrections": [
        {
            "correctionType": "Word Repetition",
            "endIndex": 8,
            "originalText": "It is is",
            "startIndex": 0,
            "suggestion": "It is",
        },
        {
            "correctionType": "Grammar",
            "endIndex": 49,
            "originalText": "doesnt",
            "startIndex": 43,
            "suggestion": "doesn't",
        },
        {
            "correctionType": "Spelling",
            "endIndex": 68,
            "originalText": "difikolt",
            "startIndex": 60,
            "suggestion": "difficult",
        },
        {
            "correctionType": "Punctuation",
            "endIndex": 126,
            "originalText": "lunch",
            "startIndex": 121,
            "suggestion": "lunch?",
        },
    ],
    "id": "929d12a5-827f-a047-9d30-714fa80efb48",
}

text = "It is is more fun to talk with someone who doesnt use long, difikolt words but rather short, easy words like, What about lunch"

for edit in reversed(response["corrections"]):
    start = edit["startIndex"]
    end = edit["endIndex"]
    text = text[:start] + edit["suggestion"] + text[end:]

print(text)
