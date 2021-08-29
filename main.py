# *********************************************
# Copyright (C) 2021 Meemo <meemo4556@gmail.com> - All Rights Reserved
#
# Unauthorized copying of this file, via any medium is strictly prohibited
#
# Proprietary and confidential
# *********************************************

from json import loads, dumps

import flask
import psycopg2 as pg

from src.auth import VerifyAPIKey
from src.files import VerifyKWZFilename
from src.fsid import VerifyPPMFSID

db_conn_string = "host=localhost port=5432 dbname=flipnotes user=api password=" + open("password.txt").read().strip()

app = flask.Flask(__name__)


# Return all flipnotes made by specified FSID as JSON data
@app.route("/user/<input_fsid>/flipnotes")
async def flipnote_name_list(input_fsid):
    input_fsid = str(input_fsid).strip()
    api_key = flask.request.args.get("key").strip()

    limit = flask.request.args.get("limit")
    if limit is not None:
        limit = int(limit)
    else:
        limit = 9999999999

    offset = flask.request.args.get("offset")
    if offset is not None:
        offset = int(offset)
    else:
        offset = 0

    if VerifyAPIKey(api_key):
        if VerifyPPMFSID(input_fsid):
            # Kaeru team extra options request:
            # - Add current/parent/root filename/fsid/username
            # - Add created and modified timestamps
            # - Sort asc modified timestamp (also asc current filename for result consistency)
            # - Limiting results: count x, offset y
            # - Send number of results in an http header X-Total-Results
            if flask.request.args.get("extra") == "True":
                cur = pg.connect(db_conn_string).cursor()
                cur.execute('''select json_agg(t) from (select
                               current_filename, current_fsid, current_fsid_ppm, current_username,
                               parent_filename, parent_fsid, parent_fsid_ppm, parent_username,
                               root_filename, root_fsid, root_fsid_ppm, root_username,
                               modified_timestamp, created_timestamp
                               from meta where current_fsid_ppm = %s::text
                               order by modified_timestamp asc, current_filename asc
                               limit %s offset %s) t;''', (input_fsid, limit, offset))
                results = dumps(cur.fetchone()[0], ensure_ascii=False)
                cur.close()

                response = flask.make_response(results, 200)
                response.headers["Content-Type"] = "application/json"
                response.headers["X-Total-Results"] = len(loads(results))

                return response
            else:
                cur = pg.connect(db_conn_string).cursor()
                cur.execute(
                    "select json_agg(t) from (select current_filename from meta where current_fsid = %s::text) t;",
                    (input_fsid,))
                results = dumps(cur.fetchone()[0], ensure_ascii=False)
                cur.close()

                response = flask.make_response(results, 200)
                response.headers["Content-Type"] = "application/json"

                return response

        else:
            response = flask.make_response(
                [{"message": "The specified FSID is invalid (does not match PPM FSID regex)."}], 400)
            response.headers["Content-Type"] = "application/json"

            return response
    else:
        response = flask.make_response([{"message": "The specified API key is invalid or incorrect."}], 401)
        response.headers["Content-Type"] = "application/json"

        return response


# Return all meta in the database for the given flipnote as JSON data
@app.route("/flipnote/<filename>/meta")
async def flipnote_meta_list(filename):
    filename = str(filename).strip()
    api_key = flask.request.args.get("key").strip()

    limit = flask.request.args.get("limit")
    if limit is not None:
        limit = int(limit)
    else:
        limit = 9999999999

    offset = flask.request.args.get("offset")
    if offset is not None:
        offset = int(offset)
    else:
        offset = 0

    if VerifyAPIKey(api_key):
        if VerifyKWZFilename(filename):
            cur = pg.connect(db_conn_string).cursor()
            cur.execute('''select json_agg(t) from (
                           select * from meta where current_filename = %s::text
                           limit %s offset %s) t;''', (filename, limit, offset))
            results = dumps(cur.fetchone(), ensure_ascii=False)
            cur.close()

            response = flask.make_response(results, 200)
            response.headers["Content-Type"] = "application/json"
            response.headers["X-Total-Results"] = len(loads(results))

            return response
        else:
            response = flask.make_response([{"message": "The specified file name is invalid."}], 400)
            response.headers["Content-Type"] = "application/json"

            return response
    else:
        response = flask.make_response([{"message": "The specified API key is invalid or incorrect."}], 401)
        response.headers["Content-Type"] = "application/json"

        return response
