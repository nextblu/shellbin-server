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
from resources.BinV2Resource import BinV2Resource
from tentalog import Tentacle

logger = Tentacle().logger

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


# Legacy version
log_routes = [
    "/api/v1/bin/<string:slug>",
    "/api/v1/bin/new"
]

api.add_resource(BinResource, *log_routes)

# Bin v2
api.add_resource(BinV2Resource, "api/v2/bin/")

# Statistics


if __name__ == '__main__':
    isProduction = False
    port = 3000
    host = "0.0.0.0"

    try:
        if os.environ['IS_PRODUCTION'] == 'production':
            logger.info(f"Found IS_PRODUCTION environment variable set, overriding the current mode")
            isProduction = True
    except KeyError:
        isProduction = False

    logger.info(f"Starting server at port {port} with production mode set to {isProduction}")

    if isProduction:
        bjoern.run(app, host, port)
    else:
        app.run(host=host, port=port, debug=True)
