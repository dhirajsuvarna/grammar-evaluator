import json
import prompts
import requests
import logging
import tomllib

from copy import deepcopy
from pprint import pprint, pformat
from diff import find_diff


logger = logging.getLogger()
OS_MODEL_NAME = "mistralai/mistral-7b-instruct:free"


def openai_api_calculate_cost(usage, model):
    pricing = {
        "gpt-3.5-turbo-0125": {
            "prompt": 0.0005,
            "completion": 0.0015,
        },
        # "gpt-4-1106-preview": {
        #     "prompt": 0.01,
        #     "completion": 0.03,
        # },
        # "gpt-4": {
        #     "prompt": 0.03,
        #     "completion": 0.06,
        # },
    }

    try:
        model_pricing = pricing[model]
    except KeyError:
        raise ValueError("Invalid model specified")

    prompt_cost = usage["prompt_tokens"] * model_pricing["prompt"] / 1000
    completion_cost = usage["completion_tokens"] * model_pricing["completion"] / 1000

    total_cost = prompt_cost + completion_cost
    # round to 6 decimals
    total_cost = round(total_cost, 6)

    print(
        f"\nTokens used:  {usage.prompt_tokens:,} prompt + {usage.completion_tokens:,} completion = {usage.total_tokens:,} tokens"
    )
    print(f"Total cost for {model}: ${total_cost:.4f}\n")

    return total_cost


def opensourcellm_check(iAPIKey, iText):
    try:
        payload = {
            "model": OS_MODEL_NAME,
            "messages": [
                {"role": "system", "content": prompts.system_message},
                {"role": "user", "content": iText},
            ],
            "temperature": 0.1,
        }

        logger.info(f"Request Payload: {payload}")
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {iAPIKey}",
                "HTTP-Referer": f"https://www.peach.com",
                "X-Title": f"peach",
            },
            json=payload,
        )
        response.raise_for_status()
        json_data = response.json()
        logger.info(f"Response: {json_data}")

        response_text = json_data["choices"][0]["message"]["content"]
        json_obj = json.loads(response_text)

        # get correct text -
        correct_stmt = json_obj.get("correct_stmt")
        # correct_stmt = "It is more fun to talk with someone who doesn't use long, difficult words but rather short, easy words like, 'What about lunch?'"
        differences = find_diff(iText, correct_stmt)
        text = deepcopy(iText)
        for edit in reversed(differences):
            text = (
                text[: edit["startIndex"]]
                + "<span style='background-color: #FFFF00'>"
                + edit["suggestion"]
                + "</span>"
                + text[edit["endIndex"] :]
            )
        logger.info(f"Highlighted Text: {text}")
        return text
        # calculate the cost
        # cost = openai_api_calculate_cost(dict(response.usage), OPENAI_MODEL_NAME)
    except requests.exceptions.HTTPError as e:
        logger.exception(str(e.response.content))
        return f"Error: {str(e.response.content)}"
    except Exception as e:
        logger.exception(e)
        error_str = f"Error: {e}"
        return error_str


if __name__ == "__main__":

    with open(
        r"F:\projects\freelancing\grammar-stuff\grammar_checker\.streamlit\secrets.toml",
        "rb",
    ) as f:
        secrets = tomllib.load(f)

    iText = """" Cycling is the most favorite activity. I love to do it in my free time. I cycle a lot. The next thing I love is music. I love to listen all kinds of music from a kinetic classical to western. And nowadays I have started reading most recently. I haven't read much but I love reading."\n"""
    opensourcellm_check(secrets["OPENROUTER_API_KEY"], iText)
