# Documentation
Welcome to the kwz-api documentation! Please refer to the table of contents below to navigate to a certain page.

For a setup guide, please view [info/setup.md](info/setup.md).


# Table of Contents
- [`endpoints/`](endpoints)
    - [`flipnote`](endpoints/flipnote.md)
      - Contains `/flipnote/{file name}/{meta|kwz|jpg}` endpoint
    - [`user`](endpoints/user.md)
      - Contains `/user/{FSID}/flipnotes` endpoint
- [`info/`](info)
    - [`setup`](info/setup.md)
      - Contains the full setup procedure for the API
    - [`db`](info/db.md)
      - Contains descriptions of the rows and columns of the database table that the API uses
    - [`glossary`](info/glossary.md)
      - Contains definitions of terms that are used throughout the documentation

    
# Formatting Notes
- URLs are given as fragments like, for example, `/user/{FSID}/flipnotes`. This is intended to be appended to an IP or domain and a port like: `127.0.0.1:9090/user/{FSID}/flipnotes`

- Values that are `{in curly braces}` are to be replaced with the value they describe, not including the curly braces themselves.
