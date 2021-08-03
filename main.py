import flask
import json
import psycopg2 as pg
from flask import Flask
from src.fsid import convertFSID, validateFSID

api_key = open("api_key.txt", "r").read().strip()

# db_password = open("password.txt", "r").read().strip()
# db_conn = pg.connect("host=localhost port=5432 dbname=flipnotes user=meta_import password = " + db_password)

app = Flask(__name__)


# Return all flipnotes made by specified FSID as a json list
@app.route("/user/<fsid>/flipnotes")
def hello(fsid):
    if flask.request.args.get("key") == api_key:
        if validateFSID(fsid):
            return {"message": "Request valid."}
        else:
            return {"message": "The specified FSID is invalid."}, 403
    else:
        return {"message": "The specified API key is invalid or incorrect."}, 401


# Return all meta in the database for the given flipnote as a json object
@app.route("/flipnote/<filename>/meta")
def hello(filename):
    if flask.request.args.get("key") == api_key:
        return {"message": "Request valid."}
    else:
        return {"message": "The specified API key is invalid or incorrect."}, 401
