import re
import json
from typing import Union

def extract_text_from_response(content: Union[str, list]) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            [part if isinstance(part, str) else part.get("text", "") for part in content]
        )
    return str(content)

def safe_json_load(text):
    text = re.sub(r"```json|```", "", text).strip()

    try:
        return json.loads(text)
    except:
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            raise ValueError("LLM did not return valid JSON.")
