#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from quart import Quart
from lib.http_utils import *
from lib.makejson import *

app = Quart(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/", defaults = {'path': ""})
@app.route("/<string:path>")
@app.route("/<path:path>")
async def root(path):

    from quart.json import jsonify
    from quart import request
    import traceback

    http_request = HTTPRequest()
    http_request.host = request.host.split(':')[0]
    http_request.path = "/" + path
    http_request.query_string = request.args
    
    try:
        data = main(vars(http_request))
        return jsonify(data), 200, {'Content-Type': "application/json"}

    except:
        return format(traceback.format_exc()), 500,  {'Content-Type': "text/plain"}

if __name__ == '__main__':
    app.run()
