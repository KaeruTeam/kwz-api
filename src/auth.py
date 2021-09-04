from os import path, getcwd
from secrets import token_hex

keys = []


# Read API keys from the text file
def loadKeys():
    global keys
    keys = open("api_key.txt", "r").readlines()


# Verifies that the API key is in the list
def verifyAPIKey(input_key):
    # Adding the newline so that `input_key in keys` works
    input_key = str(input_key) + "\n"

    if input_key in keys:
        return True
    else:
        # Reload API keys list then check if the key is in the list again
        # This way API keys can be added on the fly without restarting
        # and IO is reduced since the file isn't loaded on every request
        loadKeys()
        return input_key in keys is True


if __name__ == "__main__":
    # Generates an API key which is immediately put in the key file and printed to the console
    # API keys are currently 16 bytes in hex format, but that can be easily changed in the future.
    file_path = path.abspath(path.join(path.dirname(__file__), '..', 'api_key.txt'))

    new_key = token_hex(16)
    print(new_key)

    with open(file_path, "a") as file:
        file.write(str(new_key) + "\n")
else:
    # Loads keys on API startup so verifyKey() works immediately
    loadKeys()
