from os import path
from secrets import token_hex

keys = []

# Assuming this file is in src/ and the api key file is in ../api.key.txt
key_file_dir = path.join("../api_key.txt")


# Writes the given key to the key file
def WriteKey(key):
    with open(key_file_dir, "a") as file:
        file.write(str(key) + "\n")


# Read API keys from the text file
def LoadKeys():
    global keys
    keys = open(key_file_dir, "r").readlines()


# Verifies that the API key is in the list
def VerifyAPIKey(input_key):
    # Adding the newline so that `input_key in keys` works
    input_key = str(input_key) + "\n"

    if input_key in keys:
        return True
    else:
        # Reload API keys list then check if the key is in the list again
        # This way API keys can be added on the fly without restarting
        # and IO is reduced since the file isn't loaded on every request
        LoadKeys()
        return input_key in keys is True


if __name__ == "__main__":
    # Generates an API key which is immediately put in the key file and printed to the console
    # API keys are currently 16 bytes in hex format, but that can be easily changed in the future.
    new_key = token_hex(16)
    print(new_key)
    WriteKey(new_key)
else:
    # Loads keys on API startup so verifyKey() works immediately
    LoadKeys()
