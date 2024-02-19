import json
from pprint import pprint

json_str = """{"id": "gen-StgayS9RBs4cALaXe6Vy4I4xgVVq", "model": "mistralai/mistral-7b-instruct:free", "created": 1708318636, "object": "chat.completion", "choices": [{"message": {"role": "assistant", "content": "Output:\n{\n    "correct\\_stmt": "It is more fun to talk with someone who doesn\'t use 
long, difficult words but rather short, easy words like, \"What about lunch?\""\n}"}}], "usage": {"prompt_tokens": 178, "completion_tokens": 48, "total_tokens": 226}}
"""

json_data = json.loads(json_str)
print(json_data)
