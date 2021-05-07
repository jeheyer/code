#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import sys, os
#sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'lib'))

from lib.makejson import *
from lib.http_utils import *

# WSGI entry point
def application(environ, start_response):

    import traceback, json

    response_headers = [ ('Content-type', 'text/plain') ]

    try:

        http_request = vars(HTTPRequest(environ))
        data = main(http_request)
        output = json.dumps(data, indent=2, default=str)

        response_headers = [
            ('Content-type', 'application/json'),
            ('Content-Length', str(len(output))),
            ('Cache-Control', 'no-cache, no-store'),
            ('Pragma', 'no-cache')
        ]
        start_response('200 OK', response_headers)
        #return [ output.encode('utf-8') ]
        return [ http_request['client_ip'].encode('utf-8') ]

    except:

        start_response('500 Internal Server Error', response_headers)
        return [ str(traceback.format_exc()).encode('utf-8') ]
