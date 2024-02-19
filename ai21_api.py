import requests
from pprint import pprint
from copy import deepcopy
import logging

logger = logging.getLogger()


def ai21_check(iAPIKey, iText):
    try:
        url = "https://api.ai21.com/studio/v1/gec"

        headers = {"Authorization": f"Bearer {iAPIKey}"}
        payload = {"text": iText}
        logger.info(f"Request Payload: {payload}")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        json_data = response.json()
        logger.info(f"Response: {json_data}")

        text = deepcopy(iText)
        for edit in reversed(json_data["corrections"]):
            start = edit["startIndex"]
            end = edit["endIndex"]
            text = (
                text[:start]
                + "<span style='background-color: #FFFF00'>"
                + edit["suggestion"]
                + "</span>"
                + text[end:]
            )

        logger.info(f"Highligted Text: {text}")
        return text

    except requests.exceptions.HTTPError as e:
        logger.exception(str(e.response.content))
        return f"Error: {str(e.response.content)}"

    except Exception as e:
        logger.exception(e)
        return f"Error: {e}"


if __name__ == "__main__":
    text = "It is is more fun to talk with someone who doesnt use long, difikolt words but rather short, easy words like, What about lunch"
    ai21_check("czlGQtDK9UJ8Gcxv3jMTyPyGCN7DQDUn", text)
