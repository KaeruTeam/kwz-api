import psycopg2
from flask import Flask
from flask_restful import Resource, Api, reqparse
from src.FSIDUtils import kwzToPPM

api_key = open("api_key.txt", "r").read().strip()

# db_password = open("password.txt", "r").read().strip()
# db_conn = psycopg2.connect("host=localhost port=5432 dbname=flipnotes user=meta_import password = " + db_password)

app = Flask(__name__)
api = Api(app)


class kwz(Resource):
    def get(self):
        # Check for correct API key.
        parser = reqparse.RequestParser()
        parser.add_argument("key", required=True)
        args = parser.parse_args()

        if args["key"] == api_key:
            # Key is valid, process request.

            return {"response": "hi"}
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
        args = arg_parser.parse_args()

        if args["key"] == api_key:
            # Key is valid, process request.

            return {"response": "hi"}
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


api.add_resource(kwz, "/kwz")
api.add_resource(flipnote, "/flipnote")

if __name__ == "__main__":
    app.run()
