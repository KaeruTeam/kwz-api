# *********************************************
# Copyright (C) 2021 Meemo <meemo4556@gmail.com> - All Rights Reserved
#
# Unauthorized copying of this file, via any medium is strictly prohibited
#
# Proprietary and confidential
# *********************************************

import flask
import json
import psycopg2 as pg
import src.fsid as fsid_utils
import src.files as file_utils
import src.auth as auth

db_conn_string = "host=localhost port=5432 dbname=flipnotes user=api password=" + open("password.txt").read().strip()

app = flask.Flask(__name__)


# Return all flipnotes made by specified FSID as JSON data
@app.route("/user/<fsid>/flipnotes")
async def flipnote_name_list(fsid):
    fsid = str(fsid).strip()
    api_key = flask.request.args.get("key").strip()

    if auth.verifyAPIKey(api_key):
        if fsid_utils.VerifyPPMFSID(fsid):
            # Kaeru team extra options request:
            # - Add current/parent/root filename/fsid/username
            # - Add created and modified timestamps
            # - Sort ascending by modified timestamp
            if flask.request.args.get("extra") == "True":
                cur = pg.connect(db_conn_string).cursor()
                cur.execute('''select row_to_json(t) from (select
                               current_filename, current_fsid, current_fsid_ppm, current_username,
                               parent_filename, parent_fsid, parent_fsid_ppm, parent_username,
                               root_filename, root_fsid, root_fsid_ppm, root_username,
                               modified_timestamp, created_timestamp
                               from meta where current_fsid_ppm = %s::text
                               order by modified_timestamp asc) t;''', (fsid,))
                results = cur.fetchall()
                cur.close()

                return json.dumps(results[0], ensure_ascii=False), 200
            else:
                cur = pg.connect(db_conn_string).cursor()
                cur.execute('''select row_to_json(t) from (select current_filename from meta where current_fsid = %s::text) t;''', (fsid,))
                results = cur.fetchall()
                cur.close()

                return json.dumps(results[0], ensure_ascii=False), 200

        else:
            return [{"message": "The specified FSID is invalid (does not match PPM FSID regex)."}], 400
    else:
        return [{"message": "The specified API key is invalid or incorrect."}], 401


# Return all meta in the database for the given flipnote as JSON data
@app.route("/flipnote/<filename>/meta")
async def flipnote_meta_list(filename):
    filename = str(filename).strip()
    api_key = flask.request.args.get("key").strip()

    # Trim file extension in case it was passed
    if filename.endswith(".kwz"):
        filename = filename[:-4]

    if auth.verifyAPIKey(api_key):
        # Verify the filename is valid
        if file_utils.VerifyKWZFilename(filename):
            cur = pg.connect(db_conn_string).cursor()
            cur.execute('''select row_to_json(t) from (select * from meta where current_filename = %s::text) t;''', (filename,))
            results = cur.fetchall()

            cur.close()
            return json.dumps(results, ensure_ascii=False), 200
        else:
            return [{"message": "The specified file name is invalid."}], 400
    else:
        return [{"message": "The specified API key is invalid or incorrect."}], 401
