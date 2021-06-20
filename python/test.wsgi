#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# WSGI entry point
def application(environ, start_response):

    import traceback, json

    response_headers = [ ('Content-type', 'text/plain') ]

    try:

        output = json.dumps(environ, default=str)

        response_headers = [
            ('Content-type', 'application/json'),
            ('Content-Length', str(len(output)))
        ]

        start_response('200 OK', response_headers)
        return [ output.encode('utf-8') ]

    except:

        start_response('500 Internal Server Error', response_headers)
        return [ str(traceback.format_exc()).encode('utf-8') ]

