# setup
This file contains instructions to set up the API from scratch.

First, clone the repository:

`git clone https://github.com/meemo/kwz-api`

And then `cd` into the directory:

`cd kwz-api/`

The rest of this guide assumes that commands are run in this terminal that is in the `kwz-api/` folder initially.


# Requirements
The API is tested and developed on Debian Linux 10+. 
Other operating systems will in theory work, however no guide will be provided to set them up.

## Debian
All requirements and dependencies can be installed with the following commands:

```shell
sudo apt install -y build-essential python3 python3-pip python3-dev postgresql
python3 -m pip install -r requirements.txt
```

## Other Operating Systems
These lists contain all required packages for the API. Installing these packages should allow the API to work, however it is untested.

### System package manager
- Python 3.7+ 
    - pip 
    - Dev Headers
- `build-essential`
    - Contains basic compilation tools and libraries. Required for pip in order to compile `psycopg2`
- PostgreSQL 11+ (13 preferred)

### pip
- `uwsgi`
- `flask`
    - [async] extra is required
- `psycopg2`
- `flipnote` 
    - only version 0.0.5 is tested to work

After the above system packages are installed, all pip packages can be installed on most operating systems with:

```shell
python3 -m pip install -r requirements.txt
```


# Database Setup
First, you will need to log in as the `postgres` user in order to create the database:

```shell
sudo -iu postgres
```

Now, we can create the database:

```shell
createdb dsi_library
```

...and begin to set up the database:

```shell
psql dsi_library
```

Create the table:

```sql
create table meta (
lock boolean, loop boolean, flags smallint, layer_flags smallint, app_version smallint,
frame_count smallint, frame_speed smallint, thumb_index smallint, timestamp bigint,
root_username text, root_fsid text, root_fsid_ppm text, root_filename text,
parent_username text, parent_fsid text, parent_fsid_ppm text, parent_filename text,
current_username text, current_fsid text, current_fsid_ppm text, current_filename text,
track_frame_speed smallint,
bgm_used boolean, se1_used boolean, se2_used boolean, se3_used boolean,
bgm_digest text, se1_digest text, se2_digest text, se3_digest text
);
```

Create indexes to drastically improve performance when the DB gets larger:

```sql
create index current_filename on meta (current_filename);
```

```sql
create index current_fsid_ppm on meta (current_fsid_ppm);
```

First generate a long and secure password using a password manager or other service, then create the DB user using the following command:

```sql
create user api with password '{put password here}'
```

*Note: replace `{put password here}` with your generated password, and do not include the `{}` curly brackets. Also, record this password somewhere as it is needed in the next section.*

Add permissions to the new user:

```sql
grant select, insert on table meta to api;
```

Finally, exit the DB:

```sql
\q
```

And return to your original user:

```shell
exit
```


# Configs
The repo contains template config files that need to be filled out and renamed for the API to work.
Every `{curly bracket}` value needs to be replaced with something that is specified below.
All other values do not need to be changed assuming you followed this guide exactly.

### `config.json.template`

- `"password"`

This value should be the `api` user password you set up in the above step.

- `"flipnotes_file_path"`

This value should be the path to the folder with all flipnotes in the original S3 bucket file structure.
Below this directory should be all the FSID folders which contain the .kwz and .jpg files.

`flipnote_path_path/{fsid}/{file name.(kwz|jpg)}`

### uwsgi.ini.template
No values are required to be changed in this file, however if you would like to change the port, that can be configured on line 2.

# Importing Flipnotes

To be implemented and written.


# Usage
To start the API, run this in the API directory:

```shell
uwsgi uwsgi.ini
```
