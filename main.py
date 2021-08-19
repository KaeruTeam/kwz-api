# *********************************************
# Copyright (C) 2021 Meemo <meemo4556@gmail.com> - All Rights Reserved
#
# Unauthorized copying of this file, via any medium is strictly prohibited
#
# Proprietary and confidential
# *********************************************

import flask
import psycopg2 as pg
import src.fsid as fsid_utils
import src.files as file_utils

api_keys = open("api_key.txt", "r").read()

db_conn_string = "host=localhost port=5432 dbname=flipnotes user=meta_import password=" + open("password.txt").read().strip()

app = flask.Flask(__name__)


# Return all flipnotes made by specified FSID as JSON data
@app.route("/user/<fsid>/flipnotes")
async def flipnote_name_list(fsid):
    db_conn = pg.connect(db_conn_string)

    fsid = str(fsid).strip()

    if flask.request.args.get("key").strip() in api_keys:
        if fsid_utils.VerifyPPMFSID(fsid):
            if flask.request.args.get("extra") == "True":
                # Kaeru team extra options request:
                # - Add current/parent/root filename/fsid/username
                # - Add created and modified timestamps
                # - Sort ascending by modified timestamp

                sql_statement = '''
                                select row_to_json(t) from (select
                                current_filename, current_fsid, current_fsid_ppm, current_username,
                                parent_filename, parent_fsid, parent_fsid_ppm, parent_username,
                                root_filename, root_fsid, root_fsid_ppm, root_username,
                                modified_timestamp, created_timestamp
                                from meta where current_fsid_ppm = %s::text
                                order by modified_timestamp asc) t;
                                '''

                cur = db_conn.cursor()

                cur.execute(sql_statement, (fsid,))
                results = cur.fetchall()

                cur.close()
                return str(results), 200
            else:
                sql_statement = '''
                                select row_to_json(t) from (select current_filename
                                from meta where current_fsid = %s::text) t;
                                '''

                cur = db_conn.cursor()

                cur.execute(sql_statement, (fsid,))
                results = cur.fetchall()

                cur.close()
                return str(results), 200

        else:
            return {"message": "The specified FSID is invalid (does not match PPM FSID regex)."}, 400
    else:
        return {"message": "The specified API key is invalid or incorrect."}, 401


# Return all meta in the database for the given flipnote as JSON data
@app.route("/flipnote/<filename>/meta")
async def flipnote_meta_list(filename):
    db_conn = pg.connect(db_conn_string)

    filename = str(filename).strip()

    # Trim file extension if it exists
    if filename.endswith(".kwz"):
        filename = filename[:-4]

    # Check for a valid API key
    if flask.request.args.get("key").strip() in api_keys:
        # Verify the filename is valid
        if file_utils.VerifyKWZFilename(filename):
            sql_statement = "select row_to_json(t) from (select * from meta where current_filename = %s::text) t;"

            cur = db_conn.cursor()

            cur.execute(sql_statement, (filename,))
            results = cur.fetchall()

            cur.close()
            return str(results), 200
        else:
            return {"message": "The specified file name is invalid."}, 400
    else:
        return {"message": "The specified API key is invalid or incorrect."}, 401
