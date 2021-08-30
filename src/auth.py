keys = []


# Read API keys from the text file
def LoadKeys():
    global keys
    keys = open("api_key.txt").readlines()


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


# Loads keys on API startup so verifyKey() works immediately
LoadKeys()
