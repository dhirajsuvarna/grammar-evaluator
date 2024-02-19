import requests
import json
from pprint import pprint

OPENROUTER_API_KEY = (
    "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"
)

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": f"https://www.peach.com",
        "X-Title": f"peach",
    },
    data=json.dumps(
        {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [{"role": "user", "content": "What is the meaning of life"}],
        }
    ),
)

pprint(response.json())
