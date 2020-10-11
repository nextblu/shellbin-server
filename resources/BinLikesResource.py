import gzip
import json
from flask_restful import Resource, original_flask_make_response
from tentalog import Tentacle
from webargs.flaskparser import use_kwargs, use_args
from modules.request_schema import RequestSchema
from modules.binlikes import BinLikes


logger = Tentacle().logger


class BinLikesResource(Resource):
    @use_args(RequestSchema.BinLikes, location="query")
    def get(self, slug):
        bin_likes = BinLikes()
        slug = slug['slug']
        likes = bin_likes.get_bin_likes(slug)
        response_payload = {"success": True, "likes": likes}
        content = gzip.compress(json.dumps(response_payload, indent=4, sort_keys=True, default=str).encode('utf-8'),
                                9)
        response = original_flask_make_response(content)
        response.headers['Content-Encoding'] = 'gzip'
        return response

    @use_args(RequestSchema.BinLikes, location="query")
    def put(self, slug):
        bin_likes = BinLikes()
        slug = slug['slug']
        likes = bin_likes.increment_bin_likes(slug)
        response_payload = {"success": True, "likes": likes}
        content = gzip.compress(json.dumps(response_payload, indent=4, sort_keys=True, default=str).encode('utf-8'),
                                9)
        response = original_flask_make_response(content)
        response.headers['Content-Encoding'] = 'gzip'
        return response
