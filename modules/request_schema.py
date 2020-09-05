# PAYLOAD VERIFICATION
from webargs import fields, validate
from webargs.flaskparser import parser, abort


@parser.error_handler
def handle_args(error, req, schema, error_status_code, error_headers):
    abort(422, status="fail", result=error.messages, exc=error)


class RequestSchema:
    # BIN creation v2
    BinV2POST = {
        "creator": fields.Str(
            required=True, validate=validate.Regexp("([0-9a-zA-Z .@_-]){2,60}")
        ),
        "title": fields.Str(
            required=True, validate=validate.Regexp("([0-9a-zA-Z .@_-]){1,60}")
        ),
        "data": fields.Str(required=True),
        "private": fields.Bool(required=True)
    }
    BinV2GET = {
        "slug": fields.Str(
            required=True, validate=validate.Regexp("([0-9a-zA-Z .@_-]){2,60}")
        ),
    }
