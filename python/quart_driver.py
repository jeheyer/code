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
def root(path):

    from quart import request
    from quart.helpers import make_response
    from quart.json import jsonify

    http_request = HTTPRequest(request = request)

    try:
        data = main(vars(http_request))
        return jsonify(data), 200

    except:
        return format(traceback.format_exc()), 500,  {'Content-Type': "text/plain"}

if __name__ == '__main__':
    app.run()
