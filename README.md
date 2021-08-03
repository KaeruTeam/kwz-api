# api.kwz.pw

The kwz.pw API is intended to be used for accessing metadata and file contents from the Flipnote Studio 3D DSi Library file set.

# Features

These are the current features for the API, documentation will be created when the scope of the project expands.

`http://api.kwz.pw/user/{fsid}/flipnotes?key={api key}`

Returns a JSON list of all flipnotes with the given FSID as current author ID.

`http://api.kwz.pw/flipnote/{file name}/meta?key={api key}`

# Usage (testing)

`pip3 install -r requirements.txt`

### Bash

 ```shell
$ export FLASK_APP=main
$ flask run
```

### Powershell

```
> $env:FLASK_APP = "main"
> flask run
```


# Usage (production)

`pip3 install -r requirements.txt`

The rest to be written later.
