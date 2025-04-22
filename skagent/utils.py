import re

def extract_json_from_string(raw_output: str) -> str:
    try:
        start = raw_output.index('{')
        end = raw_output.rindex('}') + 1
        return raw_output[start:end]
    except ValueError:
        raise ValueError("Valid JSON block not found in the input string.")
