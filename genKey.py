# *********************************************
# Copyright (C) 2021 Meemo <meemo4556@gmail.com> - All Rights Reserved
#
# Unauthorized copying of this file, via any medium is strictly prohibited
#
# Proprietary and confidential
# *********************************************

from secrets import token_hex

# Generates an API key which is immediately put in the key file and printed to the console
# API keys are currently 16 bytes in hex format, but that can be easily changed in the future.

key = token_hex(16)

print(key)

with open("api_key.txt", "a") as file:
    file.write(str(key) + "\n")
