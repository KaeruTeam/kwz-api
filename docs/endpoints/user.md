# user
The `user` endpoint is for interacting with individual users (identified by FSIDs). This endpoint can be used to find all flipnotes in the database that a user has created, as well as some creator details about those flipnotes with the `extra` parameter.

## URL
`user/{FSID}/flipnotes`
This returns all flipnotes that the given user is `current_author` of in the database.

## HTTP Method
- `GET`


## Parameters
### Path
- `{FSID}`

This is the ppm format FSID of the user.

### Query
#### Required
- `key={API Key}`

This is your API key.

#### Optional
- `escapeUnicode={True or False}`

This will escape non UTF-8 characters. For example, `ッ` will become `\u30c3` when `True` is passed. Any other text (including not specifying the argument) will not escape the characters.

- `extra={True or False}`

This adds the following things (a feature request from Kaeru):
- Add current/parent/root filename/fsid/username
- Add created and modified timestamps
- Sort ascending by modified timestamp
   - also sort ascending by current filename for result consistency

Note: Any text other than `True` (case-insensitive) will not enable this parameter.

- `limit={integer}`

This parameter limits the number of rows of results that are returned in the response.

- `offset={integer}`

This parameter begins the output rows with the given number as its index.

Note: if an offset past the range of the output is specified, `Your request did not produce any results.` will be returned as shown below.


## Response
### Success
- Code: `200`
  Content (example from `/user/0000000000000000/flipnotes?key={API key}&limit=5`):

```json
[
    {
        "current_filename":"ccccccccccccccjgv1kwwmhr1nvc"
    },
    {
        "current_filename":"mcccccccccccccmpvskwcy0f1nvc"
    },
    {
        "current_filename":"mcccccccccccccjgv1kwwmhr1nvc"
    },
    {
        "current_filename":"mcccccccccccccrhvpkwwyhj1nvc"
    },
    {
        "current_filename":"mcccccccccccccw2vskwcsmf1nvc"
    }
]
```

### Failure
- **Problem**: the API Key is invalid. \
  Response:
    - **Code**: `401` \
      Content: `{"error": "The specified API key is invalid or incorrect."}`

- **Problem**: the FSID does not match the regex. Note that FSIDs must be ppm format. \
  Response:
    - **Code**: `400` \
      Content: `{"error": "The specified FSID is invalid."}`

- **Problem**: the user is not in the database, or it does not exist. This also will happen when `offset` is set past the range of the results. \
  Response:
    - **Code**: `404` \
      Content: `{"error": "Your request did not produce any results."}`


## Example Calls
- `/user/0000000000000000/flipnotes?key={API key}`

- `/user/0000000000000000/flipnotes?key={API key}&extra=True&offset=10&limit=500`