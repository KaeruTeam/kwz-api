# api.kwz.pw

![](https://forthebadge.com/images/badges/compatibility-betamax.svg)
![](https://forthebadge.com/images/badges/mom-made-pizza-rolls.svg)

The kwz.pw API is intended to be used for accessing metadata and file contents from my Flipnote Studio 3D DSi Library
file set.

# Features

These are the current features for the API, documentation will be created when the scope of the project expands.

`http://api.kwz.pw/user/{fsid}/flipnotes?key={api key}?extra={True|False}`

Returns a JSON object listing all flipnotes with the given FSID as current author ID.

`http://api.kwz.pw/flipnote/{file name}/meta?key={api key}`

Returns a JSON object listing all metadata in the database for the given flipnote.

# Usage (production)

```shell
sudo apt install -y build-essential python3-dev
python3 -m pip install -r requirements.txt
```

The rest to be written later.

# Todo

- Expose API to the public
- Create a proper website for the API
- Create proper documentation on the API
- Make API key verification a cleaner and more secure process
- Make file downloading require API key
- Create a proper logging system
- Move to django?
- Move to another language for speed? Go?
- Set up a system for requesting API keys
