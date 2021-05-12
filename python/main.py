#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.makejson import *
from lib.http_utils import *
from flask import Flask

# WSGI entry point
def application(environ, start_response):

    import traceback, json

    response_headers = [ ('Content-type', 'text/plain') ]

    try:

        http_request = vars(HTTPRequest(environ))
        data = main(http_request)
        output = json.dumps(data, default=str)

        response_headers = [
            ('Access-Control-Allow-Origin', '*'),
            ('Content-type', 'application/json'),
            ('Content-Length', str(len(output))),
            ('Cache-Control', 'no-cache, no-store'),
            ('Pragma', 'no-cache')
        ]
        start_response('200 OK', response_headers)
        return [ output.encode('utf-8') ]

    except:

        start_response('500 Internal Server Error', response_headers)
        return [ str(traceback.format_exc()).encode('utf-8') ]

# Flask entry point
app = Flask(__name__)

@app.route("/", defaults = {'path': ""})
@app.route("/<string:path>")
@app.route("/<path:path>")

def root(path):

    from flask import request, jsonify
    import traceback

    http_request = HTTPRequest(request.environ)
    http_request.host = request.host.split(':')[0]
    http_request.path = "/" + path
    http_request.query_string = request.args
    #http_request.request = str(vars(request))
    
    #if request.environ.get('HTTP_X_REAL_IP', None):
    #    http_request.client_ip = request.environ['HTTP_X_REAL_IP']
    #elif request.environ.get('HTTP_X_FORWARDED_FOR', None):
    #    http_request.client_ip = request.environ['HTTP_X_FORWARDED_FOR'][-1]
    #else:
    #    http_request.client_ip = request.remote_addr

    try:
        data = main(vars(http_request))
        response_headers = {
           'Access-Control-Allow-Origin': '*',
           'Cache-Control': 'no-cache, no-store',
           'Pragma': 'no-cache'
        }
        return jsonify(data), response_headers

    except:
        return format(traceback.format_exc()), 500,  {'Content-Type': "text/plain"}

if __name__ == '__main__':
    app.run()
