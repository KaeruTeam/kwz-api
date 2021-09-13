# flipnote
The `flipnote` endpoint is for interacting with individual flipnotes. In this endpoint you can fetch information (metadata) about a specific flipnote, download the thumbnail for the flipnote, or download the flipnote itself.

## URL
#### Metadata
`/flipnote/{file name}/meta`

This will return all available metadata in the database for the specified flipnote.

#### Download file
`/flipnote/{file name}/{file type}`

This allows you to download files relating to the specified flipnote. Valid file types are specified below.


## HTTP Method
- `GET`


## Parameters
### Path
- `{file name}`

This is the kwz format file name of the flipnote.

- `{file type}`

This is the file extension for the file you wish to download. The following table details the accepted types:

| Type | Description |
|---|---|
| kwz | The flipnote as a file |
| jpg | The flipnote's thumbnail. |

### Query
#### Required
- `key={API Key}`

This is your API key.

#### Optional
- `escapeUnicode={True or False}`

This will escape non UTF-8 characters. For example, `ッ` will become `\u30c3` when `True` is passed.

Note: Any text other than `True` (case-insensitive) will not enable this parameter.


## Response
### Success
#### Metadata
- Code: `200`
  Content (example from flipnote `ccccccccccccccjgv1kwwmhr1nvc`):
```json
[
    {
        "lock":true,
        "loop":false,
        "flags":17,
        "layer_flags":0,
        "app_version":0,
        "frame_count":207,
        "frame_speed":7,
        "thumb_index":206,
        "timestamp":1229556234,
        "frame_flags_mask":0,
        "root_username":"にんてんどう",
        "root_fsid":"00000000000000000000",
        "root_filename":"ccccccccccccccrjwycnwtclcjcc",
        "parent_username":"にんてんどう",
        "parent_fsid":"00000000000000000000",
        "parent_filename":"7DD445_086B896919B43_000",
        "current_username":"にんてんどう",
        "current_fsid":"00000000000000000000",
        "current_filename":"ccccccccccccccjgv1kwwmhr1nvc",
        "track_frame_speed":3,
        "bgm_used":false,
        "se1_used":false,
        "se2_used":false,
        "se3_used":false,
        "bgm_digest":null,
        "se1_digest":null,
        "se2_digest":null,
        "se3_digest":null,
        "current_fsid_ppm":"0000000000000000",
        "parent_fsid_ppm":"0000000000000000",
        "root_fsid_ppm":"0000000000000000"
    }
]
```

#### Download file
- **Code**: `200` \
  Content: [the requested file]

### Failure
#### Metadata and download file
- **Problem**: the API Key is invalid. \
  Response:
    - **Code**: `401` \
      Content: `{"error": "The specified API key is invalid or incorrect."}`

- **Problem**: the file name does not match the regex. \
  Response:
    - **Code**: `400` \
      Content: `{"error": "The specified file name is invalid."}`

- **Problem**: the file is not in the database or does not exist. \
  Response:
    - **Code**: `404` \
      Content: `{"error": "The specified file does not exist."}`

- **Problem**: the file type passed is not `kwz` or `jpg` (only supported file types). \
  Response:
    - **Code**: `400` \
      Content: `{"error": "The specified file type is not supported."}`


## Example Call
#### Metadata
`/flipnote/ccccccccccccccjgv1kwwmhr1nvc/meta?key={API key}`

#### Download file
`/flipnote/ccccccccccccccjgv1kwwmhr1nvc/kwz?key={API key}`
