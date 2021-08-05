import flask
import psycopg2 as pg
import src.fsid as fsid_utils
import src.files as file_utils

api_key = open("api_key.txt", "r").read().strip()

db_password = open("password.txt", "r").read().strip()
db_conn = pg.connect("host=localhost port=5432 dbname=flipnotes user=meta_import password = " + db_password)

app = flask.Flask(__name__)


# Return all flipnotes made by specified FSID as JSON data
@app.route("/user/<fsid>/flipnotes")
def flipnote_name_list(fsid):
    sql_statement = "select row_to_json(t) from (select current_filename from meta where current_fsid = %s::text) t;"

    fsid = str(fsid).strip()

    if flask.request.args.get("key") == api_key:
        if fsid_utils.ConvertKWZtoPPM(fsid):
            cur = db_conn.cursor()

            cur.execute(sql_statement, fsid)
            results = cur.fetchall()

            cur.close()
            return results, 200
        else:
            return {"message": "The specified FSID is invalid."}, 400
    else:
        return {"message": "The specified API key is invalid or incorrect."}, 401


# Return all meta in the database for the given flipnote as JSON data
@app.route("/flipnote/<filename>/meta")
def flipnote_meta_list(filename):
    sql_statement = "select row_to_json(t) from (select * from meta where current_filename = %s::text) t;"

    filename = str(filename).strip()

    # Trim file extension if it exists
    if filename.endswith(".kwz"):
        filename = filename[:-4]

    if flask.request.args.get("key") == api_key:
        if file_utils.VerifyFilename(filename):
            cur = db_conn.cursor()

            cur.execute(sql_statement, filename)
            results = cur.fetchall()

            cur.close()
            return results, 200
        else:
            return {"message": "The specified file name is invalid."}, 400
    else:
        return {"message": "The specified API key is invalid or incorrect."}, 401
