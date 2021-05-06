#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'lib'))

from makejson import *
from http_utils import *

# WSGI entry point
def application(environ, start_response):

    import traceback, json
    from urllib import parse

    request = vars(http_request(environ))

    response_headers = [ ('Content-type', 'text/plain') ]

    try:

        if '?' in request['request_uri']:
            request['query_string'] = dict(parse.parse_qsl(parse.urlsplit(request['request_uri']).query))
            #request['path'], query_string = environ.get('REQUEST_URI', '/').split('?')
            #for _ in environ.get('QUERY_STRING', None).split('&'):
            #    [key, value] = _.split('=')
            #    request['query_string'][key] = value

        data = main(request)
        output = json.dumps(data, indent=2, default=str)

        response_headers = [
            ('Content-type', 'application/json'),
            ('Content-Length', str(len(output))),
            ('Cache-Control', 'no-cache, no-store'),
            ('Pragma', 'no-cache')
        ]
        start_response('200 OK', response_headers)
        return [ output.encode('utf-8') ]

    except:

        start_response('500 Internal Server Error', response_headers)
        error = traceback.format_exc()
        return [ str(error).encode('utf-8') ]
