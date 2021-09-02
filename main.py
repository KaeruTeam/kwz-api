from os import path
from json import loads, dumps

from flask import Flask, request, make_response, send_file
from psycopg2 import connect

from src.auth import VerifyAPIKey
from src.files import VerifyKWZFilename
from src.fsid import VerifyPPMFSID

# The path to the flipnotes file directory
# File structure should be [base_file_path]/[fsid]/[file].[kwz|jpg]
base_file_path = path.join("/home/meemo/dsi_library/")

db_conn_string = "host=localhost port=5432 dbname=flipnotes user=api password=" + open("password.txt").read().strip()

app = Flask(__name__)


# Generates a response for flask containing necessary headers.
def MakeResponse(content, code):
    response = make_response(content, code)
    response.headers["Content-Type"] = "application/json"
    response.headers["X-Total-Results"] = len(loads(dumps(content)))

    return response


# Return all flipnotes made by specified FSID as JSON data
@app.route("/user/<input_fsid>/flipnotes")
async def FSIDFlipnotes(input_fsid):
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

    escapeUnicode = request.args.get("escapeUnicode").lower()
    if escapeUnicode == "true":
        escapeUnicode = True
    else:
        escapeUnicode = False

    if VerifyAPIKey(api_key):
        if VerifyPPMFSID(input_fsid):
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
                               root_filename, root_fsid, root_fsid_ppm, root_username,
                               modified_timestamp, created_timestamp
                               from meta where current_fsid_ppm = %s
                               order by modified_timestamp asc, current_filename asc
                               limit %s offset %s) t;''', (input_fsid, limit, offset))
                results = dumps(cur.fetchone()[0], ensure_ascii=escapeUnicode)
                cur.close()

                # Check if there are any results
                if results != "null":
                    return MakeResponse(results, 200)
                else:
                    return MakeResponse({"error": "Your request did not produce any results."}, 404)
            else:
                cur = connect(db_conn_string).cursor()
                cur.execute('''select json_agg(t) from (select 
                               current_filename from meta where current_fsid_ppm = %s
                               limit %s offset %s) t;''', (input_fsid, limit, offset))
                results = dumps(cur.fetchone()[0], ensure_ascii=escapeUnicode)
                cur.close()

                # Check if there are any results
                if results != "null":
                    return MakeResponse(results, 200)
                else:
                    return MakeResponse({"error": "Your request did not produce any results."}, 404)
        else:
            return MakeResponse({"error": "The specified FSID is invalid."}, 400)
    else:
        return MakeResponse({"error": "The specified API key is invalid or incorrect."}, 401)


# Return all meta in the database for the given flipnote as JSON data
@app.route("/flipnote/<file_name>/meta")
async def FlipnoteMeta(file_name):
    file_name = str(file_name).strip()
    api_key = request.args.get("key").strip()

    limit = request.args.get("limit")
    if limit is not None:
        limit = int(limit)
    else:
        # Arbitrarily high; no limit to result
        # Setting to "all" had type errors with psycopg2
        limit = 9999999999

    offset = request.args.get("offset")
    if offset is not None:
        offset = int(offset)
    else:
        offset = 0

    escapeUnicode = request.args.get("escapeUnicode").lower()
    if escapeUnicode == "true":
        escapeUnicode = True
    else:
        escapeUnicode = False

    if VerifyAPIKey(api_key):
        if VerifyKWZFilename(file_name):
            cur = connect(db_conn_string).cursor()
            cur.execute('''select json_agg(t) from (
                           select * from meta where current_filename = %s
                           limit %s offset %s) t;''', (file_name, limit, offset))
            results = dumps(cur.fetchone()[0], ensure_ascii=escapeUnicode)
            cur.close()

            return MakeResponse(results, 200)
        else:
            return MakeResponse({"error": "The specified file name is invalid."}, 400)
    else:
        return MakeResponse({"error": "The specified API key is invalid or incorrect."}, 401)


@app.route("/flipnote/<file_name>/<file_type>")
async def FlipnoteDownload(file_name, file_type):
    file_name = str(file_name).strip()
    file_type = str(file_type).strip()
    api_key = request.args.get("key").strip()

    if VerifyAPIKey(api_key):
        if VerifyKWZFilename(file_name):
            # Fetch FSID from DB
            cur = connect(db_conn_string).cursor()
            cur.execute('''select json_agg(t) from (
                           select current_fsid_ppm from meta 
                           where current_filename = %s) t;''', (file_name,))
            results = dumps(cur.fetchone()[0])
            cur.close()

            if results != "null":
                file_path = path.join(base_file_path, str(results[0]), str(file_name + "." + file_type))

                # Check that the file exists at the specified location
                # In case the database and filesystem are out of sync
                if path.isfile(file_path):
                    # Note: the thumbnail files could be deleted and instead be
                    # extracted on the fly
                    if file_type == "kwz" or file_type == "jpg":
                        send_file(file_path, as_attachment=True)
                    else:
                        return MakeResponse({"error": "The requested file does not exist in the filesystem."}, 404)
                else:
                    return MakeResponse({"error": "The specified file type is not supported."}, 400)
            else:
                return MakeResponse({"error": "The specified file does not exist."}, 404)
        else:
            return MakeResponse({"error": "The specified file name is invalid."}, 400)
    else:
        return MakeResponse({"error": "The specified API key is invalid or incorrect."}, 401)
