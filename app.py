#  """
#  Copyright (c) 2020 NextBlu systems - - All Rights Reserved.
#   * MIT License
#   * Written by Mattia Failla <mattia@nextblu.com>, May 2020
#   """

import os

import bjoern
from flask import Flask
from flask_restful import Api

from resources.BinResources import BinResource

__author__ = "@NextBlu core team"

app = Flask(__name__)
api = Api(app)


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type, Authorization"
    )
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,PATCH,OPTIONS")
    return response


# @todo: Move me to routes_configuration.py
log_routes = [
    "/api/v1/bin/<string:slug>",
    "/api/v1/bin/new"
]

api.add_resource(BinResource, *log_routes)

if __name__ == '__main__':
    isProduction = False

    port = 3000
    host = "0.0.0.0"

    if os.environ['IS_PRODUCTION'] == 'production':
        isProduction = True

    if isProduction:
        bjoern.run(app, host, port)
    else:
        app.run(host=host, port=port, debug=True)
