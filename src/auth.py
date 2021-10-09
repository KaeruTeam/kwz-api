"""
This file contains functions relating to authentication for the API.
"""

keys_file = ""


# Read API keys from the text file
def load_api_keys(keys_path=keys_file):
    global keys_file
    keys_file = keys_path

    keys = []

    with open(keys_file, "r", encoding="utf-8") as file:
        for key in file.readlines():
            keys.append(key.strip())

    return keys


# Verifies that the API key is in the list
def verify_api_key(input_key, keys):
    if input_key in keys:
        return True
    else:
        # Reload API keys list then check if the key is in the list again
        load_api_keys()
        return input_key in keys
