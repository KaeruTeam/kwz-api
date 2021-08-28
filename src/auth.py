# *********************************************
# Copyright (C) 2021 Meemo <meemo4556@gmail.com> - All Rights Reserved
#
# Unauthorized copying of this file, via any medium is strictly prohibited
#
# Proprietary and confidential
# *********************************************

keys = []


# Read API keys from the text file
def loadKeys():
    global keys
    keys = open("api_key.txt").readlines()


# Verifies that the API key is in the list
def verifyAPIKey(input_key):
    # Trim any whitespace just in case
    input_key = input_key.trim()

    if input_key in keys:
        return True
    else:
        # Reload API keys list then check if the key is in the list again
        # This way API keys can be added on the fly without restarting
        # and IO is reduced since the file isn't loaded on every request
        loadKeys()
        return input_key in keys is True


# Loads keys on API startup so verifyKey() works immediately
loadKeys()
