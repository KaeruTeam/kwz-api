from secrets import token_hex

# Generates an API key which is immediately put in the key file and printed to the console
# API keys are currently 16 bytes in hex format, but that can be easily changed in the future.

key = token_hex(16)

print(key)

with open("api_key.txt", "a") as file:
    file.write(str(key) + "\n")
