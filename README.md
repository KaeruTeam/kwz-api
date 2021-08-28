# api.kwz.pw

![](https://forthebadge.com/images/badges/compatibility-betamax.svg)
![](https://forthebadge.com/images/badges/mom-made-pizza-rolls.svg)

The kwz.pw API is intended to be used for accessing metadata and file contents from my Flipnote Studio 3D DSi Library
file set.

# Endpoints

These are the current endpoints for the API, proper documentation will be created later.

`http://api.kwz.pw/user/{fsid}/flipnotes?key={api key}?extra={True|False}`

Returns a JSON object listing all flipnotes with the given FSID as current author ID.

`http://api.kwz.pw/flipnote/{file name}/meta?key={api key}`

Returns a JSON object listing all metadata in the database for the given flipnote.

# Setup

```shell
sudo apt install -y build-essential python3 python3-dev
python3 -m pip install -r requirements.txt
```

# Deployment

```shell
uwsgi uwsgi.ini
```

# Todo

- Create proper documentation
- Make file downloading available through the API
- Create/set up a proper logging system
- Expose API to the public
  - Create a proper website for the API
    - Migrate away from kwz.pw?
  - Set up a system for requesting API keys on website


#### Tentative

- Move to django?
- Move to another language for speed? 
  - Go?
- Expand to Flipnote Studio 3D world flipnotes once set is available? 
