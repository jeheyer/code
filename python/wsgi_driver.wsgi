#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.makejson import *
from lib.http_utils import *

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
