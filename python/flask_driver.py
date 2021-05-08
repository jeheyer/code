#!/usr/bin/env python3

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
    if 'x-real-ip' in request.headers:
        http_request.client_ip = request.headers['x-real-ip']
    else:
        http_request.client_ip = request.remote_addr

    try:
        data = main(vars(http_request))
        return jsonify(data)

    except:
        return format(traceback.format_exc()), 500,  {'Content-Type': "text/plain"}

if __name__ == '__main__':
    app.run()

