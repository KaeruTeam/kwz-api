from json import loads, dumps
from os.path import join, isfile

from flask import Flask, request, send_file
from flipnote.schema import verifyPPMFSID, verifyKWZFilename
from psycopg2 import connect

from src.auth import load_api_keys, verify_api_key
from src.misc import make_response, make_db_conn_string

app = Flask(__name__)


# Documentation located at docs/endpoints/user.md
@app.route("/user/<input_fsid>/flipnotes")
async def fsid_flipnotes(input_fsid):
    # Process arguments
    input_fsid = str(input_fsid).strip()
    api_key = str(request.args.get("key")).strip()

    limit = request.args.get("limit")
    if limit is not None:
        limit = int(limit)
    else:
        # psycopg2 has type issues with "all", so this value is arbitrarily high
        limit = 9999999999

    offset = request.args.get("offset")
    if offset is not None:
        offset = int(offset)
    else:
        offset = 0

    escape_unicode = request.args.get("escapeUnicode")
    if escape_unicode is None:
        escape_unicode = False
    else:
        escape_unicode = True

    # Verify the API key is valid
    if not verify_api_key(api_key, keys):
        return make_response({"error": "The specified API key is invalid or incorrect."}, 401)

    # Verify that the FSID input is valid
    if not verifyPPMFSID(input_fsid):
        return make_response({"error": "The specified FSID is invalid."}, 400)

    # If the extra flag is set to true, add extra values (see docs/endpoints/user.md#optional)
    if request.args.get("extra").lower() == "true":
        cur = connect(db_conn_string).cursor()
        cur.execute('''select json_agg(t) from (select
                       current_filename, current_fsid, current_fsid_ppm, current_username,
                       parent_filename, parent_fsid, parent_fsid_ppm, parent_username,
                       root_filename, root_fsid, root_fsid_ppm, root_username, modified_timestamp
                       from meta where current_fsid_ppm = %s
                       order by modified_timestamp asc, current_filename asc
                       limit %s offset %s) t;''', (input_fsid, limit, offset))
        results = dumps(cur.fetchone()[0], ensure_ascii=escape_unicode)
        cur.close()

        # Verify the DB returned any results
        if results == "null":
            return make_response({"error": "Your request did not produce any results."}, 404)

        # All checks passed, return result
        return make_response(results, 200)
    else:
        cur = connect(db_conn_string).cursor()
        cur.execute('''select json_agg(t) from (select
                       current_filename from meta where current_fsid_ppm = %s
                       limit %s offset %s) t;''', (input_fsid, limit, offset))
        results = dumps(cur.fetchone()[0], ensure_ascii=escape_unicode)
        cur.close()

        # Verify the DB returned any results
        if results == "null":
            return make_response({"error": "Your request did not produce any results."}, 404)

        # All checks passed, return result
        return make_response(results, 200)


# Documentation located at docs/endpoints/flipnote.md
@app.route("/flipnote/<file_name>/meta")
async def flipnote_meta(file_name):
    # Process arguments
    file_name = str(file_name).strip()
    api_key = str(request.args.get("key")).strip()

    limit = request.args.get("limit")
    if limit is not None:
        limit = int(limit)
    else:
        # psycopg2 has type issues with "all", so this value is arbitrarily high
        limit = 9999999999

    offset = request.args.get("offset")
    if offset is not None:
        offset = int(offset)
    else:
        offset = 0

    escape_unicode = request.args.get("escapeUnicode")
    if escape_unicode is None:
        escape_unicode = False
    else:
        escape_unicode = True

    # Verify the API key is valid
    if not verify_api_key(api_key, keys):
        return make_response({"error": "The specified API key is invalid or incorrect."}, 401)

    # Verify the flipnote name is correct
    if not verifyKWZFilename(file_name):
        return make_response({"error": "The specified file name is invalid."}, 400)

    cur = connect(db_conn_string).cursor()
    cur.execute('''select json_agg(t) from (
                   select * from meta where current_filename = %s
                   limit %s offset %s) t;''', (file_name, limit, offset))
    results = dumps(cur.fetchone()[0], ensure_ascii=escape_unicode)
    cur.close()

    # Verify the DB returned any results
    if results == "null":
        return make_response({"error": "Your request did not produce any results."}, 404)

    # All checks passed, return result
    return make_response(results, 200)


