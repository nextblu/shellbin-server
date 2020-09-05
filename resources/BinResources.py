#  """
#  Copyright (c) 2020 NextBlu systems - - All Rights Reserved.
#   * MIT License
#   * Written by Mattia Failla <mattia@nextblu.com>, May 2020
#   """

import gzip
import json
import random
import string

from flask import request
from flask_restful import Resource, original_flask_make_response
from tentalog import Tentacle
from modules.bin import Bin

logger = Tentacle().logger

class BinResource(Resource):

    def get(self, slug):
        logger.info(f"Requested Bin with slug {slug}")
        data = Bin().get_bin_legacy(slug)
        response_payload = {"success": True, "resource": data}
        # gzipping the data
        content = gzip.compress(json.dumps(response_payload, indent=4, sort_keys=True, default=str).encode('utf-8'), 9)
        response = original_flask_make_response(content)
        response.headers['Content-Encoding'] = 'gzip'
        return response

    def post(self):
        data = request.get_json()
        logger.info(f"Received Bin creation request {data}")
        # generating a random string
        slug = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
        Bin().insert_bin_legacy(data, url=slug)
        return slug
