from os import path
from json import loads, dumps

from flask import Flask, request, make_response, send_file
from psycopg2 import connect

from flipnote import schema

with open("config.json", "r", encoding="utf-8") as input_file:
    config = loads(input_file.read())

db_conn_string = "host={0} port={1} dbname={2} user={3} password={4}".format(config["db"]["host"],
                                                                             config["db"]["port"],
                                                                             config["db"]["dbname"],
                                                                             config["db"]["user"],
                                                                             config["db"]["password"])

app = Flask(__name__)

base_file_path = path.join(config["flipnotes_file_path"])

keys = []


# Read API keys from the text file
def loadAPIKeys():
    global keys
    keys = []
    with open(path.join(config["api_keys_file"]), "r", encoding="utf-8") as file:
        for key in file.readlines():
            keys.append(key.strip())


# Verifies that the API key is in the list
def verifyAPIKey(input_key):
    if input_key in keys:
        return True
    else:
        # Reload API keys list then check if the key is in the list again
        loadAPIKeys()
        return input_key in keys


# Generates a response for flask containing necessary headers.
def makeResponse(content, code):
    response = make_response(content, code)
    response.headers["Content-Type"] = "application/json"
    response.headers["X-Total-Results"] = len(loads(dumps(content)))

    return response


# Return all flipnotes made by specified FSID as JSON data
@app.route("/user/<input_fsid>/flipnotes")
async def fsidFlipnotes(input_fsid):
    input_fsid = str(input_fsid).strip()
    api_key = request.args.get("key").strip()

    limit = request.args.get("limit")
    if limit is not None:
        limit = int(limit)
    else:
        limit = 9999999999

    offset = request.args.get("offset")
    if offset is not None:
        offset = int(offset)
    else:
        offset = 0

    escapeUnicode = request.args.get("escapeUnicode")
    if escapeUnicode is None:
        escapeUnicode = False
    else:
        escapeUnicode = True

    if verifyAPIKey(api_key):
        if schema.verifyPPMFSID(input_fsid):
            # Kaeru team extra options request:
            # - Add current/parent/root filename/fsid/username
            # - Add created and modified timestamps
            # - Sort asc modified timestamp
            #   - also asc current filename for consistency
            # - Limiting results: count x, offset y
            # - Send number of results in an http header X-Total-Results
            if request.args.get("extra").lower() == "true":
                cur = connect(db_conn_string).cursor()
                cur.execute('''select json_agg(t) from (select
                               current_filename, current_fsid, current_fsid_ppm, current_username,
                               parent_filename, parent_fsid, parent_fsid_ppm, parent_username,
                               root_filename, root_fsid, root_fsid_ppm, root_username, timestamp
                               from meta where current_fsid_ppm = %s
                               order by timestamp asc, current_filename asc
                               limit %s offset %s) t;''', (input_fsid, limit, offset))
                results = dumps(cur.fetchone()[0], ensure_ascii=escapeUnicode)
                cur.close()

                if results != "null":
                    return makeResponse(results, 200)
                else:
                    return makeResponse({"error": "Your request did not produce any results."}, 404)
            else:
                cur = connect(db_conn_string).cursor()
                cur.execute('''select json_agg(t) from (select 
                               current_filename from meta where current_fsid_ppm = %s
                               limit %s offset %s) t;''', (input_fsid, limit, offset))
                results = dumps(cur.fetchone()[0], ensure_ascii=escapeUnicode)
                cur.close()

                if results != "null":
                    return makeResponse(results, 200)
                else:
                    return makeResponse({"error": "Your request did not produce any results."}, 404)
        else:
            return makeResponse({"error": "The specified FSID is invalid."}, 400)
    else:
        return makeResponse({"error": "The specified API key is invalid or incorrect."}, 401)


# Return all meta in the database for the given flipnote as JSON data
@app.route("/flipnote/<file_name>/meta")
async def flipnoteMeta(file_name):
    file_name = str(file_name).strip()
    api_key = request.args.get("key").strip()

    limit = request.args.get("limit")
    if limit is not None:
        limit = int(limit)
    else:
        limit = 9999999999  # Arbitrarily high; no limit

    offset = request.args.get("offset")
    if offset is not None:
        offset = int(offset)
    else:
        offset = 0

    escapeUnicode = request.args.get("escapeUnicode")
    if escapeUnicode is None:
        escapeUnicode = False
    else:
        escapeUnicode = True

    if verifyAPIKey(api_key):
        if schema.verifyKWZFilename(file_name):
            cur = connect(db_conn_string).cursor()
            cur.execute('''select json_agg(t) from (
                           select * from meta where current_filename = %s
                           limit %s offset %s) t;''', (file_name, limit, offset))
            results = dumps(cur.fetchone()[0], ensure_ascii=escapeUnicode)
            cur.close()

            return makeResponse(results, 200)
        else:
            return makeResponse({"error": "The specified file name is invalid."}, 400)
    else:
        return makeResponse({"error": "The specified API key is invalid or incorrect."}, 401)


@app.route("/flipnote/<file_name>/<file_type>")
async def flipnoteDownload(file_name, file_type):
    file_name = str(file_name).strip()
    file_type = str(file_type).strip()
    api_key = request.args.get("key").strip()

    if verifyAPIKey(api_key):
        if schema.verifyKWZFilename(file_name):
            # Fetch FSID from DB
            cur = connect(db_conn_string).cursor()
            cur.execute('''select json_agg(t) from (
                           select current_fsid_ppm from meta 
                           where current_filename = %s) t;''', (file_name,))
            results = cur.fetchone()[0]
            cur.close()

            if results is not None:
                file_path = path.join(path.join(config["flipnotes_file_path"]),
                                      results[0]["current_fsid_ppm"],
                                      str(file_name + "." + file_type))

                # Check that the file exists at the specified location
                # In case the database and filesystem are out of sync
                if path.isfile(file_path):
                    # Note: the thumbnail files could be deleted and instead be
                    # extracted on the fly
                    if file_type == "kwz" or file_type == "jpg":
                        return send_file(file_path, as_attachment=True), 200
                    else:
                        return makeResponse({"error": "The requested file does not exist in the filesystem."}, 404)
                else:
                    return makeResponse({"error": "The specified file type is not supported."}, 400)
            else:
                return makeResponse({"error": "The specified file does not exist."}, 404)
        else:
            return makeResponse({"error": "The specified file name is invalid."}, 400)
    else:
        return makeResponse({"error": "The specified API key is invalid or incorrect."}, 401)


if __name__ == "__main__":
    print("This program is not designed to be run alone! Please check README.md")
else:
    # Load API keys when the file is loaded by uwsgi
    loadAPIKeys()
