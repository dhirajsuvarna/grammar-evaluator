import json
import prompts
import logging

from openai import OpenAI
from pprint import pprint
from diff import find_diff
from copy import deepcopy

OPENAI_MODEL_NAME = "gpt-3.5-turbo-0125"

logger = logging.getLogger()


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


def openai_check(iAPIKey, iText):
    try:
        client = OpenAI()
        client.api_key = iAPIKey

        payload = [
            {"role": "system", "content": prompts.system_message},
            {"role": "user", "content": iText},
        ]

        logger.info(f"Request Payload: {payload}")
        response = client.chat.completions.create(
            model=OPENAI_MODEL_NAME,
            response_format={"type": "json_object"},
            messages=payload,
        )
        logger.info(f"Response: {response}")
        response_text = response.choices[0].message.content
        json_obj = json.loads(response_text)

        # get correct text -
        correct_stmt = json_obj.get("correct_stmt")
        # correct_stmt = "It is more fun to talk with someone who doesn't use long, difficult words but rather short, easy words like, 'What about lunch?'"
        differences = find_diff(iText, correct_stmt)
        pprint(differences)
        text = deepcopy(iText)
        for edit in reversed(differences):
            text = (
                text[: edit["startIndex"]]
                + "<span style='background-color: #FFFF00'>"
                + edit["suggestion"]
                + "</span>"
                + text[edit["endIndex"] :]
            )
        print(f"Highlighted Text: {text}")
        return text
        # calculate the cost
        # cost = openai_api_calculate_cost(dict(response.usage), OPENAI_MODEL_NAME)
    except Exception as e:
        logger.exception(e)
        error_str = f"Error: {e}"
        return error_str

    # return text
