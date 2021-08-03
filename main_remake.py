import flask
import psycopg2 as pg
from markupsafe import escape
from flask import Flask
from src.fsid import convertFSID, validateFSID

api_key = open("api_key.txt", "r").read().strip()

# db_password = open("password.txt", "r").read().strip()
# db_conn = pg.connect("host=localhost port=5432 dbname=flipnotes user=meta_import password = " + db_password)

app = Flask(__name__)


@app.route("/<name>")
def hello(name):
    print(flask.request.args.get("key"))
    return escape(name)
