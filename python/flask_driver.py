#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from lib.http_utils import *
from lib.makejson import *
import traceback

app = Flask(__name__)

@app.route("/", defaults = {'path': ""})
@app.route("/<path:path>")
@app.route("/<string:path>")
def root(path):

    http_request = HTTPRequest(request.environ)
    
    try:
        data = main(vars(http_request))
        return jsonify(data), 200

    except:
        return format(traceback.format_exc()), 500,  {'Content-Type': "text/plain"}

if __name__ == '__main__':
    app.run(debug=True)

