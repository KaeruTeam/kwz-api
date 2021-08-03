import psycopg2 as pg
from flask import Flask
from flask_restful import Resource, Api, reqparse
from src.fsid import convertFSID, validateFSID

api_key = open("api_key.txt", "r").read().strip()

# db_password = open("password.txt", "r").read().strip()
# db_conn = pg.connect("host=localhost port=5432 dbname=flipnotes user=meta_import password = " + db_password)

app = Flask(__name__)
api = Api(app)


class user(Resource):
    def get(self):
        arg_parser = reqparse.RequestParser()

        arg_parser.add_argument("key", required=True)
        arg_parser.add_argument("fsid", required=True)
        arg_parser.add_argument("scope", required=True)

        args = arg_parser.parse_args()

        if args["key"] == api_key:
            if validateFSID(args["fsid"]):
                if args["scope"] == "flipnotes":
                    # All arguments are valid, proceed with request.

                    print("worked")
                else:
                    return {"message": "Scope is invalid."}, 401
            else:
                return {"message": "FSID is invalid."}, 401
        else:
            return {"message": "API key is invalid or incorrect."}, 401

    def post(self):
        return {"message": "Request is not supported."}, 400

    def head(self):
        return {"message": "Request is not supported."}, 400

    def put(self):
        return {"message": "Request is not supported."}, 400

    def delete(self):
        return {"message": "Request is not supported."}, 400

    pass


class flipnote(Resource):
    def get(self):
        arg_parser = reqparse.RequestParser()

        arg_parser.add_argument("key", required=True)
        arg_parser.add_argument("fsid", required=True)
        arg_parser.add_argument("scope", required=True)

        args = arg_parser.parse_args()

        if args["key"] == api_key:
            if args["scope"] == "meta":
                # Assuming the file name is correct for now
                # TODO: regex for file name
                # All other arguments are valid, proceed with request.

                print("worked")
            else:
                return {"message": "Scope is invalid."}, 401
        else:
            return {"message": "API key is invalid or incorrect."}, 401

    def post(self):
        return {"message": "Request is not supported."}, 400

    def head(self):
        return {"message": "Request is not supported."}, 400

    def put(self):
        return {"message": "Request is not supported."}, 400

    def delete(self):
        return {"message": "Request is not supported."}, 400

    pass


api.add_resource(user, "/user")
api.add_resource(flipnote, "/flipnote")

if __name__ == "__main__":
    app.run()
