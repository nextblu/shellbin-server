# Version 2 bin creator for shellbin

#  """
#  Copyright (c) 2020 NextBlu systems - - All Rights Reserved.
#   * MIT License
#   * Written by Mattia Failla <mattia@nextblu.com>, Sept 2020
#   """
import gzip
import json
import random
import string


from flask_restful import Resource, original_flask_make_response
from tentalog import Tentacle
from webargs.flaskparser import use_kwargs

from modules.bin import Bin
from modules.request_schema import RequestSchema

logger = Tentacle().logger


class BinV2Resource(Resource):
    @use_kwargs(RequestSchema.BinV2POST)
    def post(self, creator, title, data, private, language):
        slug = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
        Bin().insert_bin_v2(creator, title, data, private, url=slug, language)
        return slug

    @use_kwargs(RequestSchema.BinV2GET)
    def get(self, slug):
        logger.info(f"Requested Bin with slug {slug}")
        data = Bin().get_bin_legacy(slug)
        response_payload = {"success": True, "resource": data}
        # gzipping the data
        content = gzip.compress(json.dumps(response_payload, indent=4, sort_keys=True, default=str).encode('utf-8'), 9)
        response = original_flask_make_response(content)
        response.headers['Content-Encoding'] = 'gzip'
        return response
