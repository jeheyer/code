#!/usr/bin/env python3

from makerest import *
import json

# WSGI entry point
def application(environ, start_response):

    import traceback

    request = { 
        'host': environ.get('HTTP_HOST', 'localhost'),
        'path': environ.get('REQUEST_URI', '/'),
        'query_string': {}
    }

    try:

        if '?' in request['path']:
            request['path'], query_string = environ.get('REQUEST_URI', '/').split('?')
            for _ in environ.get('QUERY_STRING', None).split('&'):
                [key, value] = _.split('=')
                request['query_string'][key] = value

        data = main(request)
        output = json.dumps(data, sort_keys=True, indent=2)

        response_headers = [
            ('Content-type', 'application/json'),
            ('Content-Length', str(len(output))),
            ('X-Backend-Server', 'WSGI')
        ]
        start_response('200 OK', response_headers)
        return [ output.encode('utf-8') ]

    except:

        response_headers = [ ('Content-type', 'text/plain') ]
        start_response('500 Internal Server Error', response_headers)
        error = traceback.format_exc()
        return [ str(error).encode('utf-8') ]
