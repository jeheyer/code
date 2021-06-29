#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from quart import Quart
from lib.http_utils import *
from lib.makejson import *
import traceback

app = Quart(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/", defaults = {'path': ""})
@app.route("/<string:path>")
@app.route("/<path:path>")
async def root(path):

    from quart import request
    from quart.helpers import make_response
    from quart.json import jsonify

    http_request = HTTPRequest()
    http_request.host = request.host.split(':')[0]
    http_request.path = "/" + path
    http_request.query_string = request.args

    for _ in request.headers.items():
         if _[0] == "User-Agent":
             http_request.user_agent = _[1]
         if _[0] == "X-Real-Ip":
             http_request.client_ip = _[1]
         if _[0] == "X-Forwarded-For":
             http_request.client_ip = _[1].split(",")[-2]
         if _[0] == "X-Appengine-User-Ip":
             http_request.client_ip = _[1]
         if _[0] == "X-Forwarded-Proto" and _[1] == "https":
             http_request.front_end_https = True
         if _[0] == "X-Appengine-Https":
             http_request.front_end_https = True
         
    try:
        data = main(vars(http_request))
        #data = vars(request.headers)
        return jsonify(data), 200

    except:
        return format(traceback.format_exc()), 500,  {'Content-Type': "text/plain"}

if __name__ == '__main__':
    app.run()
