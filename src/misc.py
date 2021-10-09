from json import loads, dumps

from flask import make_response as flask_make_response

"""
This file contains miscellaneous functions for the API, put here for cleanliness.
"""


# Generates a response for flask containing necessary headers.
def make_response(content, code):
    response = flask_make_response(content, code)
    response.headers["Content-Type"] = "application/json"
    response.headers["X-Total-Results"] = len(loads(dumps(content)))

    return response


# Create string for connecting to DB using the values specified in the config file
def make_db_conn_string(config):
    return "host={0} port={1} dbname={2} user={3} password={4}".format(config["db"]["host"],
                                                                       config["db"]["port"],
                                                                       config["db"]["dbname"],
                                                                       config["db"]["user"],
                                                                       config["db"]["password"])