# Documentation located at docs/endpoints/flipnote.md
@app.route("/flipnote/<file_name>/<file_type>")
async def download_flipnote(file_name, file_type):
    # Process arguments
    file_name = str(file_name).strip()
    file_type = str(file_type).strip()
    api_key = str(request.args.get("key")).strip()

    # Verify the API key is valid
    if not verify_api_key(api_key, keys):
        return make_response({"error": "The specified API key is invalid or incorrect."}, 401)

    # Verify that the file type is supported
    if not (file_type == "kwz" or file_type == "jpg"):
        return make_response({"error": "The specified file type is not supported."}, 400)

    # Verify the flipnote name is correct
    if not verifyKWZFilename(file_name):
        return make_response({"error": "The specified file name is invalid."}, 400)

    # Fetch FSID from DB in order to create file path
    cur = connect(db_conn_string).cursor()
    cur.execute('''select json_agg(t) from (
                   select current_fsid_ppm from meta 
                   where current_filename = %s
                   ) t;''', (file_name, ))
    results = cur.fetchone()[0]
    cur.close()

    # Verify the DB returned any results
    # If it didn't, there's no meta on the file, and thus there must be no file to download
    if results is None:
        return make_response({"error": "The specified file does not exist."}, 404)

    # Create file path based on DB result
    file_path = join(base_flipnote_path, results[0]["current_fsid_ppm"], str(file_name + "." + file_type))

    # Check that the file exists in case the database contains meta of files that are not in the filesystem
    if not isfile(file_path):
        return make_response({"error": "The requested file does not exist in the filesystem."}, 404)

    # All checks passed, return file
    return send_file(file_path, as_attachment=True), 200


# Finds duplicate flipnotes from other conversion runs in the database based on the following:
# - PPM format current, root, parent FSIDs
#     - KWZ format FSIDs have changing prefix, we don't want to account for this
# - Timestamp
# - root + current usernames (NOT PARENT, they are incorrect on some revisions)
# - frame count (just in case? idk)
#
# Return the current file names
@app.route("/fdupes/<file_name>")
async def find_dupes(file_name):
    # Process arguments
    file_name = str(file_name).strip()
    api_key = str(request.args.get("key")).strip()

    # Verify the API key is valid
    if not verify_api_key(api_key, keys):
        return make_response({"error": "The specified API key is invalid or incorrect."}, 401)

    # Verify the flipnote name is valid
    if not verifyKWZFilename(file_name):
        return make_response({"error": "The specified file name is invalid."}, 400)

    cur = connect(db_conn_string).cursor()
    cur.execute('''select json_agg(t) from (
                       select current_fsid_ppm, parent_fsid_ppm, root_fsid_ppm, 
                       modified_timestamp, root_username, current_username, frame_count
                       from meta where current_filename = %s
                       ) t;''', (file_name,))
    results = cur.fetchone()[0]
    cur.close()

    # Verify the DB returned any results
    if results is None:
        return make_response({"error": "The specified file does not exist."}, 404)
    else:
        results = results[0]

    cur = connect(db_conn_string).cursor()
    cur.execute('''select json_agg(t) from (
                   select current_filename from meta 
                   where current_fsid_ppm = %s and parent_fsid_ppm = %s and root_fsid_ppm = %s and 
                   modified_timestamp = %s and root_username = %s  nd current_username = %s and frame_count = %s
                   ) t;''', (results["current_fsid_ppm"], results["parent_fsid_ppm"], results["root_fsid_ppm"],
                             results["modified_timestamp"],
                             results["root_username"], results["current_username"],
                             results["frame_count"]))
    results = dumps(cur.fetchall()[0][0])
    cur.close()

    # All checks passed, return file
    return make_response(results, 200)


if __name__ == "__main__":
    print("This file is not intended to be run on its own! Please check README.md")
    exit(1)
else:
    # Read config file
    with open("config.json", "r", encoding="utf-8") as input_file:
        config = loads(input_file.read())

    db_conn_string = make_db_conn_string(config)
    base_flipnote_path = join(config["flipnotes_file_path"])

    # Load API keys
    keys = load_api_keys(join(config["api_keys_file"]))
