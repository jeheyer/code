#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from lib.http_utils import *
from lib.makejson import *

app = Flask(__name__)

@app.route("/", defaults = {'path': ""})
@app.route("/<string:path>")
@app.route("/<path:path>")

def root(path):

    from flask import request, jsonify
    import traceback

    http_request = HTTPRequest()
    http_request.host = request.host.split(':')[0]
    http_request.path = "/" + path
    http_request.query_string = request.args
    
    if request.environ.get('HTTP_X_REAL_IP', None):
        http_request.client_ip = request.environ['HTTP_X_REAL_IP']
    elif request.environ.get('HTTP_X_FORWARDED_FOR', None):
        http_request.client_ip = request.environ['HTTP_X_FORWARDED_FOR']
    else:
        http_request.client_ip = request.remote_addr

    try:
        data = main(vars(http_request))
        return jsonify(data), 200, {'Content-Type': "application/json"}

    except:
        return format(traceback.format_exc()), 500,  {'Content-Type': "text/plain"}

if __name__ == '__main__':
    app.run()

