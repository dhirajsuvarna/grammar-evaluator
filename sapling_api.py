import requests
import logging
from copy import deepcopy
import tomllib

logger = logging.getLogger()


def sapling_check(iAPIKey, iText):

    try:
        payload = {
            "key": iAPIKey,
            "text": iText,
            "auto_apply": True,
            "neural_spellcheck": True,
            "session_id": "test session",
        }

        logger.info(f"Request payload: {payload}")
        response = requests.post("https://api.sapling.ai/api/v1/edits", json=payload)
        response.raise_for_status()

        resp_json = response.json()
        logger.info(f"Response: {resp_json}")

        text = deepcopy(iText)
        edits = resp_json["edits"]
        edits = sorted(
            resp_json["edits"],
            key=lambda e: (e["sentence_start"] + e["start"]),
            reverse=True,
        )

        for edit in edits:
            start = edit["sentence_start"] + edit["start"]
            end = edit["sentence_start"] + edit["end"]
            if start > len(text) or end > len(text):
                print(f"Edit start:{start}/end:{end} outside of bounds of text:{text}")
                continue
            text = (
                text[:start]
                + "<span style='background-color: #FFFF00'>"
                + edit["replacement"]
                + "</span>"
                + text[end:]
            )

        logger.info(f"Highligted Text: {text}")
        # with open("corrected_text.txt", "a", encoding="utf-8") as oTextFile:
        #     oTextFile.write(test_text)
        return text

    except requests.exceptions.HTTPError as e:
        logger.exception(str(e.response.content))
        return f"Error: {str(e.response.content)}"

    except Exception as e:
        logger.exception(e)
        return f"Error: {e}"


if __name__ == "__main__":
    with open(
        r"F:\projects\freelancing\grammar-stuff\grammar_checker\.streamlit\secrets.toml",
        "rb",
    ) as f:
        secrets = tomllib.load(f)

    iText = "It is is more fun to talk with someone who doesnt use long, difikolt words but rather short, easy words like, What about lunch"
    sapling_check(secrets["SAPLING_API_KEY"], iText)
