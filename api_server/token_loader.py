import json
import os


def is_token_valid(token: str):
    current_path = os.path.dirname(__file__)
    print(current_path)
    with open(r'api_tokens.json', 'r') as tokens:
        token_arr = json.load(tokens)
        for t in token_arr:
            if t['token'] == token:
                return True
        return False
