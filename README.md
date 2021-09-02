# api.kwz.pw

The kwz.pw API is intended to be used for accessing metadata, file contents, and possibly more from the Flipnote Studio 3D: DSi Library file set.

# Documentation
Please visit [the wiki](https://github.com/meemo/api.kwz.pw/wiki) for documentation of the API.

# Setup
## Requirements
The API is designed and tested to be run on Debian 10+ and Python 3.7+. Other platforms should work if the equivalent packages are downloaded, however support is not guaranteed.

To install all requirements, run:

```shell
sudo apt install -y build-essential python3 python3-dev
python3 -m pip install -r requirements.txt
```

## Deployment
To start the API, run this in the API directory:

```shell
uwsgi uwsgi.ini
```

# Todo
- Expose API to the public
    - Create a proper website for the API
        - Migrate away from kwz.pw?
    - Set up a system for requesting API keys on website
- Move to django?
- Move to another language for speed?
    - Go?
    - JS (for flipnote.js)?
