import gzip
import json
from flask_restful import Resource, original_flask_make_response
from tentalog import Tentacle
from webargs.flaskparser import use_kwargs, use_args
from modules.request_schema import RequestSchema
from modules.binviews import BinViews


logger = Tentacle().logger


class BinViewsResource(Resource):
    @use_args(RequestSchema.BinViews, location="query")
    def get(self, slug):
        bin_views = BinViews()
        slug = slug['slug']
        views = bin_views.get_bin_views(slug)
        response_payload = {"success": True, "views": views}
        content = gzip.compress(json.dumps(response_payload, indent=4, sort_keys=True, default=str).encode('utf-8'),
                                9)
        response = original_flask_make_response(content)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Content-Encoding'] = 'gzip'
        return response

    @use_args(RequestSchema.BinViews, location="query")
    def put(self, slug):
        bin_views = BinViews()
        slug = slug['slug']
        views = bin_views.increment_bin_views(slug)
        response_payload = {"success": True, "views": views}
        content = gzip.compress(json.dumps(response_payload, indent=4, sort_keys=True, default=str).encode('utf-8'),
                                9)
        response = original_flask_make_response(content)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Content-Encoding'] = 'gzip'
        return response
